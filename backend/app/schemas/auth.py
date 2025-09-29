from pydantic import BaseModel, EmailStr


class ApplicantCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class ApplicantRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
