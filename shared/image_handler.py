"""
WebGarden Image Handler
Image upload, validation, and processing utilities using Pillow.
"""

import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image
import logging

logger = logging.getLogger(__name__)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Image size constraints
MAX_IMAGE_SIZE = (2000, 2000)  # Maximum dimensions in pixels
THUMBNAIL_SIZE = (300, 300)    # Thumbnail dimensions


def allowed_file(filename):
    """
    Check if file has an allowed extension.

    Args:
        filename: Name of the file to check

    Returns:
        True if extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_unique_filename(original_filename):
    """
    Generate a unique filename while preserving the extension.

    Args:
        original_filename: Original filename from upload

    Returns:
        Unique filename string
    """
    ext = original_filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return unique_name


def save_image(file, upload_folder, resize=True, create_thumbnail=False):
    """
    Save an uploaded image file with optional resizing and thumbnail creation.

    Args:
        file: FileStorage object from Flask request
        upload_folder: Directory to save the file
        resize: Whether to resize large images (default True)
        create_thumbnail: Whether to create a thumbnail (default False)

    Returns:
        Dictionary with file information or None if failed:
        {
            'filename': str,
            'original_filename': str,
            'filepath': str,
            'file_size': int,
            'thumbnail_path': str (if created)
        }
    """
    if not file or file.filename == '':
        logger.warning('No file provided')
        return None

    if not allowed_file(file.filename):
        logger.warning(f'File type not allowed: {file.filename}')
        return None

    try:
        # Ensure upload folder exists
        os.makedirs(upload_folder, exist_ok=True)

        # Generate unique filename
        original_filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(original_filename)
        filepath = os.path.join(upload_folder, unique_filename)

        # Save the file temporarily
        temp_path = filepath + '.tmp'
        file.save(temp_path)

        # Open and process the image
        with Image.open(temp_path) as img:
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if 'A' in img.mode else None)
                img = background

            # Resize if image is too large
            if resize and (img.width > MAX_IMAGE_SIZE[0] or img.height > MAX_IMAGE_SIZE[1]):
                img.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
                logger.info(f'Resized image to {img.size}')

            # Save the processed image
            img.save(filepath, quality=85, optimize=True)

            # Create thumbnail if requested
            thumbnail_path = None
            if create_thumbnail:
                thumbnail_filename = f"thumb_{unique_filename}"
                thumbnail_path = os.path.join(upload_folder, thumbnail_filename)

                thumb_img = img.copy()
                thumb_img.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
                thumb_img.save(thumbnail_path, quality=85, optimize=True)
                logger.info(f'Created thumbnail: {thumbnail_filename}')

        # Remove temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

        # Get file size
        file_size = os.path.getsize(filepath)

        logger.info(f'Successfully saved image: {unique_filename}')

        return {
            'filename': unique_filename,
            'original_filename': original_filename,
            'filepath': filepath,
            'file_size': file_size,
            'thumbnail_path': thumbnail_path
        }

    except Exception as e:
        logger.error(f'Error saving image: {str(e)}')
        # Clean up any partial files
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(filepath):
            os.remove(filepath)
        return None


def delete_image(filepath, delete_thumbnail=True):
    """
    Delete an image file and optionally its thumbnail.

    Args:
        filepath: Path to the image file
        delete_thumbnail: Whether to delete associated thumbnail (default True)

    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f'Deleted image: {filepath}')

            # Delete thumbnail if it exists
            if delete_thumbnail:
                directory = os.path.dirname(filepath)
                filename = os.path.basename(filepath)
                thumbnail_path = os.path.join(directory, f"thumb_{filename}")
                if os.path.exists(thumbnail_path):
                    os.remove(thumbnail_path)
                    logger.info(f'Deleted thumbnail: {thumbnail_path}')

            return True
    except Exception as e:
        logger.error(f'Error deleting image: {str(e)}')
        return False


def validate_image_file(file, max_size_mb=5):
    """
    Validate an image file before processing.

    Args:
        file: FileStorage object from Flask request
        max_size_mb: Maximum file size in megabytes

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file or file.filename == '':
        return False, 'No file selected'

    if not allowed_file(file.filename):
        return False, f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'

    # Check file size (read first chunk to avoid loading entire file)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    max_size_bytes = max_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        return False, f'File too large. Maximum size: {max_size_mb}MB'

    # Try to open as image
    try:
        img = Image.open(file)
        img.verify()
        file.seek(0)  # Reset file pointer after verify
        return True, None
    except Exception as e:
        return False, f'Invalid image file: {str(e)}'
