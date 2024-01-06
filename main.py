from fastapi import FastAPI, Response
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)


@app.get("/")
def index():
    return {"testing": "testing"}
