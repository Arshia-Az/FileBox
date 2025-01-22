from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name="home"),
    path('get-folder-files/', get_folder_files, name='get_folder_files'),
    path('delete-file/', delete_file, name='delete_file'),
    path('rename-file/', rename_file, name='rename_file'),
]
