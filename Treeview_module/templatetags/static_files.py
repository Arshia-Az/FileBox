from django import template
import os

register = template.Library()

# @register.simple_tag
# def get_static_files():

 
#     STATIC_ROOT = os.path.join('static')


#     files = []
#     file_name = [] 
#     root_name = []
#     for root, dirs, filenames in os.walk(STATIC_ROOT):
#         file_name.append(dirs)
#         root_name.append(root)
#         # files.append(file_name)
#         # print(root)
#         # print(dirs)
#         # print(filenames)
#         # for 
#         for filename in filenames:
#             files.append(os.path.relpath(os.path.join(root, filename), STATIC_ROOT))
            
                
#     # print(root_name)
#     return files
#     # return file_name
#     # return root_name



def get_folder_structure(path):
    folder_structure = {}
    
    for root, dirs, files in os.walk(path):
        folder_name = os.path.relpath(root, path)
        if folder_name == '.':
            folder_name = ''
        
        folder_structure[folder_name] = {
            'files': files,
            'subfolders': {}
        }
        
        for dir_name in dirs:
            subfolder_path = os.path.join(root, dir_name)
            folder_structure[folder_name]['subfolders'][dir_name] = get_folder_structure(subfolder_path)  # Recursively

    return folder_structure

@register.simple_tag
def get_static_folders():
    STATIC_ROOT = os.path.join('media')
    return get_folder_structure(STATIC_ROOT)