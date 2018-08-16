from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from alarmeringen.urls import router as alarmeringen

router = DefaultRouter()
router.registry.extend(alarmeringen.registry)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
]
