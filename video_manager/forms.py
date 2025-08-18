"""
Forms for Video Manager app - Firebase Compatible
"""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, HTML

class VideoObjectForm(forms.Form):
    """Form for creating/editing video objects - Firebase compatible structure"""
    
    name = forms.CharField(
        label='Название видео',
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Введите название видео'})
    )
    
    latitude = forms.FloatField(
        label='Широта (Latitude)',
        widget=forms.NumberInput(attrs={
            'placeholder': 'Например: 41.2995',
            'step': 'any'
        })
    )
    
    longitude = forms.FloatField(
        label='Долгота (Longitude)', 
        widget=forms.NumberInput(attrs={
            'placeholder': 'Например: 69.2401',
            'step': 'any'
        })
    )
    
    video_file = forms.FileField(
        label='Видео файл',
        required=False,  # Made optional for editing
        widget=forms.FileInput(attrs={
            'accept': 'video/mp4',  # Only MP4
            'class': 'form-control'
        }),
        help_text='Только MP4 H.264 формат. При редактировании - необязательно (оставьте пустым для сохранения текущего видео)'
    )
    
    def __init__(self, *args, **kwargs):
        self.is_edit = kwargs.pop('is_edit', False)
        super().__init__(*args, **kwargs)
        
        # Make video_file required only for new videos
        if not self.is_edit:
            self.fields['video_file'].required = True
            self.fields['video_file'].help_text = 'Только MP4 H.264 формат. Видео будет загружено в Firebase Storage'
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        
        self.helper.layout = Layout(
            Fieldset(
                'Основная информация',
                'name',
                css_class='mb-4'
            ),
            Fieldset(
                'GPS координаты',
                HTML('''
                    <div class="alert alert-info">
                        <strong>Как получить координаты:</strong><br>
                        1. Перейдите на сайт <a href="https://www.latlong.net/" target="_blank" class="alert-link">LatLong.net</a><br>
                        2. Введите адрес или название места<br>
                        3. Скопируйте координаты Latitude (широта) и Longitude (долгота)
                    </div>
                '''),
                Row(
                    Column('latitude', css_class='form-group col-md-6 mb-0'),
                    Column('longitude', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                css_class='mb-4'
            ),
            Fieldset(
                'Видео файл',
                HTML('''
                    <div class="alert alert-success">
                        <strong>Firebase Storage:</strong><br>
                        • Видео будет загружено в Firebase Storage<br>
                        • Unity приложение получит прямую ссылку на видео<br>
                        • Только MP4 H.264 формат, размер до 5MB
                    </div>
                    <div class="alert alert-warning">
                        <strong>Хромакей (зеленый экран):</strong><br>
                        • Используйте цвет <code style="background-color: #00b23f; color: white; padding: 1px 4px; border-radius: 2px;">#00b23f</code> для фона<br>
                        • Unity автоматически сделает этот цвет прозрачным<br>
                        • Избегайте зеленых оттенков в одежде
                    </div>
                '''),
                'video_file',
                css_class='mb-4'
            ),
            Submit('submit', 'Сохранить видео', css_class='btn btn-primary btn-lg')
        )
    
    def clean_video_file(self):
        video_file = self.cleaned_data.get('video_file')
        
        if video_file:
            # Check file size (max 5MB)
            if video_file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Размер файла не должен превышать 5MB')
            
            # Check file type - only MP4
            if video_file.content_type != 'video/mp4':
                raise forms.ValidationError('Поддерживается только MP4 формат с кодеком H.264')
            
            # Check file extension
            if not video_file.name.lower().endswith('.mp4'):
                raise forms.ValidationError('Файл должен иметь расширение .mp4')
        
        return video_file
    
    def clean(self):
        cleaned_data = super().clean()
        video_file = cleaned_data.get('video_file')
        
        # For new videos, video file is required
        if not self.is_edit and not video_file:
            raise forms.ValidationError('Для нового видео необходимо загрузить MP4 файл')
        
        return cleaned_data


class CoordinatesForm(forms.Form):
    """Form for getting coordinates from address"""
    
    address = forms.CharField(
        label='Адрес или название места',
        max_length=500,
        widget=forms.TextInput(attrs={
            'placeholder': 'Например: Ташкент, Узбекистан или Amir Temur Square',
            'class': 'form-control'
        }),
        help_text='Введите адрес, и мы поможем найти координаты'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'form-inline mb-4'
        self.helper.layout = Layout(
            Row(
                Column('address', css_class='form-group col-md-8 mb-0'),
                Column(
                    Submit('search', 'Найти координаты', css_class='btn btn-info'),
                    css_class='form-group col-md-4 mb-0'
                ),
                css_class='form-row align-items-end'
            )
        )