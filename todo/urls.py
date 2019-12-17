from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('list',views.ListView)
router.register('user',views.UserView)

urlpatterns = [
    path('',include(router.urls))
]