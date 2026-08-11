import random
import string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from otp_manager.models import OTPCode
from firebase_service import firebase_service
from admin_api.permissions import IsAdminOrCashier, IsCashier, get_user_role


def generate_unique_otp():
    for _ in range(100):
        code = ''.join(random.choices(string.digits, k=6))
        if not OTPCode.objects.filter(code=code).exists():
            return code
    raise ValueError('Could not generate unique OTP')


class OTPListView(APIView):
    permission_classes = [IsAdminOrCashier]

    def get(self, request):
        if request.user.is_superuser:
            qs = OTPCode.objects.all()
        else:
            qs = OTPCode.objects.filter(created_by=request.user)
        qs = qs.order_by('-created_at')
        items = [
            {
                'id': str(otp.id),
                'code': otp.code,
                'amount': float(otp.amount),
                'quantity': otp.quantity,
                'currency': otp.currency,
                'status': otp.status,
                'created_at': otp.created_at.isoformat(),
                'created_by': otp.created_by.username,
                'used_at': otp.used_at.isoformat() if otp.used_at else None,
            }
            for otp in qs
        ]
        return Response({
            'otp_codes': items,
            'is_admin': request.user.is_superuser,
        })


class OTPCreateView(APIView):
    permission_classes = [IsCashier]

    def post(self, request):
        amount = request.data.get('amount')
        quantity = request.data.get('quantity', 1)
        currency = request.data.get('currency', 'UZS')
        try:
            amount = float(amount)
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response(
                {'error': 'amount и quantity должны быть числами'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if amount <= 0:
            return Response({'error': 'Сумма должна быть больше нуля'}, status=status.HTTP_400_BAD_REQUEST)
        if quantity < 1 or quantity > 10:
            return Response({'error': 'Количество чеков от 1 до 10'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            code = generate_unique_otp()
        except ValueError:
            return Response({'error': 'Не удалось сгенерировать код'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        otp = OTPCode.objects.create(
            code=code,
            amount=amount,
            quantity=quantity,
            currency=currency,
            created_by=request.user,
        )
        firebase_key = firebase_service.add_otp_code(otp)
        if firebase_key:
            otp.firebase_key = firebase_key
            otp.save(update_fields=['firebase_key'])
        return Response({
            'id': str(otp.id),
            'code': otp.code,
            'amount': float(otp.amount),
            'quantity': otp.quantity,
            'currency': otp.currency,
            'created_at': otp.created_at.isoformat(),
        }, status=status.HTTP_201_CREATED)


class OTPCashPaymentView(APIView):
    permission_classes = [IsCashier]

    def get(self, request):
        settings_data = firebase_service.get_subscription_settings() or {}
        return Response({
            'subscription_price': settings_data.get('price', 5000),
            'subscription_currency': settings_data.get('currency', 'UZS'),
            'subscription_duration': settings_data.get('duration_minutes', 30),
        })

    def post(self, request):
        quantity = request.data.get('quantity')
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response(
                {'error': 'Укажите количество билетов (1-10)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if quantity < 1 or quantity > 10:
            return Response({'error': 'Количество билетов от 1 до 10'}, status=status.HTTP_400_BAD_REQUEST)
        settings_data = firebase_service.get_subscription_settings()
        if not settings_data:
            return Response({'error': 'Не удалось получить настройки подписки'}, status=status.HTTP_502_BAD_GATEWAY)
        price_per_ticket = settings_data.get('price', 5000)
        currency = settings_data.get('currency', 'UZS')
        duration_per_ticket = settings_data.get('duration_minutes', 30)
        created = []
        for _ in range(quantity):
            code = generate_unique_otp()
            otp = OTPCode.objects.create(
                code=code,
                amount=price_per_ticket,
                quantity=duration_per_ticket,
                currency=currency,
                created_by=request.user,
            )
            firebase_key = firebase_service.add_otp_code(otp)
            if firebase_key:
                otp.firebase_key = firebase_key
                otp.save(update_fields=['firebase_key'])
            created.append({
                'id': str(otp.id),
                'code': otp.code,
                'amount': float(otp.amount),
                'quantity': otp.quantity,
                'currency': otp.currency,
            })
        return Response({
            'created': created,
            'message': f'Создано {len(created)} OTP кодов',
        }, status=status.HTTP_201_CREATED)


class OTPDetailView(APIView):
    permission_classes = [IsAdminOrCashier]

    def get(self, request, otp_id):
        try:
            otp = OTPCode.objects.get(pk=otp_id)
        except OTPCode.DoesNotExist:
            return Response({'error': 'OTP не найден'}, status=status.HTTP_404_NOT_FOUND)
        if not request.user.is_superuser and otp.created_by != request.user:
            return Response({'error': 'Нет прав'}, status=status.HTTP_403_FORBIDDEN)
        return Response({
            'id': str(otp.id),
            'code': otp.code,
            'amount': float(otp.amount),
            'quantity': otp.quantity,
            'currency': otp.currency,
            'status': otp.status,
            'created_at': otp.created_at.isoformat(),
            'created_by': otp.created_by.username,
            'used_at': otp.used_at.isoformat() if otp.used_at else None,
            'device_id': otp.device_id,
        })
