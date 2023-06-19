from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, constr

class PostDeviceRegistrationDto(BaseModel):
    deviceOsSystem: constr(max_length=64)
    deviceOsVersion: constr(max_length=64)
    deviceUniqueKey: constr(max_length=64)