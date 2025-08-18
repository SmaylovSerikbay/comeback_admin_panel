"""
Views for Video Manager app - Firebase Compatible
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from firebase_service import firebase_service
from .forms import VideoObjectForm, CoordinatesForm
import logging

logger = logging.getLogger(__name__)

def is_admin(user):
    """Check if user is admin"""
    try:
        return user.userrole.role == 'admin'
    except:
        return user.is_superuser

def is_admin_or_cashier(user):
    """Check if user is admin or cashier"""
    try:
        return user.userrole.role in ['admin', 'cashier']
    except:
        return user.is_staff

@login_required
@user_passes_test(is_admin_or_cashier)
def video_list(request):
    """List all videos from Firebase"""
    
    # Get videos from Firebase
    firebase_objects = firebase_service.get_all_video_objects()
    
    # Convert to list format for template
    videos = []
    if firebase_objects:
        for firebase_id, data in firebase_objects.items():
            if data.get('objectType') == 'video':
                videos.append({
                    'id': firebase_id,
                    'name': data.get('name', 'Unnamed Video'),
                    'objectURL': data.get('objectURL', ''),
                    'x': data.get('x', 0),
                    'y': data.get('y', 0),
                    'objectType': data.get('objectType', 'video')
                })
    
    # Paginate results
    paginator = Paginator(videos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get user role
    try:
        user_role = request.user.userrole.role
    except:
        user_role = 'admin' if request.user.is_superuser else 'cashier'
    
    context = {
        'page_obj': page_obj,
        'title': 'Управление видео',
        'user_role': user_role,
        'total_videos': len(videos)
    }
    return render(request, 'video_manager/video_list.html', context)

@login_required
@user_passes_test(is_admin)
def video_create(request):
    """Create new video object"""
    if request.method == 'POST':
        form = VideoObjectForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Upload video to Firebase Storage
                video_file = form.cleaned_data['video_file']
                video_url = firebase_service.upload_video_to_storage(video_file)
                
                if not video_url:
                    messages.error(request, 'Ошибка загрузки видео в Firebase Storage')
                    return render(request, 'video_manager/video_form.html', {
                        'form': form,
                        'coordinates_form': CoordinatesForm(),
                        'title': 'Добавить видео',
                        'latlong_url': 'https://www.latlong.net/'
                    })
                
                # Prepare Firebase data
                firebase_data = {
                    'name': form.cleaned_data['name'],
                    'objectType': 'video',
                    'objectURL': video_url,
                    'x': form.cleaned_data['latitude'],
                    'y': form.cleaned_data['longitude']
                }
                
                # Add to Firebase
                firebase_id = firebase_service.add_video_object(firebase_data)
                
                if firebase_id:
                    messages.success(request, f'Видео "{firebase_data["name"]}" успешно добавлено!')
                    return redirect('videos:list')
                else:
                    messages.error(request, 'Ошибка добавления видео в Firebase')
                    
            except Exception as e:
                logger.error(f"Error creating video: {str(e)}")
                messages.error(request, f'Ошибка создания видео: {str(e)}')
    else:
        form = VideoObjectForm()
    
    coordinates_form = CoordinatesForm()
    
    context = {
        'form': form,
        'coordinates_form': coordinates_form,
        'title': 'Добавить видео',
        'latlong_url': 'https://www.latlong.net/'
    }
    return render(request, 'video_manager/video_form.html', context)

@login_required
@user_passes_test(is_admin)
def video_edit(request, video_id):
    """Edit video object"""
    
    # Get video from Firebase
    video_data = firebase_service.get_video_object(video_id)
    if not video_data:
        messages.error(request, 'Видео не найдено')
        return redirect('videos:list')
    
    if request.method == 'POST':
        form = VideoObjectForm(request.POST, request.FILES, is_edit=True)
        if form.is_valid():
            try:
                # Check if new video file uploaded
                video_file = form.cleaned_data.get('video_file')
                if video_file:
                    # Upload new video
                    video_url = firebase_service.upload_video_to_storage(video_file)
                    if not video_url:
                        messages.error(request, 'Ошибка загрузки нового видео')
                        return render(request, 'video_manager/video_form.html', {
                            'form': form,
                            'coordinates_form': CoordinatesForm(),
                            'title': f'Редактировать: {video_data.get("name", "Видео")}',
                            'video_id': video_id,
                            'is_edit': True
                        })
                else:
                    # Keep existing video URL
                    video_url = video_data.get('objectURL')
                
                # Prepare updated Firebase data
                updated_data = {
                    'name': form.cleaned_data['name'],
                    'objectType': 'video',
                    'objectURL': video_url,
                    'x': form.cleaned_data['latitude'],
                    'y': form.cleaned_data['longitude']
                }
                
                # Update in Firebase
                success = firebase_service.update_video_object(video_id, updated_data)
                
                if success:
                    messages.success(request, f'Видео "{updated_data["name"]}" успешно обновлено!')
                    return redirect('videos:list')
                else:
                    messages.error(request, 'Ошибка обновления видео в Firebase')
                    
            except Exception as e:
                logger.error(f"Error updating video: {str(e)}")
                messages.error(request, f'Ошибка обновления видео: {str(e)}')
    else:
        # Pre-fill form with existing data
        initial_data = {
            'name': video_data.get('name', ''),
            'latitude': video_data.get('x', 0),
            'longitude': video_data.get('y', 0)
        }
        form = VideoObjectForm(initial=initial_data, is_edit=True)
    
    context = {
        'form': form,
        'coordinates_form': CoordinatesForm(),
        'title': f'Редактировать: {video_data.get("name", "Видео")}',
        'video_id': video_id,
        'video_data': video_data,
        'is_edit': True
    }
    return render(request, 'video_manager/video_form.html', context)

@login_required
@user_passes_test(is_admin)
def video_delete(request, video_id):
    """Delete video object"""
    
    # Get video from Firebase
    video_data = firebase_service.get_video_object(video_id)
    if not video_data:
        messages.error(request, 'Видео не найдено')
        return redirect('videos:list')
    
    if request.method == 'POST':
        try:
            success = firebase_service.delete_video_object(video_id)
            
            if success:
                messages.success(request, f'Видео "{video_data.get("name", "")}" успешно удалено!')
            else:
                messages.error(request, 'Ошибка удаления видео из Firebase')
                
        except Exception as e:
            logger.error(f"Error deleting video: {str(e)}")
            messages.error(request, f'Ошибка удаления видео: {str(e)}')
    
    return redirect('videos:list')

def instructions(request):
    """Instructions page for adding videos and coordinates"""
    context = {
        'title': 'Инструкции по добавлению видео',
        'latlong_url': 'https://www.latlong.net/'
    }
    return render(request, 'video_manager/instructions.html', context)

@login_required
@user_passes_test(is_admin)
def clean_firebase_data(request):
    """Clean invalid Firebase data (admin only)"""
    if request.method == 'POST':
        try:
            # Get all objects from Firebase
            firebase_objects = firebase_service.get_all_video_objects()
            cleaned_count = 0
            
            if firebase_objects:
                for firebase_id, data in firebase_objects.items():
                    # Check if this is Django-created object with invalid structure
                    if (data.get('created_at') or data.get('created_by') or 
                        data.get('description') or data.get('title') or 
                        data.get('is_active') is not None):
                        
                        # This is Django-created object, delete it
                        firebase_service.delete_video_object(firebase_id)
                        cleaned_count += 1
                        logger.info(f"Cleaned invalid Firebase object: {firebase_id}")
            
            messages.success(request, f'Очищено {cleaned_count} некорректных записей из Firebase')
            
        except Exception as e:
            logger.error(f"Error cleaning Firebase data: {str(e)}")
            messages.error(request, f'Ошибка очистки данных: {str(e)}')
    
    return redirect('videos:list')