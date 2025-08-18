"""
Views for Sales Dashboard app
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import PaymentRecord, DailyStats
from video_manager.models import UserRole
from firebase_service import firebase_service
from otp_manager.models import OTPCode
import logging

logger = logging.getLogger(__name__)

def get_user_role(user):
    """Get user role"""
    try:
        return user.userrole.role
    except UserRole.DoesNotExist:
        return 'cashier'  # Default role

@login_required
def dashboard_home(request):
    """Main dashboard view"""
    user_role = get_user_role(request.user)
    
    # Get date range for filtering
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Basic stats
    stats = {
        'today': {
            'payments': PaymentRecord.objects.filter(created_at__date=today).count(),
            'successful': PaymentRecord.objects.filter(created_at__date=today, status='success').count(),
            'revenue': PaymentRecord.objects.filter(
                created_at__date=today, status='success'
            ).aggregate(total=Sum('amount'))['total'] or 0
        },
        'week': {
            'payments': PaymentRecord.objects.filter(created_at__date__gte=week_ago).count(),
            'successful': PaymentRecord.objects.filter(created_at__date__gte=week_ago, status='success').count(),
            'revenue': PaymentRecord.objects.filter(
                created_at__date__gte=week_ago, status='success'
            ).aggregate(total=Sum('amount'))['total'] or 0
        },
        'month': {
            'payments': PaymentRecord.objects.filter(created_at__date__gte=month_ago).count(),
            'successful': PaymentRecord.objects.filter(created_at__date__gte=month_ago, status='success').count(),
            'revenue': PaymentRecord.objects.filter(
                created_at__date__gte=month_ago, status='success'
            ).aggregate(total=Sum('amount'))['total'] or 0
        },
        'all_time': {
            'payments': PaymentRecord.objects.count(),
            'successful': PaymentRecord.objects.filter(status='success').count(),
            'revenue': PaymentRecord.objects.filter(status='success').aggregate(total=Sum('amount'))['total'] or 0
        }
    }
    
    # Recent payments
    recent_payments = PaymentRecord.objects.order_by('-created_at')[:10]
    
    # Daily stats for chart
    daily_stats = DailyStats.objects.filter(date__gte=week_ago).order_by('date')
    
    # Firebase sync status
    firebase_status = check_firebase_connection()
    
    context = {
        'title': 'Дашборд',
        'user_role': user_role,
        'stats': stats,
        'recent_payments': recent_payments,
        'daily_stats': daily_stats,
        'firebase_status': firebase_status,
    }
    
    return render(request, 'sales_dashboard/dashboard.html', context)

@login_required
def payment_list(request):
    """List all payments including OTP payments"""
    user_role = get_user_role(request.user)
    
    # Filter parameters
    status_filter = request.GET.get('status', 'all')
    date_filter = request.GET.get('date', 'all')
    payment_type_filter = request.GET.get('type', 'all')
    
    # Get regular payments
    payments = PaymentRecord.objects.all()
    
    # Get OTP payments and convert them to payment-like format
    otp_payments = []
    # Показываем ВСЕ OTP коды как платежи (не только использованные)
    otp_codes = OTPCode.objects.all().order_by('-created_at')
    
    # Debug: Log OTP codes found
    logger.info(f"Found {otp_codes.count()} OTP codes total")
    
    for otp in otp_codes:
        logger.info(f"Processing OTP: {otp.code}, amount: {otp.amount}, status: {otp.status}")
        
        # Определяем статус для отображения
        if otp.status == 'used':
            display_status = 'completed'
            status_badge = 'success'
        elif otp.status == 'active':
            display_status = 'pending'
            status_badge = 'warning'
        else:  # expired
            display_status = 'failed'
            status_badge = 'danger'
        
        otp_payments.append({
            'id': f'otp_{otp.id}',
            'order_id': f'OTP-{otp.code}',
            'amount': otp.amount,
            'currency': otp.currency,
            'status': display_status,
            'status_badge': status_badge,
            'payment_method': 'cash_otp',
            'description': f'Наличный платеж - {otp.quantity} билетов',
            'created_at': otp.created_at,
            'customer_name': f'OTP: {otp.code}',
            'quantity': otp.quantity,
            'is_otp': True,
            'otp_code': otp.code,
            'created_by': otp.created_by.username,
            'otp_status': otp.status
        })
    
    logger.info(f"Created {len(otp_payments)} OTP payment records")
    
    # Apply filters to regular payments
    if status_filter != 'all':
        payments = payments.filter(status=status_filter)
    
    if date_filter == 'today':
        payments = payments.filter(created_at__date=timezone.now().date())
        otp_payments = [p for p in otp_payments if p['created_at'].date() == timezone.now().date()]
    elif date_filter == 'week':
        week_ago = timezone.now().date() - timedelta(days=7)
        payments = payments.filter(created_at__date__gte=week_ago)
        otp_payments = [p for p in otp_payments if p['created_at'].date() >= week_ago]
    elif date_filter == 'month':
        month_ago = timezone.now().date() - timedelta(days=30)
        payments = payments.filter(created_at__date__gte=month_ago)
        otp_payments = [p for p in otp_payments if p['created_at'].date() >= month_ago]
    
    # Apply payment type filter
    if payment_type_filter == 'online':
        otp_payments = []
    elif payment_type_filter == 'cash':
        payments = PaymentRecord.objects.none()
    
    # Combine and sort all payments
    all_payments = []
    
    # Add regular payments
    for payment in payments:
        payment_dict = {
            'id': payment.id,
            'order_id': payment.order_id,
            'amount': payment.amount,
            'currency': payment.currency,
            'status': payment.status,
            'payment_method': payment.payment_method,
            'description': payment.description,
            'created_at': payment.created_at,
            'customer_name': payment.customer_name,
            'quantity': getattr(payment, 'quantity', 1),
            'is_otp': False,
            'created_by': getattr(payment, 'created_by', 'Unknown')
        }
        all_payments.append(payment_dict)
    
    # Add OTP payments
    all_payments.extend(otp_payments)
    
    # Sort by creation date (newest first)
    all_payments.sort(key=lambda x: x['created_at'], reverse=True)
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(all_payments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': 'Список платежей',
        'user_role': user_role,
        'page_obj': page_obj,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'payment_type_filter': payment_type_filter,
        'status_choices': PaymentRecord.STATUS_CHOICES,
        'payment_type_choices': [
            ('all', 'Все платежи'),
            ('online', 'Онлайн платежи'),
            ('cash', 'Наличные платежи (OTP)')
        ]
    }
    
    return render(request, 'sales_dashboard/payment_list.html', context)

@login_required
def statistics(request):
    """Detailed statistics view"""
    user_role = get_user_role(request.user)
    
    # Only admin can view detailed statistics
    if user_role != 'admin':
        return render(request, 'sales_dashboard/access_denied.html')
    
    # Get date range
    today = timezone.now().date()
    
    # Revenue by day (last 30 days)
    thirty_days_ago = today - timedelta(days=30)
    daily_revenue = []
    
    for i in range(30):
        date = thirty_days_ago + timedelta(days=i)
        revenue = PaymentRecord.objects.filter(
            created_at__date=date,
            status='success'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        daily_revenue.append({
            'date': date.strftime('%d.%m'),
            'revenue': revenue
        })
    
    # Payment status distribution
    status_stats = PaymentRecord.objects.values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    # Top subscription amounts
    amount_stats = PaymentRecord.objects.filter(status='success').values('amount').annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Monthly trends
    monthly_stats = []
    for i in range(12):
        month_start = today.replace(day=1) - timedelta(days=30*i)
        month_end = month_start.replace(day=28) + timedelta(days=4)
        month_end = month_end - timedelta(days=month_end.day)
        
        revenue = PaymentRecord.objects.filter(
            created_at__date__gte=month_start,
            created_at__date__lte=month_end,
            status='success'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        count = PaymentRecord.objects.filter(
            created_at__date__gte=month_start,
            created_at__date__lte=month_end,
            status='success'
        ).count()
        
        monthly_stats.append({
            'month': month_start.strftime('%m.%Y'),
            'revenue': revenue,
            'count': count
        })
    
    monthly_stats.reverse()
    
    # Prepare data for charts
    daily_labels = [item['date'] for item in daily_revenue]
    daily_values = [item['revenue'] for item in daily_revenue]
    
    # Get recent payments
    recent_payments = PaymentRecord.objects.select_related().order_by('-created_at')[:10]
    
    # Get top users (admin only)
    top_users = []
    if user_role == 'admin':
        from django.db.models import Count, Sum, Max
        top_users = PaymentRecord.objects.values('user_id').annotate(
            payment_count=Count('id'),
            total_amount=Sum('amount'),
            last_payment=Max('created_at')
        ).filter(
            user_id__isnull=False
        ).order_by('-total_amount')[:10]
    
    # Current time for display
    from datetime import datetime
    current_time = datetime.now()
    
    # Period from request
    period = request.GET.get('period', 'month')
    
    context = {
        'title': 'Статистика',
        'user_role': user_role,
        'period': period,
        'current_time': current_time,
        'stats': {
            'total_payments': status_stats.get('total', 0),
            'successful_payments': status_stats.get('success', 0),
            'pending_payments': status_stats.get('pending', 0),
            'failed_payments': status_stats.get('failed', 0),
            'total_revenue': amount_stats.get('total_revenue', 0),
            'top_users': top_users,
        },
        'daily_labels': daily_labels,
        'daily_revenue': daily_values,
        'recent_payments': recent_payments,
        'daily_revenue_data': daily_revenue,
        'status_stats': status_stats,
        'amount_stats': amount_stats,
        'monthly_stats': monthly_stats,
    }
    
    return render(request, 'sales_dashboard/statistics.html', context)

def check_firebase_connection():
    """Check Firebase connection status"""
    try:
        if not firebase_service.is_initialized():
            return {'status': 'warning', 'message': 'Firebase не настроен. Настройте ключи в .env файле'}
        
        # Try to get data from Firebase
        firebase_service.get_all_video_objects()
        return {'status': 'connected', 'message': 'Firebase подключен'}
    except Exception as e:
        logger.error(f"Firebase connection error: {str(e)}")
        return {'status': 'error', 'message': f'Ошибка подключения: {str(e)}'}

@login_required
def sync_payments(request):
    """Sync payments from Firebase"""
    user_role = get_user_role(request.user)
    
    if user_role != 'admin':
        return render(request, 'sales_dashboard/access_denied.html')
    
    try:
        # Get payment data from Firebase
        payment_data = firebase_service.get_payment_stats()
        
        synced_count = 0
        for payment_id, data in payment_data.items():
            payment, created = PaymentRecord.objects.get_or_create(
                order_id=payment_id,
                defaults={
                    'amount': data.get('amount', 0),
                    'currency': data.get('currency', 'UZS'),
                    'status': data.get('status', 'pending'),
                    'payment_id': data.get('payment_id', ''),
                    'description': data.get('description', ''),
                    'user_id': data.get('user_id', ''),
                    'user_info': data.get('user_info', {}),
                }
            )
            
            if created:
                synced_count += 1
        
        context = {
            'title': 'Синхронизация платежей',
            'synced_count': synced_count,
            'total_firebase': len(payment_data),
        }
        
    except Exception as e:
        logger.error(f"Payment sync error: {str(e)}")
        context = {
            'title': 'Синхронизация платежей',
            'error': str(e),
        }
    
    return render(request, 'sales_dashboard/sync_result.html', context)
