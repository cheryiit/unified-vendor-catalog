from sqlalchemy.orm import Session
from app.domain.entities.product import Product

class PostgreSQLRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_product(self, product: Product):
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get_product(self, product_id: int):
        return self.session.query(Product).filter(Product.id == product_id).first()

    def update_product(self, product: Product):
        self.session.commit()
        self.session.refresh(product)
        return product

    def delete_product(self, product_id: int):
        product = self.get_product(product_id)
        if product:
            self.session.delete(product)
            self.session.commit()
        return product