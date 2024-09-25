from sqlalchemy.orm import Session
from app.domain.entities.product import Product

class SQLiteRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_product(self, product_id: int):
        return self.session.query(Product).filter(Product.id == product_id).first()

    def get_products(self, skip: int = 0, limit: int = 100):
        return self.session.query(Product).offset(skip).limit(limit).all()

    def create_product(self, product: dict):
        db_product = Product(**product)
        self.session.add(db_product)
        self.session.commit()
        self.session.refresh(db_product)
        return db_product

    def update_product(self, product_id: int, product: dict):
        db_product = self.session.query(Product).filter(Product.id == product_id).first()
        for key, value in product.items():
            setattr(db_product, key, value)
        self.session.commit()
        self.session.refresh(db_product)
        return db_product