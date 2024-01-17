from datetime import datetime, date
import re
from typing import List, Optional, Union

import pytz
from peewee import Model
from pydantic import BaseModel, EmailStr, AnyHttpUrl, Field, constr, validator

from utils.tools_func import tz

class WeldGene(BaseModel):
    id: Optional[int]
    weldBeadCode: Optional[str]
    weldMethod: Optional[str]
    weldMaterialInf: Optional[str]
    weldWorker: Optional[str]
    weldGrooveType: Optional[str]
    standard:  Optional[str]
    weldTechnologyData: Optional[str]
    weldProcessData: Optional[str]
    testReportData: Optional[str]



  