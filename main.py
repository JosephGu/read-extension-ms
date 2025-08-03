from os import name
from fastapi import FastAPI, status

app = FastAPI()


@app.get("/getBooks", status_code=status.HTTP_200_OK)
def root():
    return {
        "message": [
            {"series": "Harry Potter", "level": "1", "name": "Harry Potter and the Philosopher's Stone"},
            {"series": "Harry Potter", "level": "2",  "name": "Harry Potter and the Chamber of Secrets"},
            {"series": "Harry Potter", "level": "3",  "name": "Harry Potter and the Prisoner of Azkaban"},
            {"series": "The Lord of the Rings", "level": "1",  "name": "The Fellowship of the Ring"},
            {"series": "The Lord of the Rings", "level": "2",  "name": "The Two Towers"},
            {"series": "The Lord of the Rings", "level": "3",  "name": "The Return of the King"},
            {"series": "Hello World", "level": "3",  "name": "RAZ"},
        ]
    }
