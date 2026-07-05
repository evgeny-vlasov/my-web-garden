/**
 * TinyMCE Rich Text Editor Initialization
 * Configuration for blog post content editor
 */

document.addEventListener('DOMContentLoaded', function() {
    // Check if TinyMCE is loaded
    if (typeof tinymce === 'undefined') {
        console.error('TinyMCE not loaded');
        return;
    }

    // Initialize TinyMCE
    tinymce.init({
        // Target textarea
        selector: '#content',

        // Editor size
        height: 500,
        menubar: false,

        // Plugins
        plugins: [
            'advlist', 'autolink', 'lists', 'link', 'image', 'charmap',
            'anchor', 'searchreplace', 'visualblocks', 'code', 'fullscreen',
            'insertdatetime', 'media', 'table', 'help', 'wordcount'
        ],

        // Toolbar
        toolbar: 'undo redo | formatselect | ' +
            'bold italic underline strikethrough | ' +
            'alignleft aligncenter alignright alignjustify | ' +
            'bullist numlist outdent indent | ' +
            'link image | ' +
            'removeformat code | help',

        // Content style
        content_style: `
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                font-size: 16px;
                line-height: 1.8;
                padding: 20px;
            }
            img {
                max-width: 100%;
                height: auto;
            }
        `,

        // Format options
        block_formats: 'Paragraph=p; Heading 2=h2; Heading 3=h3; Heading 4=h4; Blockquote=blockquote',

        // Image upload handler
        images_upload_handler: function(blobInfo, success, failure) {
            uploadImage(blobInfo, success, failure);
        },

        // Image settings
        image_advtab: true,
        image_caption: true,
        image_title: true,
        automatic_uploads: true,
        file_picker_types: 'image',

        // Link settings
        link_assume_external_targets: true,
        link_title: false,
        target_list: [
            {title: 'Same window', value: ''},
            {title: 'New window', value: '_blank'}
        ],

        // Auto-save to localStorage
        autosave_ask_before_unload: true,
        autosave_interval: '30s',
        autosave_prefix: 'tinymce-autosave-{path}{query}-{id}-',
        autosave_restore_when_empty: true,
        autosave_retention: '30m',

        // Paste settings
        paste_as_text: false,
        paste_data_images: true,
        paste_preprocess: function(plugin, args) {
            // Clean up pasted content
            args.content = args.content.replace(/<\s*script[^>]*>[\s\S]*?<\s*\/\s*script\s*>/gi, '');
        },

        // Formatting
        formats: {
            alignleft: {selector: 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,table,img', classes: 'text-start'},
            aligncenter: {selector: 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,table,img', classes: 'text-center'},
            alignright: {selector: 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,table,img', classes: 'text-end'},
            alignjustify: {selector: 'p,h1,h2,h3,h4,h5,h6,td,th,div,ul,ol,li,table,img', classes: 'text-justify'}
        },

        // Valid elements (security)
        valid_elements: '*[*]',
        extended_valid_elements: 'script[src|async|defer|type|charset]',

        // Callbacks
        init_instance_callback: function(editor) {
            console.log('TinyMCE initialized:', editor.id);

            // Show notification when autosave triggers
            editor.on('StoreDraft', function() {
                showEditorNotification('Draft saved automatically', 'info');
            });

            // Warn about unsaved changes
            editor.on('change', function() {
                window.onbeforeunload = function() {
                    return 'You have unsaved changes. Are you sure you want to leave?';
                };
            });
        },

        // Remove warning on submit
        setup: function(editor) {
            editor.on('submit', function() {
                window.onbeforeunload = null;
            });
        }
    });
});

/**
 * Upload image to server
 */
function uploadImage(blobInfo, success, failure) {
    const formData = new FormData();
    formData.append('file', blobInfo.blob(), blobInfo.filename());

    // Get CSRF token
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;

    fetch('/admin/upload-image', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Upload failed');
        }
        return response.json();
    })
    .then(data => {
        if (data.location) {
            success(data.location);
            showEditorNotification('Image uploaded successfully', 'success');
        } else {
            failure('Invalid response from server');
        }
    })
    .catch(error => {
        console.error('Upload error:', error);
        failure('Image upload failed: ' + error.message);
        showEditorNotification('Image upload failed', 'error');
    });
}

/**
 * Show notification in editor
 */
function showEditorNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} position-fixed bottom-0 end-0 m-3`;
    notification.style.zIndex = '99999';
    notification.innerHTML = `<i class="bi bi-${type === 'success' ? 'check-circle' : type === 'error' ? 'x-circle' : 'info-circle'} me-2"></i>${message}`;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

/**
 * Manual save function (can be called from save button)
 */
window.saveDraft = function() {
    if (typeof tinymce !== 'undefined') {
        tinymce.activeEditor.save();
        showEditorNotification('Draft saved', 'success');
    }
};

/**
 * Restore autosaved content
 */
window.restoreAutoSave = function() {
    if (typeof tinymce !== 'undefined' && tinymce.activeEditor) {
        tinymce.activeEditor.plugins.autosave.restoreDraft();
        showEditorNotification('Draft restored', 'info');
    }
};
