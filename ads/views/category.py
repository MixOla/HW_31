
from django.http import JsonResponse

from ads.models import Category
from ads.serializers import CategorySerializer


def root(request):
    return JsonResponse({"status": "ok"})

from rest_framework.viewsets import ModelViewSet

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

