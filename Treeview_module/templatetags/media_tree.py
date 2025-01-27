# templatetags/media_tree.py
from django import template
from django.conf import settings
import os

register = template.Library()

def build_tree(directory):
    tree = []
    for entry in os.scandir(directory):
        print(f"Scanning: {entry.path}") 
        if entry.is_dir():
            tree.append({
                'name': entry.name,  
                'type': 'folder', 
                'path': entry.path, 
                'children': build_tree(entry.path),
            })
        elif entry.is_file() and entry.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            tree.append({
                'name': entry.name, 
                'type': 'image', 
                'path': entry.path, 
            })
    return tree

@register.simple_tag
def media_tree():
    media_root = settings.MEDIA_ROOT
    if not os.path.exists(media_root):
        return [] 
    return build_tree(media_root)
