from django.shortcuts import render
from django.http import JsonResponse
import os
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
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


@csrf_exempt
def delete_file(request):
    if request.method == 'POST':
        base_path = r"C:\Users\User\Desktop\TreeView"
        
        fileUrl = request.POST.get('fileUrl')

        if not fileUrl:
            return JsonResponse({'error': 'نام فایل ارسال نشده است.'}, status=400)


        file_path = base_path + fileUrl
        # بررسی وجود فایل
        if os.path.exists(file_path):
            try:
                os.remove(file_path)  # حذف فایل
                return JsonResponse({'message': 'فایل با موفقیت حذف شد.'})
            except Exception as e:
                return JsonResponse({'error': f'خطا در حذف فایل: {str(e)}'}, status=500)
        else:
            return JsonResponse({'error': 'فایل وجود ندارد.'}, status=404)

    return JsonResponse({'error': 'درخواست نامعتبر است.'}, status=400)
