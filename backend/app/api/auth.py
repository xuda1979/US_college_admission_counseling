from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import get_settings
from ..core.security import create_access_token, get_password_hash, verify_password
from ..db.session import get_db
from ..repositories.applicants import applicant_repository
from ..schemas.auth import ApplicantCreate, ApplicantRead, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=ApplicantRead)
async def register(applicant_in: ApplicantCreate, db: AsyncSession = Depends(get_db)):
    existing = await applicant_repository.get_by_email(db, applicant_in.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    applicant = await applicant_repository.create(
        db,
        {
            "email": applicant_in.email,
            "full_name": applicant_in.full_name,
            "password_hash": get_password_hash(applicant_in.password),
        },
    )
    return applicant


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    applicant = await applicant_repository.get_by_email(db, form_data.username)
    if not applicant or not verify_password(form_data.password, applicant.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    settings = get_settings()
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    token = create_access_token(applicant.email, access_token_expires)
    return Token(access_token=token)
