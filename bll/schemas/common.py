
from typing import Any, Dict, Optional
from pydantic import BaseModel

from models.constants import MODIFIED_AT_SORT_KEY
from models.enums import SortDirection


class PaginationParams(BaseModel):
    offset: Optional[int] = 0
    limit: Optional[int] = 10
    sort_by: Optional[str] = MODIFIED_AT_SORT_KEY
    sort_direction: Optional[int] = SortDirection.ASC
    filter_key: Optional[str] = None
    filter_value: Optional[Any] = None