from django.urls import path
from .views import SignUpView
from .views import upload_image, image_list, download_image,edit_image, save_edited_image
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
                  path('signup/', SignUpView.as_view(), name='signup'),
                  path('upload/', upload_image, name='upload_image'),
                    path('edit/<int:image_id>/', edit_image, name='edit_image'),
                  path('images/', image_list, name='image_list'),
                   path('download/<int:image_id>/', views.download_image, name='download_image'),
                  path('save_edited_image/', save_edited_image, name='save_edited_image')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
