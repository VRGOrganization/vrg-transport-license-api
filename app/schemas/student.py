from pydantic import BaseModel


class Student(BaseModel):
    id: str
    name: str
    degree: str
    institution: str
    shift: str
    telephone: str
    blood_type: str
    photo: str | None = None  # base64 da foto do estudante (opcional)