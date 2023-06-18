from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class UserDto(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []

# external_data = {'signup_ts': '2017-06-01 12:22', 'friends': [1, '2', b'3']}
# user = UserDto(**external_data)