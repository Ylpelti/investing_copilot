from app.core.errors.exceptions import NotFound
from typing import Generic, TypeVar, Type, Protocol

class HasId(Protocol):
    id: int

T = TypeVar("T", bound=HasId)

class BaseCrud(Generic[T]):
    model: Type[T]

    def __init__(self, db):
        self.db = db

    def get_by_id(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_id_or_404(self, id:int):
        record = self.get_by_id(id)
        if not record:
            raise NotFound()
        return record
    
    def delete_by_id(self, id:int, commit: bool = True) -> bool:
        record = self.get_id_or_404(id)
        self.db.delete(record)
        if commit:
            self.db.commit()
        return True
    

