import uvicorn
from fastapi import FastAPI

from config.config import settings
from routes import router


app = FastAPI(
    title="AI-creator",
    docs_url="/api/v1/swagger",)

app.include_router(router, prefix = '/api/v1')

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True
    )