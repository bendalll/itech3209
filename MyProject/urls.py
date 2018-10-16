from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('MyDigitalHealth/', include('MyDigitalHealth.urls')),
    path('', RedirectView.as_view(url='/MyDigitalHealth/')),  # just redirect everything to our app
]
#
# # Use static() to add url mapping to serve static files during development (only)
# from django.conf import settings
# from django.conf.urls.static import static
#
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

