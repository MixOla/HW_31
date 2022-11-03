import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView

from HW_27.settings import TOTAL_ON_PAGE
from ads.models import Ad, Category
from users.models import User


def root(request):
    return JsonResponse({"status": "ok"})


from ads.models import Ad
from ads.serializers import AdSerializer, AdDetailSerializer
from rest_framework.viewsets import ModelViewSet


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.order_by('-price')
    default_serializer = AdSerializer
    serializer_classes = {
        "retrieve": AdDetailSerializer
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        categories = request.GET.getlist('cat')
        if categories:
            self.queryset = self.queryset.filter(
                category_id__in=categories
            )

        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(
                name__icontains=text)

        location = request.GET.get('location')
        if location:
            self.queryset = self.queryset.filter(
                author__location__name__icontains=location
            )

        price_from = request.GET.get('price_from', None)
        price_to = request.GET.get('price_to', None)
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        return super().list(self, request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImage(UpdateView):
    model = Ad
    fields = ['name']

    def post(self, request, *args, **kwargs):
        self.object = self.get()
        self.object.image = request.FILES.get('image')
        self.object.save()
        return JsonResponse({'id': self.object.pk,
                             'name': self.object.name,
                             'author': self.object.author.username,
                             'price': self.object.price,
                             'description': self.object.description,
                             'category': self.object.category.name,
                             'image': self.object.image.url if self.object.image else None,
                             'is_publised': self.object.is_published}, safe=False,
                            json_dumps_params={"ensure_ascii": False})
