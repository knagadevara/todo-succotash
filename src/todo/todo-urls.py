from django.conf.urls import include , url
from todo import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'todos' , views.ToDoViewSet)

urlpatterns = [
    url(r'^' , include(router.urls)),
]
