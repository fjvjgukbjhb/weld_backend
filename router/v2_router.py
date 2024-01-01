# '''
# Author: 嘉欣 罗 2592734121@qq.com
# Date: 2022-12-22 12:49:07
# LastEditors: Please set LastEditors
# LastEditTime: 2023-05-09 14:56:59
# FilePath: \psad-backend\router\v1_router.py
# Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
# '''
# import os
#
# """
#
# 版本路由区分
#
# # 可以在这里添加所需要的依赖
# https://fastapi.tiangolo.com/tutorial/bigger-applications/#import-fastapi
#
# """
#
# # from common.deps import check_authority
#
# # from api.v1.sys_scheduler import router as scheduler_router
#
#
# # from api.v1.user_des import router as userinfo_router
# from common.deps import check_jwt_token, verify_current_user_perm
# from api.v1.fan_introduction import router as fan_introduction_router
# from api.v1.user_action import router as user_action_router
# from api.v1.usermenu import router as usermenu_router
# from api.v1.userrole import router as userrole_router
# from api.v1.user import router as user_router
# from api.v1.fan_category import router as fan_category_router
# from api.v1.fan_application_model import router as application_model_router
# from api.v1.perf import router as performance_router
# from fastapi import APIRouter, Depends
# from api.v1.items import router as items_router
# from api.v1.fan import router as fan_router
# from api.v1.file import router as file_router
# from api.v1.permission import router as permission_router
# from api.v1.sys_manage import router as sys_manage_router
# from api.v1.department import router as department_router
# from api.v1.audit import router as audit_router
# from api.v1.intro_control import router as intro_control_router
# from api.v2.weld import router as weld_router
#
#
# api_v2_router = APIRouter()
#
# # if os.getenv('DEBUG')=='True':
# api_v2_router.include_router(
#     weld_router, prefix="/api", tags=["焊接测试接口"])