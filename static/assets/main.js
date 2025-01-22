
$(document).ready(function() {
    $(".folder").click(function() {  

        var folderPath = $(this).find('input[name="path"]').val();

        $.ajax({
            url: '/get-folder-files/', 
            type: 'GET',
            data: {
                path: folderPath
            },
            success: function(response) {
              
                if (response && response.files) {
                  
                  var imageContainer = $("#image-container");
                  imageContainer.empty(); // پاک کردن محتوای قبلی

                  response.files.forEach(function(file) {              
                      if (file.url) {
                          // ایجاد یک تگ <img> برای هر فایل
                          var img = $('<img>').attr('src', file.url).attr('alt', file.name);
                          img.css({
                              width: '150px',
                              height: 'auto',
                              margin: '10px'
                          }); // تنظیم استایل دلخواه
                          imageContainer.append(img); // افزودن <img> به container
                      }
                  });

                }
            },
            error: function(error) {
                alert("خطا در بارگذاری فایل‌ها");
            }
        });
    });
});

function toggleFolder(id) {
    const folderElement = document.getElementById(id);
   
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