from fastapi import HTTPException
from starlette import status



def status_response_error(status_code: int, response_message: str):
    match status_code:
        case 401: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response_message)