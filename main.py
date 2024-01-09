from fastapi import FastAPI, Response
from mangum import Mangum
from sentence_transformers import SentenceTransformer, util
from pydantic import BaseModel

app = FastAPI()
handler = Mangum(app)


class SimilarAnswer(BaseModel):
    expected_answer: str
    given_answer: str


@app.get("/")
def index():
    return {"testing": "testing"}


# get score
@app.post("/answer")
def get_score(similaranswer: SimilarAnswer, response: Response):
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode([similaranswer.expected_answer, similaranswer.given_answer], convert_to_tensor=True)
        cosine_score = util.pytorch_cos_sim(embeddings[0], embeddings[1])
        similarity_score = cosine_score.item()
        print(f"Similarity Score for Answers: {similarity_score}")
        return {"Similarity Score for Answers":similarity_score}
    except Exception as e:
        print(e)
        response.status_code = 500
        return {"message": "something went wrong"}



