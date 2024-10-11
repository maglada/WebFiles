$(document).ready(function() {
    $('#upload-form').on('submit', function(e) {
        e.preventDefault();
        var formData = new FormData(this);
        formData.append('current_path', $('#current-path').text());
        
        $.ajax({
            url: '/add_file',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                alert(response.message);
                location.reload();
            },
            error: function() {
                alert('Error uploading file');
            }
        });
    });

    $('.file-link').on('click', function(e) {
        e.preventDefault();
        var filepath = $(this).data('path');
        
        $.get('/preview/' + filepath, function(data) {
            var previewContent = $('#preview-content');
            previewContent.empty();
            
            if (data.type === 'text') {
                previewContent.html('<pre>' + data.content + '</pre>');
            } else if (data.type === 'image') {
                previewContent.html('<img src="' + data.src + '" alt="File preview" style="max-width: 100%;">');
            } else {
                previewContent.html('<p>Preview not available for this file type.</p>');
            }
        });
    });

    $('#create-file-btn').on('click', function() {
        var filename = $('#new-filename').val();
        var content = $('#new-file-content').val();
        var currentPath = $('#current-path').text();

        $.ajax({
            url: '/create_file',
            type: 'POST',
            data: {
                filename: filename,
                content: content,
                current_path: currentPath
            },
            success: function(response) {
                alert(response.message);
                location.reload();
            },
            error: function() {
                alert('Error creating file');
            }
        });
    });
});
