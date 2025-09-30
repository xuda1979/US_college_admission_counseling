from pydantic import BaseModel, ConfigDict, EmailStr


class ApplicantCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class ApplicantRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
