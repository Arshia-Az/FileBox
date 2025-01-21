from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name="home"),
    path('get-folder-files/', get_folder_files, name='get_folder_files'),
]
