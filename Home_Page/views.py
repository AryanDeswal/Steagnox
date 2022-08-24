from django.shortcuts import render


def homepage(request):
    return render(request, "index.html" )

def signin(request):
    return render(request, "signin.html")

def signup(request):
    return render(request, "signup.html")

def embed_image(request):
    return render(request, "embed_image.html")

def embed_video(request):
    return render(request, "embed_video.html")

def extract_image(request):
    return render(request, "extract_image.html")

def extract_video(request):
    return render(request, "extract_video.html")