from django.urls import path
from Image_embed import views

urlpatterns = [ 
    path('embed_image', views.embed_image, name="embed_image")
]