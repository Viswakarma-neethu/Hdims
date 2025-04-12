# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('hospital.urls')),  # ✅ This connects `hospital/urls.py`
# ]


from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hospital.urls')),

    # Favicon Fix
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.png', permanent=True)),
]

# Static File Handling in Development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
