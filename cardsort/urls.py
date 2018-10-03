from django.urls import path
from . import views

urlpatterns = [
    path('create_package', views.create_package, name='create_package'),
    path('administration', views.package_administration, name='administration'),
    path('edit_package/<package_id>/', views.edit_package, name='edit_package'),
    path('package_open/<package_id>/', views.package_open, name='package_open'),
    path('assign/<base_package_id>/', views.assign_choose_user, name="assign"),
    path('assign_to/<base_package_id>/<user_id>/', views.assign_package_to_user, name='assign_to'),
    path('delete/<package_id>/', views.delete_package, name='delete'),
    path('save/<package_id>/', views.activity_save, name='save'),
    path('css/<package_id>', views.get_css, name='css'),
]