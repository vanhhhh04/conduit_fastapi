from datetime import datetime
from typing import List, Optional, Sequence

from pydantic import BaseModel, Field



class Profile(BaseModel):
    username: str
    bio: Optional[str]
    image: Optional[str]


