from typing import Literal

from pydantic import BaseModel

class ScoreRequestModel(BaseModel):
    score: Literal["PASS", "FAIL"]
    scorer_id: str