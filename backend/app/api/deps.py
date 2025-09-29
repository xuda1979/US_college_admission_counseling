from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.security import decode_token
from ..db.session import get_db
from ..repositories.applicants import applicant_repository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


async def get_current_applicant(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    email = decode_token(token)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    applicant = await applicant_repository.get_by_email(db, email)
    if applicant is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Applicant not found")
    return applicant
