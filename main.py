from fastapi import FastAPI, Response, Request
from mangum import Mangum
from sentence_transformers import SentenceTransformer, util
from pydantic import BaseModel
import os
from boto3.session import Session
import whisper
import soundfile as sf
import numpy as np

os.environ['TRANSFORMERS_CACHE'] = '/tmp/cache'

session = Session(
    aws_access_key_id='AKIAZC3RQOWY7PYQKW5W',
    aws_secret_access_key='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',
    region_name='ap-southeast-2'
)

s3 = session.client('s3')

app = FastAPI()
handler = Mangum(app)


class SimilarAnswer(BaseModel):
    expected_answer: str
    file_name: str


@app.get("/")
def index():
    return {"testing": "testing"}


def get_text(file_name: str):
    try:
        s3_object = s3.get_object(Bucket="sagemakerquestions", Key=file_name)
        audio_stream = s3_object["Body"]

        # Download the audio file to a temporary location
        temp_file_path = f'/tmp/{file_name}'  # Replace with your temporary file path and format
        with open(temp_file_path, 'wb') as f:
            f.write(audio_stream.read())

        # Read the downloaded file using soundfile
        audio_data, sample_rate = sf.read(temp_file_path, dtype='float32')

        model = whisper.load_model("base")
        result = model.transcribe(temp_file_path, fp16=False)

        return result["text"]
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None


# get score
@app.post("/answer")
def get_score(similaranswer: SimilarAnswer, response: Response):
    try:
        transcribed_text = get_text(similaranswer.file_name)
        return {"Similarity Score for Answers": transcribed_text}
        # model = SentenceTransformer('all-MiniLM-L6-v2',cache_folder='/tmp/cache')
        # embeddings = model.encode([similaranswer.expected_answer, similaranswer.given_answer], convert_to_tensor=True)
        # cosine_score = util.pytorch_cos_sim(embeddings[0], embeddings[1])
        # similarity_score = cosine_score.item()
        # print(f"Similarity Score for Answers: {similarity_score}")
        # return {"Similarity Score for Answers": similarity_score}
    except Exception as e:
        print(e)
        response.status_code = 500
        return {"message": "something went wrong"}
