from django.urls import path, include
from rest_framework import routers
from app.views import ArtistViewSet, WorkViewSet, UserViewSet, register


router = routers.DefaultRouter()
router.register(r'artists', ArtistViewSet)
router.register(r'works', WorkViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register, name='register'),
]
