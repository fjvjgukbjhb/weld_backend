from venv import create

from certifi import where
# TODO:userinfo=>user_text
from peewee import CharField, IntegerField, DateTimeField, JOIN, Model, fn, FloatField
from peewee_async import select

from common.session import BaseModel, paginator, db, async_db
# from weld_function.stft import stft
from utils.tools_func import convert_num_arr, convert_arr
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class WeldGene(BaseModel):
    id = IntegerField()
    weldBeadCode = CharField()
    weldMethod = CharField()
    weldMaterialInf = CharField()
    weldWorker = CharField()
    weldGrooveType = CharField()
    standard = CharField()
    weldTechnologyData = CharField()
    weldProcessData = CharField()
    testReportData = CharField()

    class Meta:
        table_name = 'weld_gene'


    @classmethod
    async def select_by_weld_id(cls, id:int):  # id查询
        # route = 'burnthrough.xlsx'
        result = await async_db.execute(WeldGene.select(id).where(WeldGene.id == id))


                # WeldGene.select (WeldGene,
                #                  fn.group_concat(WeldGene.id)
                #                  .python_value(convert_num_arr).alias('id')
                #                 fn.group_concat(WeldGene.id)
                #                 .python_value(convert_num_arr).alias('id')
                #                 )
        return result



