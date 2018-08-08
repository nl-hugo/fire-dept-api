from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from alarmeringen.urls import router as alarmeringen
#from snippets.urls import router as snippets

router = DefaultRouter()
router.registry.extend(alarmeringen.registry)
#router.registry.extend(snippets.registry)

urlpatterns = [
    url(r'^', include(router.urls)),
#    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
]
