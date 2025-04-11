from fastapi import FastAPI
import uvicorn

from routers import OutletRouter, PromotionRouter, ImageRouter



app = FastAPI()
app.include_router(OutletRouter(), prefix="/outlets", tags=["Outlets"])
app.include_router(PromotionRouter(), prefix="/promotions", tags=["Promotions"])
app.include_router(ImageRouter(), tags=["Images"])



if __name__ == "__main__":
    uvicorn.run(app)