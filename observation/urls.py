from django.urls import path, include
from . import views

urlpatterns = [
    path('import_dataset/', views.import_dataset, name='import_dataset'),
    path('upload_csv/', views.upload_csv, name='upload_csv')
]