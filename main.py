from fastapi import FastAPI, Response, Request
from mangum import Mangum
from sentence_transformers import SentenceTransformer, util
from pydantic import BaseModel
import os
from typing import List

os.environ["TRANSFORMERS_CACHE"] = "/tmp/data"

app = FastAPI()
handler = Mangum(app)


# question class
class Question:
    def __init__(self, answer: str, expected: str):
        self.answer = answer
        self.expected = expected
        self.result = 0


# question Base model
class QuestionsAnswers(BaseModel):
    answer: str
    question: str
    expected: str


# questions Base model
class Questions(BaseModel):
    questions: List[QuestionsAnswers]


@app.get("/")
def index():
    return {"testing": "testing"}


def check_text(expected_answer: str, given_answer: str):
    model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='/tmp/data')
    embeddings = model.encode([expected_answer, given_answer], convert_to_tensor=True)
    cosine_score = util.pytorch_cos_sim(embeddings[0], embeddings[1])
    similarity_score = cosine_score.item()
    print(f"Similarity Score for : {similarity_score}")
    return similarity_score


# get score
@app.post("/answer")
def get_score(questions: Questions, response: Response):
    new_result = []
    try:
        for question in questions.questions:
            if question.answer:
                new_question = Question(question.answer, question.expected)
                new_question.result = check_text(question.expected,question.answer )
                new_result.append(new_question)
            else:
                response.status_code = 400
                return {"message": "no data found"}
        return {"message": new_result}

    except Exception as e:
        print(e)
        response.status_code = 500
        return {"message": "something went wrong"}
