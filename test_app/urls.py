from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('file_upload', views.ExcelFileViewSet, 'file_upload')
router.register('sftp_upload', views.SftpViewSet, 'sftp_upload')
urlpatterns = router.urls
