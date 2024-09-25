from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.adapters.repositories.sqlite_repository import SQLiteRepository
from app.domain.use_cases.get_product import GetProductUseCase
from app.adapters.message_queue.kafka_producer import KafkaProducer
from app.core.config import settings
import json

router = APIRouter()
kafka_producer = KafkaProducer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/products")
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repository = SQLiteRepository(db)
    products = repository.get_products(skip=skip, limit=limit)
    return products

@router.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    repository = SQLiteRepository(db)
    use_case = GetProductUseCase(repository)
    product = use_case.execute(product_id)
    
    if product:
        kafka_producer.send_message(
            settings.KAFKA_TOPIC,
            str(product.id),
            json.dumps({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price
            })
        )
    
    return product