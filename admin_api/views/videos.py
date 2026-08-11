import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from firebase_service import firebase_service
from admin_api.permissions import IsAdminOrCashier, IsAdmin, get_user_role

logger = logging.getLogger(__name__)


class VideoListView(APIView):
    permission_classes = [IsAdminOrCashier]

    def get(self, request):
        firebase_objects = firebase_service.get_all_video_objects()
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
                        'objectType': data.get('objectType', 'video'),
                    })
        return Response({
            'videos': videos,
            'total': len(videos),
            'user_role': get_user_role(request.user),
        })


class VideoCreateView(APIView):
    permission_classes = [IsAdmin]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        name = request.data.get('name') or request.POST.get('name')
        try:
            latitude = float(request.data.get('latitude', 0) or request.POST.get('latitude', 0))
            longitude = float(request.data.get('longitude', 0) or request.POST.get('longitude', 0))
        except (TypeError, ValueError):
            return Response(
                {'error': 'Широта и долгота должны быть числами'},
                status=status.HTTP_400_BAD_REQUEST
            )
        video_file = request.FILES.get('video_file')
        if not video_file:
            return Response(
                {'error': 'Необходимо загрузить видео файл'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not name:
            return Response(
                {'error': 'Укажите название видео'},
                status=status.HTTP_400_BAD_REQUEST
            )
        video_url = firebase_service.upload_video_to_storage(video_file)
        if not video_url:
            return Response(
                {'error': 'Ошибка загрузки видео в Firebase Storage'},
                status=status.HTTP_502_BAD_GATEWAY
            )
        firebase_data = {
            'name': name,
            'objectType': 'video',
            'objectURL': video_url,
            'x': latitude,
            'y': longitude,
        }
        firebase_id = firebase_service.add_video_object(firebase_data)
        if not firebase_id:
            return Response(
                {'error': 'Ошибка добавления видео в Firebase'},
                status=status.HTTP_502_BAD_GATEWAY
            )
        return Response({
            'id': firebase_id,
            'name': name,
            'objectURL': video_url,
            'x': latitude,
            'y': longitude,
        }, status=status.HTTP_201_CREATED)


class VideoDetailView(APIView):
    permission_classes = [IsAdmin]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, video_id):
        data = firebase_service.get_video_object(video_id)
        if not data:
            return Response({'error': 'Видео не найдено'}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'id': video_id,
            'name': data.get('name', ''),
            'objectURL': data.get('objectURL', ''),
            'x': data.get('x', 0),
            'y': data.get('y', 0),
        })

    def put(self, request, video_id):
        data = firebase_service.get_video_object(video_id)
        if not data:
            return Response({'error': 'Видео не найдено'}, status=status.HTTP_404_NOT_FOUND)
        name = request.data.get('name', data.get('name'))
        latitude = request.data.get('latitude', data.get('x'))
        longitude = request.data.get('longitude', data.get('y'))
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (TypeError, ValueError):
            return Response(
                {'error': 'Широта и долгота должны быть числами'},
                status=status.HTTP_400_BAD_REQUEST
            )
        video_url = data.get('objectURL')
        if request.FILES.get('video_file'):
            video_file = request.FILES['video_file']
            new_url = firebase_service.upload_video_to_storage(video_file)
            if new_url:
                video_url = new_url
        updated = {
            'name': name,
            'objectType': 'video',
            'objectURL': video_url,
            'x': latitude,
            'y': longitude,
        }
        success = firebase_service.update_video_object(video_id, updated)
        if not success:
            return Response({'error': 'Ошибка обновления'}, status=status.HTTP_502_BAD_GATEWAY)
        return Response({'id': video_id, **updated})


class VideoDeleteView(APIView):
    permission_classes = [IsAdmin]

    def delete(self, request, video_id):
        data = firebase_service.get_video_object(video_id)
        if not data:
            return Response({'error': 'Видео не найдено'}, status=status.HTTP_404_NOT_FOUND)
        success = firebase_service.delete_video_object(video_id)
        if not success:
            return Response({'error': 'Ошибка удаления'}, status=status.HTTP_502_BAD_GATEWAY)
        return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
