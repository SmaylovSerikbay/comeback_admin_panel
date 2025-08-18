"""
Views for subscription management
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from .models import SubscriptionSettings
from .forms import SubscriptionSettingsForm
from firebase_service import firebase_service
import logging

logger = logging.getLogger(__name__)

def is_admin(user):
    """Check if user is admin"""
    try:
        return user.userrole.role == 'admin'
    except:
        return user.is_superuser

@login_required
@user_passes_test(is_admin)
def subscription_settings(request):
    """Manage subscription settings"""
    
    settings = SubscriptionSettings.get_settings()
    
    if request.method == 'POST':
        form = SubscriptionSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            settings = form.save(commit=False)
            settings.updated_by = request.user.username
            settings.save()
            
            # Sync to Firebase
            try:
                firebase_data = settings.to_firebase_dict()
                success = firebase_service.update_subscription_settings(firebase_data)
                
                if success:
                    messages.success(request, 'Настройки подписки обновлены и синхронизированы с Firebase!')
                else:
                    messages.warning(request, 'Настройки сохранены, но не удалось синхронизировать с Firebase.')
            except Exception as e:
                logger.error(f"Firebase sync error: {str(e)}")
                messages.warning(request, f'Настройки сохранены, но произошла ошибка синхронизации с Firebase.')
            
            return redirect('subscription:settings')
    else:
        form = SubscriptionSettingsForm(instance=settings)
    
    context = {
        'form': form,
        'settings': settings,
        'title': 'Настройки подписки'
    }
    return render(request, 'subscription/settings.html', context)

@login_required
@user_passes_test(is_admin)
def sync_firebase(request):
    """Force sync subscription settings to Firebase"""
    
    if request.method == 'POST':
        try:
            settings = SubscriptionSettings.get_settings()
            firebase_data = settings.to_firebase_dict()
            success = firebase_service.update_subscription_settings(firebase_data)
            
            if success:
                messages.success(request, 'Настройки успешно синхронизированы с Firebase!')
            else:
                messages.error(request, 'Ошибка синхронизации с Firebase')
                
        except Exception as e:
            logger.error(f"Firebase sync error: {str(e)}")
            messages.error(request, f'Ошибка синхронизации: {str(e)}')
    
    return redirect('subscription:settings')

def api_subscription_settings(request):
    """API endpoint for getting current subscription settings"""
    
    try:
        settings = SubscriptionSettings.get_settings()
        return JsonResponse({
            'success': True,
            'data': settings.to_firebase_dict()
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
