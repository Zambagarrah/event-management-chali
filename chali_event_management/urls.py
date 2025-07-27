from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse  # Optional fallback view

def fallback_home(request):
    return HttpResponse("<h1>Welcome to Chali Event Management</h1><p>This is a fallback homepage route.</p>")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('events.urls')),
]

# Fallback root view if events.urls doesn’t serve `/`
urlpatterns += [
    path('', fallback_home),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
