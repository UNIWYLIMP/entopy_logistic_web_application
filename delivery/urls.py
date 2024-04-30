from mini import urls as miniUrls
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'mini.views.error_404'
handler505 = 'mini.views.error_505'
handler500 = 'mini.views.error_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(miniUrls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
