from fastapi import FastAPI

app = FastAPI(title="MedBooking API")


@app.get("/")
def root():
    return {"message": "MedBooking API is running"}