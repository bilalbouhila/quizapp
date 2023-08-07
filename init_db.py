from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import text
import numpy as np

db_string = "sqlite:///questions.db"  # Your SQLite database
engine = create_engine(db_string)

db = scoped_session(sessionmaker(bind=engine))

db.execute(text("DROP TABLE IF EXISTS questions"))
db.commit()

db.execute(text("""
    CREATE TABLE questions (
        id INTEGER PRIMARY KEY,
        question_number INTEGER,
        question_text TEXT,
        num_correct INTEGER,
        answer1 TEXT,
        answer2 TEXT,
        answer3 TEXT,
        answer4 TEXT,
        answer5 TEXT,
        answer6 TEXT,
        correct TEXT,
        explanation TEXT)
"""))
db.commit()

df = pd.read_csv('questions.csv', sep=';')
df = df.replace(np.nan, '', regex=True)  # Replace NaN values with empty string

for _, row in df.iterrows():
    db.execute(text("""
        INSERT INTO questions 
        (question_number, question_text, num_correct, answer1, answer2, answer3, answer4, answer5, answer6, correct, explanation)
        VALUES (:question_number, :question_text, :num_correct, :answer1, :answer2, :answer3, :answer4, :answer5, :answer6, :correct, :explanation)"""),
        {
            "question_number": row['Question_number'],
            "question_text": row['Question'],
            "num_correct": row['NumCorrect'],
            "answer1": row['Answer1'],
            "answer2": row['Answer2'],
            "answer3": row['Answer3'],
            "answer4": row['Answer4'],
            "answer5": row['Answer5'],
            "answer6": row['Answer6'],
            "correct": row['Correct'],
            "explanation": row['Explanation']
        })
    db.commit()

print("Data loaded successfully.")