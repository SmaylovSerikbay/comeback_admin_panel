from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from sales_dashboard.models import PaymentRecord
from otp_manager.models import OTPCode
from admin_api.permissions import IsAdminOrCashier, get_user_role


class PaymentListView(APIView):
    permission_classes = [IsAdminOrCashier]

    def get(self, request):
        status_filter = request.GET.get('status', 'all')
        date_filter = request.GET.get('date', 'all')
        payment_type = request.GET.get('type', 'all')

        payments_qs = PaymentRecord.objects.all()
        if status_filter != 'all':
            payments_qs = payments_qs.filter(status=status_filter)
        if date_filter == 'today':
            payments_qs = payments_qs.filter(created_at__date=timezone.now().date())
        elif date_filter == 'week':
            week_ago = timezone.now().date() - timedelta(days=7)
            payments_qs = payments_qs.filter(created_at__date__gte=week_ago)
        elif date_filter == 'month':
            month_ago = timezone.now().date() - timedelta(days=30)
            payments_qs = payments_qs.filter(created_at__date__gte=month_ago)

        if payment_type == 'online':
            otp_payments = []
        else:
            otp_codes = OTPCode.objects.all().order_by('-created_at')
            if date_filter == 'today':
                otp_codes = otp_codes.filter(created_at__date=timezone.now().date())
            elif date_filter == 'week':
                week_ago = timezone.now().date() - timedelta(days=7)
                otp_codes = otp_codes.filter(created_at__date__gte=week_ago)
            elif date_filter == 'month':
                month_ago = timezone.now().date() - timedelta(days=30)
                otp_codes = otp_codes.filter(created_at__date__gte=month_ago)
            otp_payments = [
                {
                    'id': f'otp_{otp.id}',
                    'order_id': f'OTP-{otp.code}',
                    'amount': float(otp.amount),
                    'currency': otp.currency,
                    'status': 'completed' if otp.status == 'used' else ('pending' if otp.status == 'active' else 'failed'),
                    'payment_method': 'cash_otp',
                    'description': f'Наличный платеж - {otp.quantity} билетов',
                    'created_at': otp.created_at.isoformat(),
                    'customer_name': f'OTP: {otp.code}',
                    'quantity': otp.quantity,
                    'is_otp': True,
                    'otp_code': otp.code,
                }
                for otp in otp_codes
            ]

        if payment_type == 'cash':
            regular_list = []
        else:
            regular_list = [
                {
                    'id': p.id,
                    'order_id': p.order_id,
                    'amount': p.amount,
                    'currency': p.currency,
                    'status': p.status,
                    'payment_method': getattr(p, 'payment_method', 'online'),
                    'description': p.description or '',
                    'created_at': p.created_at.isoformat(),
                    'customer_name': getattr(p, 'customer_name', '') or p.user_id or '—',
                    'quantity': 1,
                    'is_otp': False,
                }
                for p in payments_qs
            ]

        all_payments = regular_list + otp_payments
        all_payments.sort(key=lambda x: x['created_at'], reverse=True)

        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 20))
        start = (page - 1) * per_page
        end = start + per_page
        page_items = all_payments[start:end]

        return Response({
            'payments': page_items,
            'total': len(all_payments),
            'page': page,
            'per_page': per_page,
            'user_role': get_user_role(request.user),
        })
