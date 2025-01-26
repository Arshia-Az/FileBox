from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name="home"),
    path('get-folder-files/', get_folder_files, name='get_folder_files'),
    path('delete-file/', delete_file, name='delete_file'),
    path('rename-file/', rename_file, name='rename_file'),
    path('create_folder/', create_folder, name='create_folder'),
    path('delete_folder/', delete_folder, name='delete_folder'),
    path('upload_images/', upload_images, name='upload_images'),
    path('list_images/', list_images, name='list_images'),
    path('get-image-info/', get_image_info, name='get_image_info'),
    path('resize-image/', resize_image, name='resize_image'),
    

]
