from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count, Max
from django.utils import timezone
from datetime import timedelta
from sales_dashboard.models import PaymentRecord
from admin_api.permissions import IsAdmin, get_user_role


class StatisticsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        if get_user_role(request.user) != 'admin':
            return Response({'error': 'Доступ только для администратора'}, status=403)
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)
        daily_revenue = []
        for i in range(30):
            date = thirty_days_ago + timedelta(days=i)
            revenue = PaymentRecord.objects.filter(
                created_at__date=date,
                status='success'
            ).aggregate(total=Sum('amount'))['total'] or 0
            daily_revenue.append({'date': date.strftime('%d.%m'), 'revenue': revenue})
        status_stats = list(
            PaymentRecord.objects.values('status').annotate(count=Count('id')).order_by('status')
        )
        total_payments = sum(s['count'] for s in status_stats)
        successful = next((s['count'] for s in status_stats if s['status'] == 'success'), 0)
        total_revenue = PaymentRecord.objects.filter(status='success').aggregate(
            total=Sum('amount')
        )['total'] or 0
        top_users = list(
            PaymentRecord.objects.values('user_id').annotate(
                payment_count=Count('id'),
                total_amount=Sum('amount'),
                last_payment=Max('created_at'),
            ).filter(user_id__isnull=False).exclude(user_id='').order_by('-total_amount')[:10]
        )
        return Response({
            'daily_revenue': daily_revenue,
            'total_payments': total_payments,
            'successful_payments': successful,
            'total_revenue': total_revenue,
            'status_stats': status_stats,
            'top_users': top_users,
        })
