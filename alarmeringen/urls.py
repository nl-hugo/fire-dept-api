from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from alarmeringen import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'alarmeringen', views.AlarmeringViewSet)
router.register(r'capcodes', views.CapCodeViewSet)
router.register(r'regios', views.RegioViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
]
