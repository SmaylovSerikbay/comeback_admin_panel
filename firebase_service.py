"""
Firebase service for ComeBack Admin Panel
Handles all Firebase operations including authentication and database management
"""

import firebase_admin
from firebase_admin import credentials, db, storage
from django.conf import settings
import logging
import uuid
from datetime import datetime, timedelta
import os

logger = logging.getLogger(__name__)

class FirebaseService:
    """Service class for Firebase operations"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.initialize_firebase()
            self._initialized = True
    
    def initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            if not firebase_admin._apps:
                # Check if Firebase config is properly set
                firebase_config = settings.FIREBASE_CONFIG
                
                # Skip Firebase initialization if no proper config
                if not firebase_config.get('private_key') or firebase_config.get('private_key') == '':
                    logger.warning("Firebase credentials not configured. Skipping Firebase initialization.")
                    logger.warning("Please set up your Firebase credentials in .env file")
                    return
                
                # Create credentials from settings
                cred = credentials.Certificate(firebase_config)
                
                firebase_admin.initialize_app(cred, {
                    'databaseURL': settings.FIREBASE_DATABASE_URL,
                    'storageBucket': settings.FIREBASE_STORAGE_BUCKET
                })
                logger.info("Firebase initialized successfully")
            else:
                logger.info("Firebase already initialized")
                
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {str(e)}")
            logger.warning("Running without Firebase integration. Please configure Firebase credentials.")
            # Don't raise exception - allow Django to start without Firebase
    
    def is_initialized(self):
        """Check if Firebase is properly initialized"""
        return len(firebase_admin._apps) > 0
    
    def get_database_ref(self, path=''):
        """Get Firebase database reference"""
        try:
            if not self.is_initialized():
                logger.warning("Firebase not initialized. Cannot get database reference.")
                return None
            return db.reference(path)
        except Exception as e:
            logger.error(f"Failed to get database reference: {str(e)}")
            return None
    
    def add_video_object(self, video_data):
        """
        Add video object to Firebase Realtime Database
        Uses Unity-compatible structure: name, objectType, objectURL, x, y
        
        Args:
            video_data (dict): Video object data with fields:
                - name: video name/title
                - objectType: 'video' 
                - objectURL: Firebase Storage URL
                - x: latitude
                - y: longitude
        """
        try:
            if not self.is_initialized():
                logger.warning("Firebase not initialized. Cannot add video object.")
                return None
                
            ref = self.get_database_ref('objects')
            if ref is None:
                return None
            
            # Create clean structure compatible with Unity
            clean_data = {
                'name': video_data.get('name', video_data.get('title', 'Unnamed Video')),
                'objectType': 'video',
                'objectURL': video_data.get('objectURL'),
                'x': float(video_data.get('x', 0)),
                'y': float(video_data.get('y', 0))
            }
            
            # Generate new Firebase key
            new_ref = ref.push(clean_data)
            logger.info(f"Video object {new_ref.key} added to Firebase successfully")
            return new_ref.key
            
        except Exception as e:
            logger.error(f"Failed to add video object: {str(e)}")
            return None
    
    def upload_video_to_storage(self, video_file, filename=None):
        """
        Upload video file to Firebase Storage
        
        Args:
            video_file: Django UploadedFile object
            filename: Optional custom filename
            
        Returns:
            str: Firebase Storage download URL or None if failed
        """
        try:
            if not self.is_initialized():
                logger.warning("Firebase not initialized. Cannot upload video.")
                return None
            
            # Get Firebase Storage bucket
            bucket = storage.bucket()
            
            # Generate unique filename if not provided
            if not filename:
                file_extension = os.path.splitext(video_file.name)[1]
                filename = f"videos/{uuid.uuid4().hex}{file_extension}"
            else:
                filename = f"videos/{filename}"
            
            # Create blob and upload
            blob = bucket.blob(filename)
            
            # Set content type
            content_type = video_file.content_type or 'video/mp4'
            blob.content_type = content_type
            
            # Upload file
            video_file.seek(0)  # Reset file pointer
            blob.upload_from_file(video_file)
            
            # Make the blob publicly accessible
            blob.make_public()
            
            # Get download URL
            download_url = blob.public_url
            
            logger.info(f"Video uploaded to Firebase Storage: {filename}")
            return download_url
            
        except Exception as e:
            logger.error(f"Failed to upload video to Firebase Storage: {str(e)}")
            return None
    
    def update_video_object(self, video_id, video_data):
        """Update video object in Firebase with clean structure"""
        try:
            if not self.is_initialized():
                logger.warning("Firebase not initialized. Cannot update video object.")
                return False
                
            ref = self.get_database_ref(f'objects/{video_id}')
            if ref is None:
                return False
            
            # Create clean structure compatible with Unity
            clean_data = {
                'name': video_data.get('name', video_data.get('title', 'Unnamed Video')),
                'objectType': 'video',
                'objectURL': video_data.get('objectURL'),
                'x': float(video_data.get('x', 0)),
                'y': float(video_data.get('y', 0))
            }
                
            ref.set(clean_data)  # Use set instead of update to replace completely
            logger.info(f"Video object {video_id} updated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update video object: {str(e)}")
            return False
    
    def delete_video_object(self, video_id):
        """Delete video object from Firebase"""
        try:
            if not self.is_initialized():
                logger.warning("Firebase not initialized. Cannot delete video object.")
                return False
                
            ref = self.get_database_ref(f'objects/{video_id}')
            if ref is None:
                return False
                
            ref.delete()
            logger.info(f"Video object {video_id} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete video object: {str(e)}")
            return False
    
    def get_all_video_objects(self):
        """Get all video objects from Firebase"""
        try:
            if not self.is_initialized():
                logger.warning("Firebase not initialized. Cannot get video objects.")
                return {}
                
            ref = self.get_database_ref('objects')
            if ref is None:
                return {}
                
            data = ref.get()
            
            if data:
                # Filter only video objects
                video_objects = {k: v for k, v in data.items() 
                               if isinstance(v, dict) and v.get('objectType') == 'video'}
                return video_objects
            else:
                return {}
                
        except Exception as e:
            logger.error(f"Failed to get video objects: {str(e)}")
            return {}
    
    def get_video_object(self, video_id):
        """Get specific video object from Firebase"""
        try:
            if not self.is_initialized():
                logger.warning("Firebase not initialized. Cannot get video object.")
                return None
                
            ref = self.get_database_ref(f'objects/{video_id}')
            if ref is None:
                return None
                
            data = ref.get()
            return data
            
        except Exception as e:
            logger.error(f"Failed to get video object {video_id}: {str(e)}")
            return None
    
    def get_payment_stats(self):
        """Get payment statistics from Firebase (if stored there)"""
        try:
            if not self.is_initialized():
                logger.warning("Firebase not initialized. Cannot get payment stats.")
                return {}
                
            ref = self.get_database_ref('payments')
            if ref is None:
                return {}
                
            data = ref.get()
            
            if data:
                return data
            else:
                return {}
                
        except Exception as e:
            logger.error(f"Failed to get payment stats: {str(e)}")
            return {}
    
    def add_payment_record(self, payment_data):
        """Add payment record to Firebase"""
        try:
            if not self.is_initialized():
                logger.warning("Firebase not initialized. Cannot add payment record.")
                return False
                
            ref = self.get_database_ref('payments')
            if ref is None:
                return False
                
            payment_id = payment_data.get('order_id')
            ref.child(payment_id).set(payment_data)
            logger.info(f"Payment record {payment_id} added successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add payment record: {str(e)}")
            return False
    
    def update_subscription_settings(self, settings_data):
        """
        Update subscription settings in Firebase for Unity app
        
        Args:
            settings_data (dict): Subscription settings with fields:
                - price: subscription price
                - duration_minutes: access duration in minutes
                - currency: currency code (UZS, USD, etc.)
                - is_active: whether subscription system is active
        """
        try:
            if not self.is_initialized():
                logger.warning("Firebase not initialized. Cannot update subscription settings.")
                return False
                
            ref = self.get_database_ref('subscription_settings')
            if ref is None:
                return False
            
            # Ensure data is properly formatted for Unity
            clean_data = {
                'price': float(settings_data.get('price', 0)),
                'duration_minutes': int(settings_data.get('duration_minutes', 30)),
                'currency': str(settings_data.get('currency', 'UZS')),
                'is_active': bool(settings_data.get('is_active', True)),
                'updated_at': settings_data.get('updated_at')
            }
            
            ref.set(clean_data)
            logger.info("Subscription settings updated in Firebase successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update subscription settings: {str(e)}")
            return False
    
    def get_subscription_settings(self):
        """Get current subscription settings from Firebase"""
        try:
            if not self.is_initialized():
                logger.warning("Firebase not initialized. Cannot get subscription settings.")
                return None
                
            ref = self.get_database_ref('subscription_settings')
            if ref is None:
                return None
                
            settings = ref.get()
            logger.info("Subscription settings retrieved from Firebase successfully")
            return settings
            
        except Exception as e:
            logger.error(f"Failed to get subscription settings: {str(e)}")
            return None
    
    def add_otp_code(self, otp_code):
        """
        Add OTP code to Firebase for Unity app activation
        
        Args:
            otp_code: OTPCode model instance
            
        Returns:
            str: Firebase key of the created OTP code
        """
        try:
            if not self.is_initialized():
                logger.warning("Firebase not initialized. Cannot add OTP code.")
                return None
                
            ref = self.get_database_ref('activation_codes')
            if ref is None:
                return None
            
            # Create clean structure for Unity
            clean_data = {
                'code': otp_code.code,
                'amount': float(otp_code.amount),
                'quantity': int(otp_code.quantity),
                'currency': str(otp_code.currency),
                'status': 'active',
                'created_at': otp_code.created_at.isoformat(),
                'created_by': otp_code.created_by.username,
                'django_id': str(otp_code.id)
            }
            
            # Push to Firebase and get the key
            new_ref = ref.push(clean_data)
            logger.info(f"OTP code {otp_code.code} added to Firebase successfully")
            
            # Также добавляем в список платежей для учета
            self.add_otp_payment_record(otp_code)
            
            return new_ref.key
            
        except Exception as e:
            logger.error(f"Failed to add OTP code: {str(e)}")
            return None
    
    def add_otp_payment_record(self, otp_code):
        """Add OTP payment record to Firebase payments list"""
        try:
            if not self.is_initialized():
                logger.warning("Firebase not initialized. Cannot add OTP payment record.")
                return False
                
            ref = self.get_database_ref('payments')
            if ref is None:
                return False
            
            # Создаем запись о платеже
            payment_data = {
                'order_id': f'otp_{otp_code.code}_{otp_code.id}',
                'amount': float(otp_code.amount),
                'currency': str(otp_code.currency),
                'status': 'completed',
                'payment_method': 'cash_otp',
                'description': f'Наличный платеж - {otp_code.quantity} билетов',
                'created_at': otp_code.created_at.isoformat(),
                'customer_name': f'OTP: {otp_code.code}',
                'quantity': int(otp_code.quantity),
                'otp_code': otp_code.code,
                'created_by': otp_code.created_by.username,
                'django_id': str(otp_code.id)
            }
            
            # Добавляем в Firebase
            ref.child(payment_data['order_id']).set(payment_data)
            logger.info(f"OTP payment record {payment_data['order_id']} added successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add OTP payment record: {str(e)}")
            return False
    
    def verify_otp_code(self, otp_code, device_id):
        """
        Verify OTP code in Firebase and mark as used if valid
        
        Args:
            otp_code (str): 6-digit OTP code
            device_id (str): Unique device identifier
            
        Returns:
            dict: Result with success status and details
        """
        try:
            if not self.is_initialized():
                logger.warning("Firebase not initialized. Cannot verify OTP code.")
                return {'success': False, 'error': 'Firebase not initialized'}
                
            ref = self.get_database_ref('activation_codes')
            if ref is None:
                return {'success': False, 'error': 'Cannot access Firebase'}
            
            # Search for the OTP code
            query = ref.order_by_child('code').equal_to(otp_code)
            result = query.get()
            
            if not result:
                return {'success': False, 'error': 'OTP code not found'}
            
            # Get the first (and should be only) result
            firebase_key = list(result.keys())[0]
            code_data = result[firebase_key]
            
            # Check if code is active
            if code_data.get('status') != 'active':
                return {'success': False, 'error': 'OTP code already used or expired'}
            
            # Check if code is expired (24 hours)
            created_at_str = code_data.get('created_at')
            if created_at_str:
                from datetime import datetime, timezone
                try:
                    created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
                    if datetime.now(timezone.utc) - created_at > timedelta(hours=24):
                        return {'success': False, 'error': 'OTP code expired'}
                except:
                    pass
            
            # Mark code as used
            updates = {
                'status': 'used',
                'used_at': datetime.now().isoformat(),
                'device_id': device_id
            }
            
            ref.child(firebase_key).update(updates)
            
            # Return success with activation details
            return {
                'success': True,
                'amount': code_data.get('amount'),
                'quantity': code_data.get('quantity'),
                'currency': code_data.get('currency'),
                'firebase_key': firebase_key,
                'message': 'OTP code verified successfully'
            }
            
        except Exception as e:
            logger.error(f"Failed to verify OTP code: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_otp_codes(self):
        """Get all OTP codes from Firebase"""
        try:
            if not self.is_initialized():
                logger.warning("Firebase not initialized. Cannot get OTP codes.")
                return {}
                
            ref = self.get_database_ref('activation_codes')
            if ref is None:
                return {}
                
            codes = ref.get()
            logger.info("OTP codes retrieved from Firebase successfully")
            return codes if codes else {}
            
        except Exception as e:
            logger.error(f"Failed to get OTP codes: {str(e)}")
            return {}

# Singleton instance
firebase_service = FirebaseService()
