"""
Testes para o schema Student (Pydantic model)
"""
import pytest
from pydantic import ValidationError

from app.schemas.student import Student


class TestStudentSchema:
    """Testes do schema Student"""
    
    def test_valid_student_with_photo(self, valid_student_data):
        """Teste com dados válidos incluindo foto."""
        student = Student(**valid_student_data)
        
        assert student.id == valid_student_data["id"]
        assert student.name == valid_student_data["name"]
        assert student.photo == valid_student_data["photo"]
    
    def test_valid_student_without_photo(self, valid_student_data_no_photo):
        """Teste com dados válidos sem foto (campo opcional)."""
        student = Student(**valid_student_data_no_photo)
        
        assert student.photo is None
    
    def test_missing_required_field(self):
        """Teste com campo obrigatório faltando - deve levantar ValidationError."""
        incomplete_data = {
            "id": "2024001",
            # "name": missing!
            "degree": "Engenharia",
            "institution": "UFPE",
            "shift": "Manhã",
            "telephone": "(81) 99999-9999",
            "blood_type": "O+",
            "bus": "123"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            Student(**incomplete_data)
        
        # Verifica que o erro menciona o campo 'name'
        assert "name" in str(exc_info.value)
    
    def test_invalid_type(self):
        """Teste com tipo de dado inválido."""
        invalid_data = {
            "id": 123,  # Deveria ser string
            "name": "João",
            "degree": "Engenharia",
            "institution": "UFPE",
            "shift": "Manhã",
            "telephone": "(81) 99999-9999",
            "blood_type": "O+",
            "bus": "123"
        }
        
        with pytest.raises(ValidationError):
            Student(**invalid_data)
    
    def test_empty_strings_are_rejected(self, empty_student_data):
        """
        Teste com strings vazias - deve levantar ValidationError.
        Após adicionar Field(min_length=1), strings vazias são rejeitadas.
        """
        with pytest.raises(ValidationError) as exc_info:
            Student(**empty_student_data)
        
        # Verifica que TODOS os campos obrigatórios falharam na validação
        errors = exc_info.value.errors()
        assert len(errors) == 8  # 8 campos obrigatórios
        
        # Verifica que o erro é do tipo 'string_too_short'
        for error in errors:
            assert error['type'] == 'string_too_short'
    
    def test_extra_fields_ignored(self, valid_student_data):
        """Teste que campos extras são ignorados (comportamento padrão Pydantic)."""
        data_with_extra = valid_student_data.copy()
        data_with_extra["extra_field"] = "ignored"
        
        student = Student(**data_with_extra)
        
        # Não deve ter o campo extra
        assert not hasattr(student, "extra_field")
    
    def test_photo_can_be_none(self, valid_student_data):
        """Teste que photo pode ser explicitamente None."""
        data = valid_student_data.copy()
        data["photo"] = None
        
        student = Student(**data)
        assert student.photo is None
    
    def test_photo_can_be_omitted(self, valid_student_data):
        """Teste que photo pode ser omitido do dict."""
        data = valid_student_data.copy()
        del data["photo"]
        
        student = Student(**data)
        assert student.photo is None
