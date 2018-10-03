from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/MyDigitalHealth/')),
    path('MyDigitalHealth/', include('MyDigitalHealth.urls')),
    path('MyDigitalHealth/', include('cardsort.urls')),
]
