from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, constr

class PatchDeviceRegistrationDto(BaseModel):
    deviceUniqueKey: constr(max_length=64)