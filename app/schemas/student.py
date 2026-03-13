from pydantic import BaseModel, Field


class Student(BaseModel):
    id: str =           Field(min_length=1, description="ID do estudante")
    employee_id: str =  Field(min_length=1, description="ID do funcionario que realizou criacao da carteirinha")
    name: str =         Field(min_length=1, description="Nome completo do estudante")
    degree: str =       Field(min_length=1, description="Curso do estudante")
    institution: str =  Field(min_length=1, description="Instituição de ensino")
    shift: str =        Field(min_length=1, description="Turno (Manhã, Tarde, Noite)")
    telephone: str =    Field(min_length=1, description="Telefone de contato")
    blood_type: str =   Field(min_length=1, description="Tipo sanguíneo")
    bus: str =          Field(min_length=1, description="Número do ônibus")
    photo: str | None = None  # base64 da foto do estudante (opcional)