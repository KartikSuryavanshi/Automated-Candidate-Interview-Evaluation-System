from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "ARIES Automated Candidate Interview & Evaluation System is running."}
