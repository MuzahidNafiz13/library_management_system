from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from books.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('users/', include('users.urls')),
    path('books/', include('books.urls')),
] 
urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)