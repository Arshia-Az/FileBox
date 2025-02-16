from django.shortcuts import render, redirect
from django.http import JsonResponse
import os
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import requests
from io import BytesIO
import base64
from django.core.files.base import ContentFile


def home(request):
    context = {
    }
    return render(request, 'home/index.html', context)


# get folder from the media and show in template for show i use ajax 
def get_folder_files(request):
    folder_path = request.GET.get('path')
    base_path = r"C:\Users\User\Desktop\TreeView\media"
    print(base_path)
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
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



def delete_folder(request):
    if request.method == "POST":
        folder_path = request.POST.get("folder_path")
        try:
            # مسیر کامل پوشه
            full_path = os.path.join(settings.MEDIA_ROOT, folder_path)

            if os.path.exists(full_path) and os.path.isdir(full_path):
                # حذف تمام فایل‌ها و زیرفولدرها
                for root, dirs, files in os.walk(full_path, topdown=False):
                    for file in files:
                        os.remove(os.path.join(root, file))
                    for dir in dirs:
                        os.rmdir(os.path.join(root, dir))
                
                # حذف پوشه اصلی
                os.rmdir(full_path)

                return JsonResponse({"status": "success", "message": "Folder and its contents deleted successfully."})
            else:
                return JsonResponse({"status": "error", "message": "Folder does not exist."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Error deleting folder: {str(e)}"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."})


@csrf_exempt
def upload_images(request):
    if request.method == "POST":
        folder_path = request.POST.get("folder_path")  # مسیر پوشه
        images = request.FILES.getlist("images")  # گرفتن لیست فایل‌های تصویر

        if not folder_path or not images:
            return JsonResponse({"error": "Invalid folder path or no images provided"}, status=400)

        # ایجاد مسیر پوشه در صورت وجود نداشتن
        folder_full_path = os.path.join(settings.MEDIA_ROOT, folder_path)
        os.makedirs(folder_full_path, exist_ok=True)

        uploaded_files = []
        try:
            for image in images:
                save_path = os.path.join(folder_full_path, image.name)
                with open(save_path, "wb") as f:
                    for chunk in image.chunks():
                        f.write(chunk)
                uploaded_files.append(image.name)

            return JsonResponse({"message": "Images uploaded successfully!", "files": uploaded_files})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

# show the image when clicl on folder
def list_images(request):
    folder_path = request.GET.get("folder_path")  # مسیر پوشه انتخاب‌شده

    if not folder_path:
        return JsonResponse({"error": "Folder path is required."}, status=400)

    folder_full_path = os.path.join(settings.MEDIA_ROOT, folder_path)

    if not os.path.exists(folder_full_path) or not os.path.isdir(folder_full_path):
        return JsonResponse({"error": "Folder does not exist."}, status=404)

    try:
        # لیست کردن فایل‌های موجود در پوشه
        images = [f for f in os.listdir(folder_full_path) if os.path.isfile(os.path.join(folder_full_path, f))]
        return JsonResponse({"images": images})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)    

@csrf_exempt
def get_image_info(request):
    if request.method == 'POST':
        try:
            # دریافت داده‌های ارسالی از کلاینت
            data = json.loads(request.body)
            image_url = data.get('imageUrl')
            
            if not image_url:
                return JsonResponse({'error': 'آدرس تصویر ارسال نشده است'}, status=400)
            base_path = r"C:\Users\User\Desktop\TreeView"
            img = base_path + image_url
            
            # باز کردن تصویر
            image = Image.open(img)

            # ایجاد متادیتا
            metadata = PngInfo()
            metadata.add_text("width", str(image.width))  # عرض تصویر
            metadata.add_text("height", str(image.height))  # ارتفاع تصویر

            # ذخیره تصویر در حافظه با متادیتای جدید
            output = BytesIO()
            image.save(output, format="PNG", pnginfo=metadata)
            output.seek(0)

            # بازگشت اطلاعات به کلاینت
            return JsonResponse({
                'width': image.width,
                'height': image.height,
                'message': 'اطلاعات متادیتا با موفقیت ایجاد شد.'
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'تنها درخواست‌های POST مجاز هستند'}, status=400)


@csrf_exempt
def resize_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_url = data.get('imageUrl')
            print(image_url)
            print('!!!!!!!!!!!!!!!')
            base_path = r"C:\Users\User\Desktop\TreeView"
            img = base_path + image_url
            new_width = int(data.get('width'))
            new_height = int(data.get('height'))

            if not image_url or not new_width or not new_height:
                return JsonResponse({'error': 'اطلاعات ناقص است!'}, status=400)

            # باز کردن تصویر و تغییر ابعاد
            image = Image.open(img)
            resized_image = image.resize((new_width, new_height))

            # ذخیره‌سازی تصویر تغییر اندازه داده شده
            resized_image.save(img)

            # بازگشت مسیر تصویر جدید به سمت کلاینت
            return JsonResponse({'newImageUrl': image_url})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'درخواست نامعتبر'}, status=400)    


@csrf_exempt
def upload_cropped_image(request):
    if request.method == 'POST':
        try:
            # داده ارسال شده از کلاینت
            data = request.body.decode('utf-8')
            cropped_image_data = eval(data).get('croppedImage', None)
            original_image_path = eval(data).get('originalImagePath', None)  # مسیر تصویر اصلی
            base_path = r"C:\Users\User\Desktop\TreeView"  # مسیر پایه
            original_image_path = base_path + original_image_path

            if not cropped_image_data or not original_image_path:
                return JsonResponse({'error': 'Image data or original image path is missing.'}, status=400)

            # بررسی وجود فایل اصلی
            if not os.path.exists(original_image_path):
                return JsonResponse({'error': 'Original image not found.'}, status=404)

            # حذف اطلاعات "data:image/png;base64,"
            format, imgstr = cropped_image_data.split(';base64,')

            # ذخیره تصویر کراپ‌شده در مسیر جدید (مثلاً temp)
            cropped_image_path = original_image_path + "_temp"  # مسیر فایل موقت
            with open(cropped_image_path, 'wb') as f:
                f.write(base64.b64decode(imgstr))

            # حذف فایل اصلی
            os.remove(original_image_path)

            # تغییر نام فایل کراپ‌شده به نام فایل اصلی
            os.rename(cropped_image_path, original_image_path)

            # بازگشت پاسخ به کلاینت
            return JsonResponse({'success': True, 'message': 'Image successfully updated and original image deleted.'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
