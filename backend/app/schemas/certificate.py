# Sertifikat sxemalari

import uuid
from datetime import datetime

from pydantic import BaseModel


class CertificateResponse(BaseModel):
    """Sertifikat yaratildi yoki mavjudi topildi."""
    certificate_number: str
    issued_at: datetime
    download_url: str
    course_id: uuid.UUID
    course_title: str

    model_config = {"from_attributes": True}


class CertificateListItem(BaseModel):
    """Foydalanuvchi sertifikatlari ro'yxatidagi bitta element."""
    certificate_number: str
    course_id: uuid.UUID
    course_title: str
    course_thumbnail: str | None
    issued_at: datetime
    download_url: str

    model_config = {"from_attributes": True}
