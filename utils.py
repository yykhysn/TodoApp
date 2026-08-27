from fastapi import HTTPException
from sqlalchemy import Row
from starlette import status


def status_response_error(status_code: int, response_message: str):
    match status_code:
        case 401: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response_message)
        case 404: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=response_message)


def sql_result_to_dict(sql_result):
    if sql_result is None:
        return None
    if isinstance(sql_result, Row):
        return sql_result._asdict()
    return [result._asdict() for result in sql_result]