from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from subscription.models import SubscriptionSettings
from firebase_service import firebase_service
from admin_api.permissions import IsAdmin


class SubscriptionSettingsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        settings = SubscriptionSettings.get_settings()
        return Response(settings.to_firebase_dict())

    def put(self, request):
        settings = SubscriptionSettings.get_settings()
        price = request.data.get('price')
        duration_minutes = request.data.get('duration_minutes')
        currency = request.data.get('currency')
        is_active = request.data.get('is_active')
        online_payment_enabled = request.data.get('online_payment_enabled')
        otp_enabled = request.data.get('otp_enabled')
        if price is not None:
            try:
                settings.price = float(price)
            except (TypeError, ValueError):
                return Response({'error': 'Некорректная цена'}, status=status.HTTP_400_BAD_REQUEST)
        if duration_minutes is not None:
            try:
                duration_minutes = int(duration_minutes)
                if duration_minutes < 1 or duration_minutes > 1440:
                    return Response({'error': 'Длительность от 1 до 1440 минут'}, status=status.HTTP_400_BAD_REQUEST)
                settings.duration_minutes = duration_minutes
            except (TypeError, ValueError):
                return Response({'error': 'Некорректная длительность'}, status=status.HTTP_400_BAD_REQUEST)
        if currency is not None:
            settings.currency = str(currency)
        if is_active is not None:
            settings.is_active = bool(is_active)
        if online_payment_enabled is not None:
            settings.online_payment_enabled = bool(online_payment_enabled)
        if otp_enabled is not None:
            settings.otp_enabled = bool(otp_enabled)
        settings.updated_by = request.user.username
        settings.save()
        firebase_data = settings.to_firebase_dict()
        firebase_service.update_subscription_settings(firebase_data)
        return Response(firebase_data)
