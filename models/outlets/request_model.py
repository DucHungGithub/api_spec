from typing import Literal

from enums.validation_status import ValidationStatus
from pydantic import BaseModel
class ScoreRequestModel(BaseModel):
    sr_validation: ValidationStatus
    ai_validation: ValidationStatus
    sa_validation: ValidationStatus
    fa_validation: ValidationStatus
