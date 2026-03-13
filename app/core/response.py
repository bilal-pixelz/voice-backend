from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse

class ResponseModel(BaseModel):
    success: bool = Field(..., example=True)
    data: Optional[Any] = Field(None, example=None)
    message: str = Field("", example="Success")
    error: List[Dict[str, Any]] = Field([], example=[])

def create_response(
    success: bool,
    data: Optional[Any] = None,
    message: str = "",
    error: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]] = None,
    status_code: int = 200,
) -> JSONResponse:
    if error is None:
        error = []
    elif isinstance(error, dict):
        error = [error]
        
    response_content = ResponseModel(
        success=success,
        data=data,
        message=message,
        error=error
    ).dict()
    
    return JSONResponse(content=response_content, status_code=status_code)
