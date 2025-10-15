from pydantic import BaseModel
from typing import Optional, Any, List, Dict

class ErrorItem(BaseModel):
    loc: Optional[List[Any]] = None
    msg: str
    type: Optional[str] = None

class ProblemDetail(BaseModel):
    type: Optional[str] = None
    title: str
    status: int
    detail: Optional[str] = None
    instance: Optional[str] = None
    errors: Optional[List[ErrorItem]] = None
    trace_id: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

