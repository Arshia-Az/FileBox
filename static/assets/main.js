
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

                           
                           var editButton = $('<button>').text('rename').addClass('action-button edit-button').attr('id', 'rename_image');
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

  $(document).on('click', '#delete_image', function() {
    var figure = $(this).closest('figure'); 
    figure.remove();
    var fileUrl = figure.find('img').attr('src') 
    alert('11111111111111111111111111111111111111111111111')
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