from django.urls import path
from . import views

urlpatterns = [ 
    path('',views.homepage, name="homepage"),
    path('signin',views.signin, name="signin"),
    path('signup',views.signup, name="signup"),
    # path('signout',views.signout, name="signout"),
    path('embed_image',views.embed_image, name="embed_image"),
    path('embed_video',views.embed_video, name="embed_video"),
    path('extract_image',views.extract_image, name="extract_image"),
    path('extract_video',views.extract_video, name="extract_video")
]
