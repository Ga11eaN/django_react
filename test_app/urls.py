from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register('api/test_app', views.ReactViewSet, 'form_test')
urlpatterns = router.urls