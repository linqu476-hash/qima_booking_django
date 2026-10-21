from django.urls import path
from . import views
urlpatterns=[path('',views.dashboard,name='dashboard'),path('runs/new/',views.new_run,name='new_run'),path('runs/<int:pk>/',views.run_detail,name='run_detail'),path('runs/<int:pk>/file/<path:relative_path>/',views.run_file,name='run_file')]
