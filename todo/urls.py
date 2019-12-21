from django.urls import include, path
from django.conf.urls import url
from .views import main
from rest_framework import routers
from todo.views import main

router = routers.DefaultRouter()
router.register('list',main.ListView)
router.register('user-profiles',main.UserView)

urlpatterns = [
    path('',include(router.urls)),
    url(r'^register/$',
        main.UserRegistrationView.as_view(),
        name='register'),
    # url(r'^user-profile/$',
    #     main.UserView.as_view(),
    #     name='user_profile'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                main.UserEmailVerificationView.as_view(), name='activate'),
]