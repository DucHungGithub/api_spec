from typing import Literal

from pydantic import BaseModel


class ImageResponseModel(BaseModel):
    image_id: str
    upload_time: str 
    sr_validation: Literal["Unvalidate", "PASS", "FAIL"]
    ai_validation: Literal["Unvalidate", "PASS", "FAIL"]
    sa_validation: Literal["Unvalidate", "PASS", "FAIL"]
    fa_validation: Literal["Unvalidate", "PASS", "FAIL"]