"""
Defines Pydantic data models for API requests and responses.

This module includes schemas used for validation and serialization
in FastAPI endpoints.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Used in POST /alerts for automatic validation and parsing
class Alert(BaseModel):
    ticker: str  # 1-10 characters, enforced in database
    price: float
    direction: str  # 'above' or 'below'
    expiration_time: Optional[datetime]  # ISO 8601 string will be automatically parsed
