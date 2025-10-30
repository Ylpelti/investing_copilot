from app.core.errors.exceptions import NotFound

class BaseCrud():
    model = None

    def __init__(self, db):
        self.db = db

    def get_by_id(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_id_or_404(self, id:int):
        record = self.get_by_id(id)
        if not record:
            raise NotFound()
        return record
    

