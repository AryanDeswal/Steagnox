from django.shortcuts import render


def extract_image(request):
    return render(request, "extract_image.html" )

