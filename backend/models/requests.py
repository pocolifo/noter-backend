from uuid import UUID
from pydantic import BaseModel, EmailStr



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