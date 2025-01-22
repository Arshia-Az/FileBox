from django.shortcuts import render
from django.http import JsonResponse
import os
from .models import Profile
# Create your views here.


def home(request):
    context = {

    }
    return render(request, 'home/index.html', context)




def get_folder_files(request):
    folder_path = request.GET.get('path')
    base_path = r"C:\Users\User\Desktop\TreeView\media"
    print(base_path)
    try:
        files = []
        
        for filename in os.listdir(folder_path):
            
            
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                relative_path = os.path.relpath(folder_path, base_path)
                files.append({
                    'name': filename,
                    'url': f'/media/{relative_path}/{filename}'
                })
                
        return JsonResponse({'files': files})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
