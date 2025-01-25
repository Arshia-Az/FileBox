
// عکسای داخل پوشه ی media رو میگیره 
$(document).ready(function() {
  
    $(".folder").click(function() {  
        
        var folderPath = $(this).find('input[name="path"]').val();
        $('#path').val(folderPath)
        $.ajax({
            url: '/get-folder-files/', 
            type: 'GET',
            data: {
                path: folderPath
            },
            success: function(response) {
              
                if (response && response.files) {
                  
                  var imageContainer = $("#image-container");
                  imageContainer.empty(); 
                  response.files.forEach(function(file) {              
                      if (file.url) {  
                           var figure = $('<figure>').addClass('image-figure');
                           
                           var img = $('<img>').attr('src', file.url).attr('alt', file.name).attr('id', file.name);        
                           img.css({
                               width: '200px',
                               height: '200px',
                               margin: '10px'
                           });

                           
                           var caption = $('<figcaption>').text(file.name);

                           
                           var editButton = $('<button>').text('rename').addClass('action-button edit-button').attr('id', 'rename_image');
                           var deleteButton = $('<button>').text('Delete').addClass('action-button delete-button').attr('id', 'delete_image');

                           
                           var buttonContainer = $('<div>').addClass('button-container').append(editButton, deleteButton);

                        //    var inputAll = $('<input>').attr('type', 'hidden').attr('name', 'path').val(folderPath);
                           figure.append(img).append(caption).append(buttonContainer);

                           
                           imageContainer.append(figure);
                      }
                  });

                }
            },
            error: function(error) {
                alert("خطا در بارگذاری فایل‌ها");
            }
        });
    });
    
    // search box
    $("#search-box").on("keyup", function () {
      var searchTerm = $(this).val().toLowerCase();

      
      $("#image-container figure").each(function() {
          var captionText = $(this).find('figcaption').text().toLowerCase();

          if (captionText.includes(searchTerm)) {
              $(this).show();
          } else {
              $(this).hide(); 
          }
      });
  });

  // rename_image
  $(document).on('click', '#rename_image', function() {
    var figure = $(this).closest('figure');
    var caption = figure.find('figcaption');
    var fullName = caption.text(); 
    var nameUrl = figure.find('img').attr('src') 
    
    var nameParts = fullName.split('.');
    var baseName = nameParts.slice(0, -1).join('.'); 
    var extension = nameParts.slice(-1); 

    
    var input = $('<input>')
        .attr('type', 'text')
        .addClass('rename-input')
        .val(baseName);

    
    caption.replaceWith(input);
    input.focus();

    
    input.on('keypress', function(e) {
        if (e.which === 13) { 
            var newBaseName = input.val().trim();

            
            if (newBaseName && newBaseName !== baseName) {
                var newFullName = newBaseName + '.' + extension; 

                
                $.ajax({
                    url: '/rename-file/',
                    type: 'POST',
                    data: {
                        old_name: fullName,
                        new_name: newFullName,
                        name_url: nameUrl
                    },
                    success: function(response) {
                        // به‌روزرسانی لینک مرتبط
                        var link = $('a.image').filter(function() {
                            return $(this).text().trim() === '📄 ' + fullName;
                        });
                        link.text('📄 ' + newFullName); // به‌روزرسانی متن لینک
                        link.attr('onclick', "fileClicked('" + newFullName + "')"); // به‌روزرسانی مقدار onclick

                        // جایگزینی ورودی با figcaption و نمایش نام جدید
                        var updatedCaption = $('<figcaption>').text(newFullName);
                        input.replaceWith(updatedCaption);
                    },
                    error: function(error) {
                        alert('خطا در تغییر نام.');
                        var originalCaption = $('<figcaption>').text(fullName);
                        input.replaceWith(originalCaption);
                    }
                });
            } else {
                
                var originalCaption = $('<figcaption>').text(fullName);
                input.replaceWith(originalCaption);
            }
        }
    });

    
    input.on('blur', function() {
        var currentBaseName = input.val().trim(); 

        if (currentBaseName && currentBaseName !== baseName) {
            var newFullName = currentBaseName + '.' + extension; 

            
            $.ajax({
                url: '/rename-file/',
                type: 'POST',
                data: {
                    old_name: fullName,
                    new_name: newFullName
                },
                success: function(response) {
                    alert('نام با موفقیت تغییر کرد.');

                    
                    var updatedCaption = $('<figcaption>').text(newFullName);
                    input.replaceWith(updatedCaption);
                },
                error: function(error) {
                    alert('خطا در تغییر نام.');
                    var originalCaption = $('<figcaption>').text(fullName);
                    input.replaceWith(originalCaption);
                }
            });
        } else {

            var originalCaption = $('<figcaption>').text(fullName);
            input.replaceWith(originalCaption);
        }
    });
});


 // delete image
$(document).on('click', '#delete_image', function() {
    var figure = $(this).closest('figure'); 
    
    
    var fileUrl = figure.find('img').attr('src'); 
    var caption = figure.find('figcaption');
    var fullName = caption.text(); 

    
    if (!confirm('آیا مطمئن هستید که می‌خواهید این تصویر را حذف کنید؟')) {
        return;
    }

    
    $.ajax({
        url: '/delete-file/',
        type: 'POST',
        data: {
            fileUrl: fileUrl,
        },
        success: function(response) {
            alert('فایل با موفقیت حذف شد.');

            
            figure.remove();

            
            $('a.image').filter(function() {
                return $(this).text().trim() === '📄 ' + fullName;
            }).remove();
        },
        error: function(error) {
            alert('خطا در حذف تصویر.');
        }
    });
});

});

