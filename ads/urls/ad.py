from django.urls import path

from ads.views.ad import *

urlpatterns = [
    path('<int:pk>/upload/', AdUploadImage.as_view(), name='ad-upload'),
]

