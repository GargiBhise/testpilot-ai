from fastapi import FastAPI

app = FastAPI(title="TestPilot AI", version="0.1.0")

@app.get("/")
def root():
    return {"message": "TestPilot AI Backend Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}