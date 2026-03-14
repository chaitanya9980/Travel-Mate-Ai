"""
Cloudinary Configuration for TravelMate AI
Handles image uploads and management with enhanced error handling
"""

import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cloudinary configuration - Replace with your actual credentials
CLOUDINARY_CONFIG = {
    'cloud_name': 'du66eeejp',
    'api_key': '854564547933489',
    'api_secret': 'Iu0uRT3SIU5_Kn01wHoS-nsaNIw'
}

# Try to initialize Cloudinary
CLOUDINARY_ENABLED = False

try:
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    
    cloudinary.config(
        cloud_name=CLOUDINARY_CONFIG['cloud_name'],
        api_key=CLOUDINARY_CONFIG['api_key'],
        api_secret=CLOUDINARY_CONFIG['api_secret']
    )
    CLOUDINARY_ENABLED = True
    logger.info("Cloudinary initialized successfully")
except ImportError:
    logger.warning("Cloudinary: cloudinary package not installed. Image uploads will use URLs only.")
except Exception as e:
    logger.error(f"Cloudinary: Configuration failed. Error: {e}")

class CloudinaryManager:
    """
    Enhanced Cloudinary Helper Class
    Provides methods for image upload, management, and deletion with proper error handling
    """

    @staticmethod
    def upload_image(file_or_path, folder='travelmate', **kwargs):
        """
        Upload an image to Cloudinary with enhanced error handling
        
        Args:
            file_or_path: File object or path to the image file
            folder: Folder name in Cloudinary (default: 'travelmate')
            **kwargs: Additional Cloudinary upload options
            
        Returns:
            dict: Upload result with URL and other metadata
        """
        if not CLOUDINARY_ENABLED:
            logger.warning("Cloudinary upload attempted but not configured")
            return {
                'success': False,
                'error': 'Cloudinary not configured'
            }
        
        try:
            # Set default options
            upload_options = {
                'folder': folder,
                'resource_type': 'image',
                'overwrite': False,
                'invalidate': True
            }
            upload_options.update(kwargs)
            
            logger.info(f"Uploading image to Cloudinary folder: {folder}")
            result = cloudinary.uploader.upload(file_or_path, **upload_options)
            
            logger.info(f"Successfully uploaded: {result.get('public_id')}")
            return {
                'success': True,
                'url': result['secure_url'],
                'public_id': result['public_id'],
                'bytes': result.get('bytes'),
                'format': result.get('format'),
                'width': result.get('width'),
                'height': result.get('height')
            }
        except Exception as e:
            error_msg = f"Cloudinary upload failed: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }

    @staticmethod
    def upload_image_from_url(image_url, folder='travelmate', **kwargs):
        """
        Upload an image from URL to Cloudinary with enhanced error handling
        
        Args:
            image_url: URL of the image
            folder: Folder name in Cloudinary
            **kwargs: Additional upload options
            
        Returns:
            dict: Upload result
        """
        if not CLOUDINARY_ENABLED:
            logger.warning("Cloudinary upload from URL attempted but not configured")
            return {
                'success': False,
                'error': 'Cloudinary not configured'
            }
        
        try:
            upload_options = {
                'folder': folder,
                'resource_type': 'image'
            }
            upload_options.update(kwargs)
            
            logger.info(f"Uploading image from URL to Cloudinary: {image_url}")
            result = cloudinary.uploader.upload(image_url, **upload_options)
            
            logger.info(f"Successfully uploaded from URL: {result.get('public_id')}")
            return {
                'success': True,
                'url': result['secure_url'],
                'public_id': result['public_id'],
                'source_url': image_url
            }
        except Exception as e:
            error_msg = f"Cloudinary upload from URL failed: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }

    @staticmethod
    def delete_image(public_id):
        """
        Delete an image from Cloudinary with enhanced error handling
        
        Args:
            public_id: Public ID of the image
            
        Returns:
            dict: Deletion result with success status and details
        """
        if not CLOUDINARY_ENABLED:
            logger.warning(f"Cloudinary delete attempted for {public_id} but not configured")
            return {
                'success': False,
                'error': 'Cloudinary not configured'
            }
        
        try:
            logger.info(f"Deleting image from Cloudinary: {public_id}")
            result = cloudinary.uploader.destroy(public_id)
            
            success = result.get('result') == 'ok'
            if success:
                logger.info(f"Successfully deleted: {public_id}")
            else:
                logger.warning(f"Deletion may have failed for {public_id}: {result}")
                
            return {
                'success': success,
                'result': result,
                'public_id': public_id
            }
        except Exception as e:
            error_msg = f"Cloudinary deletion failed for {public_id}: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'public_id': public_id
            }

    @staticmethod
    def delete_multiple_images(public_ids):
        """
        Delete multiple images from Cloudinary
        
        Args:
            public_ids: List of public IDs to delete
            
        Returns:
            dict: Batch deletion result
        """
        if not CLOUDINARY_ENABLED:
            return {
                'success': False,
                'error': 'Cloudinary not configured',
                'deleted': [],
                'failed': public_ids
            }
        
        deleted = []
        failed = []
        
        for public_id in public_ids:
            result = CloudinaryManager.delete_image(public_id)
            if result['success']:
                deleted.append(public_id)
            else:
                failed.append({
                    'public_id': public_id,
                    'error': result.get('error', 'Unknown error')
                })
        
        logger.info(f"Batch deletion completed. Deleted: {len(deleted)}, Failed: {len(failed)}")
        return {
            'success': len(failed) == 0,
            'deleted': deleted,
            'failed': failed,
            'total_processed': len(public_ids)
        }

    @staticmethod
    def get_image_url(public_id, width=None, height=None, crop='fill', **transformations):
        """
        Get optimized image URL with transformations
        
        Args:
            public_id: Public ID of the image
            width: Desired width
            height: Desired height
            crop: Crop mode (fill, fit, scale, etc.)
            **transformations: Additional transformation parameters
            
        Returns:
            str: Optimized image URL
        """
        if not CLOUDINARY_ENABLED:
            return None
            
        try:
            options = {}
            if width:
                options['width'] = width
            if height:
                options['height'] = height
            if width or height:
                options['crop'] = crop
            options.update(transformations)
            
            url = cloudinary.CloudinaryImage(public_id).build_url(**options)
            return url
        except Exception as e:
            logger.error(f"Failed to generate Cloudinary URL: {e}")
            return None

    @staticmethod
    def list_images(folder='travelmate', max_results=100):
        """
        List all images in a folder
        
        Args:
            folder: Folder name
            max_results: Maximum number of results
            
        Returns:
            list: List of image resources with metadata
        """
        if not CLOUDINARY_ENABLED:
            return []
            
        try:
            logger.info(f"Listing images in folder: {folder}")
            result = cloudinary.api.resources(
                type='upload',
                prefix=folder,
                max_results=max_results
            )
            resources = result.get('resources', [])
            logger.info(f"Found {len(resources)} images in folder: {folder}")
            return resources
        except Exception as e:
            logger.error(f"Failed to list images in folder {folder}: {e}")
            return []

    @staticmethod
    def get_image_info(public_id):
        """
        Get detailed information about an image
        
        Args:
            public_id: Public ID of the image
            
        Returns:
            dict: Image information or None if not found
        """
        if not CLOUDINARY_ENABLED:
            return None
            
        try:
            info = cloudinary.api.resource(public_id)
            return info
        except Exception as e:
            logger.error(f"Failed to get image info for {public_id}: {e}")
            return None

    @staticmethod
    def extract_public_id_from_url(url):
        """
        Extract public_id from a Cloudinary URL
        
        Args:
            url: Cloudinary image URL
            
        Returns:
            str: Public ID or None if not a Cloudinary URL
        """
        if not url or 'cloudinary' not in url:
            return None
            
        try:
            # Extract public_id from URL like:
            # https://res.cloudinary.com/cloud_name/image/upload/v123456789/travelmate/destinations/image_name.jpg
            # OR: https://res.cloudinary.com/cloud_name/image/upload/travelmate/destinations/image_name.jpg
            
            # Find the 'upload' part and get everything after it
            parts = url.split('/upload/')
            if len(parts) < 2:
                return None
                
            # Get the part after 'upload/' - this includes version number and path
            path_part = parts[1]
            
            # Remove version number if present (starts with 'v' followed by digits)
            path_segments = path_part.split('/')
            if path_segments[0].startswith('v') and path_segments[0][1:].isdigit():
                # Remove version segment
                path_segments = path_segments[1:]
            
            # Join remaining segments to get the full public_id with folder path
            public_id_with_folder = '/'.join(path_segments)
            
            # Remove file extension
            public_id = '.'.join(public_id_with_folder.split('.')[:-1])
            
            logger.info(f"Extracted public_id: {public_id} from URL")
            return public_id
            
        except Exception as e:
            logger.error(f"Failed to extract public_id from URL {url}: {e}")
            
        return None

    @staticmethod
    def cleanup_destination_images(destination_data):
        """
        Cleanup all images associated with a destination
        
        Args:
            destination_data: Dictionary containing destination data with image URLs
            
        Returns:
            dict: Cleanup result with success status and details
        """
        if not CLOUDINARY_ENABLED:
            return {
                'success': False,
                'error': 'Cloudinary not configured',
                'deleted': [],
                'failed': []
            }
            
        main_image_url = destination_data.get('image', '')
        gallery_urls = destination_data.get('gallery', [])
        
        public_ids_to_delete = []
        
        # Extract public_id from main image
        main_public_id = CloudinaryManager.extract_public_id_from_url(main_image_url)
        if main_public_id:
            public_ids_to_delete.append(main_public_id)
            
        # Extract public_ids from gallery images
        for gallery_url in gallery_urls:
            gallery_public_id = CloudinaryManager.extract_public_id_from_url(gallery_url)
            if gallery_public_id:
                public_ids_to_delete.append(gallery_public_id)
                
        if not public_ids_to_delete:
            logger.info("No Cloudinary images found to delete")
            return {
                'success': True,
                'message': 'No Cloudinary images to delete',
                'deleted': [],
                'failed': []
            }
            
        # Delete all images
        result = CloudinaryManager.delete_multiple_images(public_ids_to_delete)
        return result

