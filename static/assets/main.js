
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
                           var figure = $('<figure>').addClass('image-figure');
                           
                           var img = $('<img>').attr('src', file.url).attr('alt', file.name).attr('id', file.name);        
                           img.css({
                               width: '200px',
                               height: 'auto',
                               margin: '10px'
                           });

                           
                           var caption = $('<figcaption>').text(file.name);

                           
                           var editButton = $('<button>').text('Edit').addClass('action-button edit-button');
                           var deleteButton = $('<button>').text('Delete').addClass('action-button delete-button').attr('id', 'delete_image');

                           
                           var buttonContainer = $('<div>').addClass('button-container').append(editButton, deleteButton);

                           
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

  $(document).on('click', '#delete_image', function() {
    var figure = $(this).closest('figure'); 
    figure.remove();
    var fileUrl = figure.find('img').attr('src') 

    $.ajax({
        url: '/delete-file/',
        type: 'POST',
        data: {
          fileUrl: fileUrl,
        },
        success: function(response) {
            alert('تصویر با موفقیت حذف شد.');
        },
        error: function(error) {
            alert('خطا در حذف تصویر.');
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