from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import FileResponse

class ImageRouter(APIRouter):
    def __init__(self, *args, **kwargs) -> None:
        super(ImageRouter, self).__init__(*args, **kwargs)
        
        self.add_api_route(
            "/static/images/{image_id}",
            self.get_image,
            methods=["GET"],
            status_code=200,
            summary="Serve a static image file"
        )
        
        self.image_paths = {
            "img1": "1.jpg",
            "img2": "2.jpg",
            "img3": "3.jpg",
            "img4": "4.jpg",
            "img5": "5.jpeg",
        }
        
        # Base directory for static images
        self.base_dir = Path("static/images")
        
        
    async def get_image(self, image_id: str) -> FileResponse:
        """
        Serves the image file identified by image_id from a static directory.
        """
        if image_id not in self.image_paths:
            # Handle case where image doesn't exist
            # In production, this would return a 404
            return FileResponse("static/images/notfound.png")
            
        image_path = self.base_dir / self.image_paths[image_id]
        
        # In a real implementation, you'd check if the file exists
        # For mock purposes, we'll just return the path
        return FileResponse(str(image_path))