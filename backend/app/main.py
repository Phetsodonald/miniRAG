from app.api.documents import router as documents_router
from fastapi import FastAPI

app = FastAPI(
	title="MiniRAG",
	description="A lightWeight Retrieval Aujumented Generation application",
	version="1.0.0"
)

app.include_router(documents_router)

@app.get("/")
def root():
	return {
		"message": "welcome to MiniRAG API",
		"status": "running"
	}



@app.get("/health")
def health_check():
	return {
		"status": "Healthy"
	}
