from django.shortcuts import render


def embed_image(request):
    return render(request, "embed_image.html" )

