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
        
        
    async def get_image(self, image_id: str) -> FileResponse:
        """
        Serves the image file identified by image_id from a static directory.
        """
        pass