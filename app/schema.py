from pydantic import BaseModel 
from typing import Optional, Dict

class Item(BaseModel):
    data: Optional[Dict[str, str]]