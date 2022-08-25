from django.urls import path
from Image_extract import views

urlpatterns = [ 
    path('extract_image', views.extract_image, name="extract_image")
]