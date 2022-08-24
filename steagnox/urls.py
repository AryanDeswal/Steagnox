from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("Home_Page.urls")),
    path('', include("Image_embed.urls")),
    path('', include("Image_extract.urls"))
]
