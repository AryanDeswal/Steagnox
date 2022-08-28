from django.urls import path
from Image_extract import views

urlpatterns = [ 
    path('extract_image', views.extract_image, name="extract_image"),
    path('download', views.download_fl, name='download_fl')
]