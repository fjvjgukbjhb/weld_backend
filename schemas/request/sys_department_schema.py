from datetime import datetime
import re
from typing import List, Optional

from pydantic import BaseModel, EmailStr, AnyHttpUrl, Field, constr, validator

from utils.tools_func import tz


# SQLAlchemy 模型使用 定义属性，并将类型作为参数传递,   =Column
# 而 Pydantic 模型使用 、 新类型注释语法/类型提示声明类型：

# 用于读取的 Pydantic 模型中，添加一个内部类。ItemUserConfig
# Config类用于为 Pydantic 提供配置

# Shared properties


class DepartmentBase(BaseModel):
    # id: int 自增字段

    parentId: Optional[int]=0
    name: Optional[str] = ''
    code: Optional[str] = ''
    sort:Optional[int]
    createAt: Optional[datetime] = None
    
class DepartmentUpdate(BaseModel):
    id: Optional[int] = None
    parentId: Optional[int] = 0
    name: Optional[str] = ''
    code: Optional[str] = ''
    sort: Optional[int] = 1
    updateAt: Optional[datetime] = None

class DepartmentQuery(BaseModel):
    code: Optional[str] = ''
    name: Optional[str] = ''
    # current: int= 1
    # pageSize: int = 5
class DepartmentDelete(BaseModel):
    id: Optional[int]