// for show folder
function toggleFolder(id) {
    const folderElement = document.getElementById(id);
    console.log(this);
    if (folderElement) {
      
      if (folderElement.style.display === "none") {
        folderElement.style.display = "block";
      } else {
        folderElement.style.display = "none"; 
      }
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    const treeNodes = document.querySelectorAll("#media-tree ul");
    treeNodes.forEach((node) => {
      node.style.display = "none";
    });

    const rootNodes = document.querySelectorAll("#media-tree > ul");
    rootNodes.forEach((node) => {
      node.style.display = "block";
    });
  });


function showCreateFolderForm() {
    const form = document.getElementById("create-folder-form");
    form.style.display = "block";
}

function hideCreateFileForm() {
    const form = document.getElementById("create-folder-form");
    form.style.display = "none";
}  


$(document).ready(function () {
    // نمایش فرم ایجاد پوشه
    $("#show-create-folder").click(function () {
        $("#create-folder-form").show(); // نمایش فرم ایجاد
        $("#delete-folder-form").hide(); // مخفی کردن فرم حذف
    });

    // مخفی کردن ایجاد پوشه
    $("#hide-create-folder").click(function () {
        $("#create-folder-form").hide(); // مخفی کردن فرم ایجاد پوشه
    });

    // نمایش فرم حذف پوشه
    $("#show-delete-folder").click(function () {
        $("#delete-folder-form").show(); // نمایش فرم حذف
        $("#create-folder-form").hide(); // مخفی کردن فرم ایجاد
    });

    // مخفی کردن فرم حذف
    $("#hide-delete-folder").click(function () {
        $("#delete-folder-form").hide(); // مخفی کردن فرم حذف
    });

    // انتخاب پوشه و ذخیره مسیر آن برای حذف
    $(".folder").click(function () {
        var folderPath = $(this).find("input[name='path']").val(); // گرفتن مسیر پوشه
        $("#delete-path").val(folderPath); // ذخیره مسیر در فرم حذف
        
    });

    // ارسال فرم حذف از طریق Ajax
    $("#delete-folder-form").submit(function (e) {
        e.preventDefault(); 

        var folderPath = $("#delete-path").val();
        
        $.ajax({
            url: "/delete_folder/",
            type: "POST",
            data: {
                folder_path: folderPath,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(), 
            },
            success: function (response) {
                alert("Folder deleted successfully!");
                
                location.reload(); 
            },
            error: function (xhr, status, error) {
                alert("Error deleting folder: " + error);
            },
        });
    });
});

$(document).ready(function () {
    // نمایش فرم آپلود تصاویر
    $("#show-upload-image").click(function () {
        $("#upload-image-form").show(); // نمایش فرم
        $("#upload-message").hide(); // مخفی کردن پیام
    });

    // مخفی کردن فرم آپلود تصاویر
    $("#hide-upload-image").click(function () {
        $("#upload-image-form").hide(); // مخفی کردن فرم
    });

    // انتخاب پوشه و ذخیره مسیر آن
    $(".folder").click(function () {
        var folderPath = $(this).find("input[name='path']").val(); // مسیر پوشه انتخاب‌شده
        $("#image-folder-path").val(folderPath); // ذخیره مسیر در فرم
        
    });

    // ارسال چند تصویر با Ajax
    $("#multi-image-upload-form").submit(function (e) {
        e.preventDefault(); // جلوگیری از ارسال عادی فرم

        var formData = new FormData(this); // گرفتن اطلاعات فرم

        // اضافه کردن چندین فایل به فرم دیتا
        var files = $("#image-files")[0].files;
        for (let i = 0; i < files.length; i++) {
            formData.append("images", files[i]);
        }

        $.ajax({
            url: "/upload_images/", // آدرس ویو آپلود
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $("#upload-message").text("Images uploaded successfully!").css("color", "green").show();
                $("#upload-image-form").hide(); // مخفی کردن فرم
                // به‌روزرسانی نمایش تصاویر (در صورت نیاز)
            },
            error: function (xhr, status, error) {
                $("#upload-message").text("Error uploading images: " + error).css("color", "red").show();
            },
        });
    });
});
