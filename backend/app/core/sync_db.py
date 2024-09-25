from app.core.database import SessionLocal, PGSessionLocal
from app.domain.entities.product import Product
from sqlalchemy.orm import Session

def sync_sqlite_to_postgres():
    sqlite_session = SessionLocal()
    pg_session = PGSessionLocal()

    try:
        # SQLite'dan tüm ürünleri al
        sqlite_products = sqlite_session.query(Product).all()

        for sqlite_product in sqlite_products:
            # PostgreSQL'de ürünü ara
            pg_product = pg_session.query(Product).filter_by(id=sqlite_product.id).first()

            if pg_product:
                # Ürün varsa güncelle
                for attr, value in vars(sqlite_product).items():
                    if attr != '_sa_instance_state':
                        setattr(pg_product, attr, value)
            else:
                # Ürün yoksa yeni ürün oluştur
                new_pg_product = Product(**vars(sqlite_product))
                pg_session.add(new_pg_product)

        # Değişiklikleri kaydet
        pg_session.commit()

    except Exception as e:
        print(f"An error occurred during synchronization: {e}")
        pg_session.rollback()

    finally:
        sqlite_session.close()
        pg_session.close()

if __name__ == "__main__":
    sync_sqlite_to_postgres()