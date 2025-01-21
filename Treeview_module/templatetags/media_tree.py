from django import template
from django.conf import settings
import os

register = template.Library()

def build_tree(directory):
    tree = []
    for entry in os.scandir(directory):
        if entry.is_dir():
          
            tree.append({
                'name': entry.name,
                'type': 'folder',
                'children': build_tree(entry.path),
            })
        elif entry.is_file():
      
            tree.append({
                'name': entry.name,
                'type': 'file',
            })
    return tree

@register.simple_tag
def media_tree():

    media_root = settings.MEDIA_ROOT
    if not os.path.exists(media_root):
        return [] 
    return build_tree(media_root)
