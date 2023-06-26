from fastapi.responses import JSONResponse
from fastapi_test.routers import UserRouter as router
import pydantic

# TODO: Need a way to make it works in an generic way

# Only for example, this code is not actually working
# @router.exception_handler(pydantic.error_wrappers.ValidationError)
# async def validantion_error_handling(request, exc):
#     return JSONResponse(content={'error': "User not found"}, status_code=404)