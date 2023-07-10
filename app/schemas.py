from pydantic import BaseModel


class Points(BaseModel):
    x: float
    y: float