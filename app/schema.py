from pydantic import BaseModel 
from typing import  Dict

class Item(BaseModel):
    data: Dict[str, str]