# Gallery categories for the travel gallery
gallery_categories = {
    'beaches': {
        'name': 'Beaches',
        'description': 'Pristine beaches and coastal destinations',
        'images': [
            'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800',
            'https://images.unsplash.com/photo-1519046904884-53103b34b206?w=800',
            'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800'
        ]
    },
    'mountains': {
        'name': 'Mountains',
        'description': 'Majestic mountain ranges and hill stations',
        'images': [
            'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800',
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
            'https://images.unsplash.com/photo-1626010448982-4d629b1a0151?w=800'
        ]
    },
    'cities': {
        'name': 'Cities',
        'description': 'Vibrant cities and urban destinations',
        'images': [
            'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=800',
            'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800',
            'https://images.unsplash.com/photo-1477587458883-47145ed94245?w=800'
        ]
    },
    'adventure': {
        'name': 'Adventure',
        'description': 'Thrilling adventure destinations',
        'images': [
            'https://images.unsplash.com/photo-1533692328991-08159ff19fca?w=800',
            'https://images.unsplash.com/photo-1522163182402-834f871fd851?w=800',
            'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800'
        ]
    }
}

# Instructions for Cloudinary Setup:
"""
1. Go to https://cloudinary.com/ and create a free account
2. Get your Cloud Name, API Key, and API Secret from the dashboard
3. Replace the placeholder values in CLOUDINARY_CONFIG above
4. Install cloudinary: pip install cloudinary
5. Use CloudinaryManager.upload_image() to upload images
6. Store the returned URL in your database
7. For deletion, use CloudinaryManager.delete_image() with the public_id
"""
