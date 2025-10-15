"""
GridFS storage service for storing and retrieving raw resume files.
"""
from app.database import get_gridfs
from app.icons import X_MARK
from bson import ObjectId
from typing import Optional
import io


class StorageService:
    """Handle file storage operations using MongoDB GridFS."""
    
    async def store_file(
        self,
        file_content: bytes,
        filename: str,
        content_type: str
    ) -> str:
        """
        Store file in GridFS and return file ID.
        
        Args:
            file_content: Raw file bytes
            filename: Original filename
            content_type: MIME type
        
        Returns:
            String file ID
        """
        gridfs = get_gridfs()
        
        file_id = await gridfs.upload_from_stream(
            filename,
            io.BytesIO(file_content),
            metadata={
                "content_type": content_type,
                "original_filename": filename
            }
        )
        
        return str(file_id)
    
    async def retrieve_file(self, file_id: str) -> Optional[tuple]:
        """
        Retrieve file from GridFS.
        
        Args:
            file_id: GridFS file ID
        
        Returns:
            Tuple of (file_content, filename, content_type) or None
        """
        try:
            gridfs = get_gridfs()
            grid_out = await gridfs.open_download_stream(ObjectId(file_id))
            
            file_content = await grid_out.read()
            filename = grid_out.filename
            content_type = grid_out.metadata.get("content_type", "application/octet-stream")
            
            return (file_content, filename, content_type)
        except Exception as e:
            print(f"{X_MARK} Failed to retrieve file {file_id}: {e}")
            return None
    
    async def delete_file(self, file_id: str) -> bool:
        """
        Delete file from GridFS.
        
        Args:
            file_id: GridFS file ID
        
        Returns:
            True if deleted successfully
        """
        try:
            gridfs = get_gridfs()
            await gridfs.delete(ObjectId(file_id))
            return True
        except Exception as e:
            print(f"{X_MARK} Failed to delete file {file_id}: {e}")
            return False


# Global storage instance
storage_service = StorageService()
