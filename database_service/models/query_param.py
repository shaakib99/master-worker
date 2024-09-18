from pydantic import BaseModel
from typing import Optional

class QueryParamsModel(BaseModel):
    limit: Optional[int] = 10
    skip: Optional[int] = 0
    selected_fields: Optional[list[str]] = []
    join_fields: Optional[list[str]] = []
    filter_by: Optional[str] = None
    group_by: Optional[str] = None
    order_by: Optional[str]= None
    having: Optional[str] = None
