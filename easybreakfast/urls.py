"""
URL configuration for EasyBreakfast project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Custom Admin branding
admin.site.site_header = "Easy Eats — Admin"
admin.site.site_title = "Easy Eats Admin Portal"
admin.site.index_title = "Recipe & Ingredient Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recommender.urls', namespace='recommender')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
