from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------
# AUTH
# ---------------------------------------------------------

class RegisterRequest(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6,
        max_length=128,
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr


# ---------------------------------------------------------
# HOME INTERIOR
# ---------------------------------------------------------

class HomeRequest(BaseModel):
    budget: float = Field(..., gt=0)
    room_type: str = Field(..., min_length=2)
    room_count: int = Field(default=1, ge=1, le=20)

    lights: int = Field(default=0, ge=0)
    fans: int = Field(default=0, ge=0)
    dining_tables: int = Field(default=0, ge=0)

    style: Optional[str] = "Modern"
    notes: Optional[str] = ""


# ---------------------------------------------------------
# PARTY
# ---------------------------------------------------------

class PartyRequest(BaseModel):
    budget: float = Field(..., gt=0)
    guests: int = Field(..., ge=1, le=10000)

    event_type: str = Field(
        ...,
        min_length=2,
    )

    venue: str = Field(
        ...,
        min_length=2,
    )

    food_preference: Optional[str] = "Mixed"
    entertainment: Optional[str] = "Music"
    notes: Optional[str] = ""


# ---------------------------------------------------------
# JEWELRY
# ---------------------------------------------------------

class JewelryRequest(BaseModel):
    budget: float = Field(..., gt=0)

    occasion: str = Field(
        ...,
        min_length=2,
    )

    style: str = Field(
        ...,
        min_length=2,
    )

    metal: Optional[str] = "Any"
    notes: Optional[str] = ""


# ---------------------------------------------------------
# RECOMMENDATION
# ---------------------------------------------------------

class RecommendationResponse(BaseModel):
    success: bool
    category: str
    source: str
    data: Dict[str, Any]


class HistoryItem(BaseModel):
    id: int
    category: str
    created_at: str
    result: Dict[str, Any]