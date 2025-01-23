from django.shortcuts import render, redirect
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



# get folder from the media and show in template for show i use ajax 
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



# delete image only from media
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

# rename image from media
@csrf_exempt
def rename_file(request):
    if request.method == 'POST':
        old_name = request.POST.get('old_name')
        new_name = request.POST.get('new_name')
        base_path = r"C:\Users\User\Desktop\TreeView"
        name_url = request.POST.get('name_url')
        
        if not old_name or not new_name:
            return JsonResponse({'error': 'نام فایل یا نام جدید ارسال نشده است.'}, status=400)

 
        old_file_path = base_path + name_url
  
        if old_file_path.endswith(old_name):
            new_file_path = old_file_path.replace(old_name, new_name)

            if os.path.exists(old_file_path):
                try:
                    os.rename(old_file_path, new_file_path)
                    return JsonResponse({'message': 'نام فایل با موفقیت تغییر کرد.'})
                except Exception as e:
                    return JsonResponse({'error': f'خطا در تغییر نام فایل: {str(e)}'}, status=500)
            else:
                return JsonResponse({'error': 'فایل قدیمی وجود ندارد.'}, status=404)

    return JsonResponse({'error': 'درخواست نامعتبر است.'}, status=400)

def create_folder(request):
    if request.method == "POST":
        folder_name = request.POST.get('folder_name')  
        current_path = request.POST.get('path_folder')
    
        folder_path = os.path.join(settings.MEDIA_ROOT, current_path, folder_name)

        try:
            # ایجاد پوشه
            os.makedirs(folder_path, exist_ok=True)  
        except Exception as e:
            print(f"Error creating folder: {e}")

        # بازگشت به صفحه قبلی
        return redirect(request.META.get('HTTP_REFERER', '/'))



        