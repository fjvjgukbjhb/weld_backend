"""
纯增删改查操作,写在model里面
"""

from common.session import BaseModel, paginator, db, async_db
from peewee import CharField, IntegerField, ForeignKeyField, TimeField
from playhouse.shortcuts import model_to_dict, dict_to_model
from sqlalchemy.orm import relationship
from peewee import fn, JOIN
import time
from utils.tools_func import convert_arr, convert_num_arr


class Department(BaseModel):
    """
    部门表，
    """
    id = IntegerField(primary_key=True)
    # parent_id = IntegerField()
    parentId = IntegerField(column_name='parent_id')
    name = CharField()
    code = CharField()
    sort = IntegerField()

    class Meta:
        table_name = 'department'  # 自定义映射的表名

    class Config:
        orm_mode = True

    @classmethod
    async def add_department(cls, department):  # 添加角色
        # result = await async_db.execute(Department.create(**department))
        result = await async_db.create(Department,**department)
        return result.id

    @classmethod
    async def del_by_department_id(cls, id):
        await async_db.execute(Department.delete().where(Department.id == id))

    @classmethod
    async def update_department(cls, department):
        # 字典结构更新数据
        print(department)
        u = await async_db.execute(Department.update(**department).where(Department.id == department['id']))
        #
        return u

    @classmethod
    async def fuzzy_query(cls, querydepartment):
        db = await async_db.execute(Department.select().where(Department.code.contains(querydepartment['code']),
                                       Department.name.contains(querydepartment['name'])).order_by(
            Department.sort,Department.code ).dicts())
        result = list(db)
        return result
    # Department.name == querydepartment['name']
    @classmethod
    async def select_all(cls):  # 获取
        db = await async_db.execute(Department.select().dicts())
        # 附加 iterator() 方法调用还可以减少内存消耗
        return list(db)
