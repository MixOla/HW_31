import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from HW_27.settings import TOTAL_ON_PAGE
from users.models import User, Location


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.all().order_by('username')
        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page = request.GET.get('page')
        obj = paginator.get_page(page)

        response = {}
        items_list = [{'id': user.pk,
                       'username': user.username,
                       'first_name': user.first_name,
                       'last_name': user.last_name,
                       'role': user.role,
                       'age': user.age,
                       'location': list(map(str, user.location.all())),
                       'total_ads': user.ads.filter(is_published=True).count()
                       } for user in obj]
        response['items'] = items_list
        response['total'] = self.object_list.count()
        response['num_pages'] = paginator.num_pages

        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return JsonResponse({'id': user.pk,
                             'username': user.username,
                             'first_name': user.first_name,
                             'last_name': user.last_name,
                             'role': user.role,
                             'age': user.age,
                             'location': list(map(str, user.location.all())),
                             'total_ads': user.ads.filter(is_published=True).count()
                             }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['username']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if 'first_name' in data:
            self.object.name = data['first_name']
        if 'last_name' in data:
            self.object.price = data['last_name']
        if 'age' in data:
            self.object.description = data['age']
        if 'role' in data:
            self.object.is_published = data['role']
        if 'locations' in data:
            for loc_name in data['locations']:
                loc, _ = Location.objects.get_or_create(Name=loc_name)
                self.object.location.add(loc)

        return JsonResponse({'id': self.object.pk,
                             'username': self.object.username,
                             'first_name': self.object.first_name,
                             'last_name': self.object.last_name,
                             'role': self.object.role,
                             'age': self.object.age,
                             'location': list(map(str, self.object.location.all())),
                             }, safe=False,
                            json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['username']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = User.objects.create(username=data['username'],
                            first_name=data['first_name'],
                            last_name=data['last_name'],
                            role=data['role'],
                            age=data['age']
                            )

        if 'locations' in data:
            for loc_name in data['locations']:
                loc, _ = Location.objects.get_or_create(Name=loc_name)
                user.location.add(loc)

        return JsonResponse({'id': user.pk,
                             'username': user.username,
                             'first_name': user.first_name,
                             'last_name': user.last_name,
                             'role': user.role,
                             'age': user.age,
                             'location': list(map(str, user.location.all())),
                             }, safe=False,
                            json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, status=204)