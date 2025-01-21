from django.shortcuts import render
from django.http import JsonResponse
import os
# Create your views here.


def home(request):
    context = {

    }
    return render(request, 'home/index.html', context)




def get_folder_files(request):
    folder_path = request.GET.get('path')
    
    try:
        files = []
        
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                files.append({
                    'name': filename,
                    'url': f'/media/{filename}' if os.path.isfile(file_path) else None
                })
                print(files)
        return JsonResponse({'files': files})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
