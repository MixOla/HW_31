import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, DeleteView, ListView, UpdateView, CreateView

from HW_27.settings import TOTAL_ON_PAGE
from ads.models import Ad, Category


def root(request):
    return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        search_text = request.GET.get("name", None)
        if search_text:
            self.object_list = self.object_list.filter(name=search_text)

        self.object_list = self.object_list.all().order_by("name")
        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        categories = []
        for category in page_obj:
            categories.append({
                "id": category.id,
                "name": category.name,
            })
        response = {
            "items": categories,
            "num_pages": paginator.num_pages,
        }

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()
        return JsonResponse({'id': cat.pk,
                             'name': cat.name},
                            safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if 'name' in data:
            self.object.name = data['name']
        self.object.save()

        return JsonResponse({'id': self.object.pk,
                             'name': self.object.name,
                             }, safe=False,
                            json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        cat = Category.objects.create(name=data['name'])
        return JsonResponse({'id': cat.pk,
                             'name': cat.name }, safe=False, json_dumps_params={"ensure_ascii": False})

