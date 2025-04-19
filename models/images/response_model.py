from typing import Literal
from datetime import datetime

from enums.validation_status import ValidationStatus
from pydantic import BaseModel


class ImageResponseModel(BaseModel):
    image_id: str
    upload_time: datetime 
    uploader_id: str
    uploader_name: str
    sr_validation: ValidationStatus
    ai_validation: ValidationStatus
    sa_validation: ValidationStatus
    fa_validation: ValidationStatus