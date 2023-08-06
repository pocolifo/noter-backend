from enum import Enum
import os
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class NoterPlan(Enum):
    FREE = 'free'
    PREMIUM_MONTHLY = 'premium_monthly'
    PREMIUM_YEARLY = 'premium_yearly'

    @property
    def stripe_price(self):
        return {
            NoterPlan.FREE: None,
            NoterPlan.PREMIUM_MONTHLY: os.environ['STRIPE_PRICE_NOTER_PREMIUM_MONTHLY'],
            NoterPlan.PREMIUM_YEARLY: os.environ['STRIPE_PRICE_NOTER_PREMIUM_YEARLY']
        }[self]


class UserCredentialsRequest(BaseModel):
    email: EmailStr
    password: str


class ItemMetadataRequest(BaseModel):
    path: list[str]
    name: str


class CreateStudyGuideRequest(ItemMetadataRequest):
    from_notes: list[UUID]


class RequestEmailUpdateRequest(BaseModel):
    email: EmailStr


class EmailUpdateRequest(RequestEmailUpdateRequest):
    cur_code: int
    new_code: int


class NameUpdateRequest(BaseModel):
    name: str


class PFPUpdateRequest(BaseModel):
    image: str