from app.adapters.repositories.sqlite_repository import SQLiteRepository

class GetProductUseCase:
    def __init__(self, repository: SQLiteRepository):
        self.repository = repository

    def execute(self, product_id: int):
        return self.repository.get_product(product_id)