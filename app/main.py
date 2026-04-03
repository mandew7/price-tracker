from fastapi import FastAPI

# Вот эта строчка ОБЯЗАТЕЛЬНО должна быть и называться именно app
app = FastAPI(title="Price Tracker API")

@app.get("/")
async def root():
    return {"message": "Welcome to Price Tracker SaaS API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}