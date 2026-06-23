"""
URL configuration for config project.
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('django-admin/', admin.site.urls),  # Admin Django déplacé ici
    path('api/', include('api.urls')),

    # Page d'accueil → acceuil.html
    path('', lambda request: serve(request, 'acceuil.html', document_root=settings.BASE_DIR.parent)),

    # Tous les autres fichiers frontend (css, js, pages/, admin/, images/)
    re_path(r'^(?P<path>.*)$', lambda request, path: serve(request, path, document_root=settings.BASE_DIR.parent)),
]
