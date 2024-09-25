from fastapi import FastAPI
from app.adapters.controllers import product_controller
from app.core.database import engine, Base
from app.core.sync_db import sync_sqlite_to_postgres
import threading
import time

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(product_controller.router)

def periodic_sync():
    while True:
        sync_sqlite_to_postgres()
        time.sleep(300)  # 5 dakikada bir senkronize et

# Senkronizasyon işlemini arka planda başlat
sync_thread = threading.Thread(target=periodic_sync, daemon=True)
sync_thread.start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)