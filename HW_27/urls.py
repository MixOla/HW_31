
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from rest_framework import routers

from HW_27 import settings
from ads.views.ad import *
from users.urls import *
from ads.views.category import *

router = routers.SimpleRouter()
router.register('location', LocationViewSet)
router.register('ad', AdViewSet)
router.register('cat', CategoryViewSet)

urlpatterns = [
    path('', root),
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),
    path('ad/', include('ads.urls.ad')),
    path('user/', include('users.urls')),
    # path('cat/', include('ads.urls.category')),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
