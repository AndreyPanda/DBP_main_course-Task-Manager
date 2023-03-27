from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, TaskViewSet, TagViewSet
from .admin import task_manager_admin_site


router = routers.SimpleRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"tags", TagViewSet, basename="tags")

urlpatterns = [
    path("admin/", task_manager_admin_site.urls),
    path('api/', include(router.urls)),
]
