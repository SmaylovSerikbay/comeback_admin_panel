from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from sales_dashboard.models import PaymentRecord
from admin_api.permissions import IsAdminOrCashier, get_user_role
from firebase_service import firebase_service


class DashboardStatsView(APIView):
    permission_classes = [IsAdminOrCashier]

    def get(self, request):
        user_role = get_user_role(request.user)
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        stats = {
            'today': {
                'payments': PaymentRecord.objects.filter(created_at__date=today).count(),
                'successful': PaymentRecord.objects.filter(created_at__date=today, status='success').count(),
                'revenue': PaymentRecord.objects.filter(
                    created_at__date=today, status='success'
                ).aggregate(total=Sum('amount'))['total'] or 0,
            },
            'week': {
                'payments': PaymentRecord.objects.filter(created_at__date__gte=week_ago).count(),
                'successful': PaymentRecord.objects.filter(created_at__date__gte=week_ago, status='success').count(),
                'revenue': PaymentRecord.objects.filter(
                    created_at__date__gte=week_ago, status='success'
                ).aggregate(total=Sum('amount'))['total'] or 0,
            },
            'month': {
                'payments': PaymentRecord.objects.filter(created_at__date__gte=month_ago).count(),
                'successful': PaymentRecord.objects.filter(created_at__date__gte=month_ago, status='success').count(),
                'revenue': PaymentRecord.objects.filter(
                    created_at__date__gte=month_ago, status='success'
                ).aggregate(total=Sum('amount'))['total'] or 0,
            },
            'all_time': {
                'payments': PaymentRecord.objects.count(),
                'successful': PaymentRecord.objects.filter(status='success').count(),
                'revenue': PaymentRecord.objects.filter(status='success').aggregate(total=Sum('amount'))['total'] or 0,
            },
        }

        recent = PaymentRecord.objects.order_by('-created_at')[:10]
        recent_list = [
            {
                'id': p.id,
                'order_id': p.order_id,
                'amount': p.amount,
                'currency': p.currency,
                'status': p.status,
                'created_at': p.created_at.isoformat(),
            }
            for p in recent
        ]

        firebase_status = 'connected' if firebase_service.is_initialized() else 'warning'

        return Response({
            'stats': stats,
            'recent_payments': recent_list,
            'firebase_status': firebase_status,
            'user_role': user_role,
        })
