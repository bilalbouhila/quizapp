from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import sqlite3
import random
import json
import os
import secrets
import html

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)

# SQLite connection
db_string = "questions.db"

def load_data():
    conn = sqlite3.connect(db_string)
    df = pd.read_sql_query("SELECT question_number FROM questions", conn)
    questions_list = df.to_dict('records')
    return questions_list



# @app.route('/start')
# def start():
#     session.clear()  # This will clear the session
#     session['questions'] = load_data()  # Reload the questions data
#     return redirect(url_for(home, questions=questions))  # Redirect to the first question
# @app.route('/is-question-ready')


@app.route('/', methods=['GET', 'POST'])
def home():
    session.clear()
    session['score'] = 0
    questions = load_data()
    if request.method == 'POST':
        num_questions_str = request.form.get('num_questions')
        mode = request.form.get('mode')  # get the mode
        session['questions'] = questions
        if mode == 'exam':
            # Exam mode: shuffle the questions and select a subset
            random.shuffle(questions)
            if not num_questions_str:
                session['questions'] = questions
            else:
                num_questions = int(num_questions_str)
                if num_questions > len(questions):
                    num_questions = len(questions)
                session['questions'] = random.sample(questions, num_questions)
        elif mode == 'training':
            # Training mode: select a range of questions without shuffling
            start_range_str = request.form.get('start_range')
            start_range = int(start_range_str) - 1 if start_range_str else 0  # if the field is left blank, we start from the first question (0 index)
            end_range = start_range + int(num_questions_str) if num_questions_str else len(questions)  # calculate the end range based on the number of questions, or use the end of the list if no number is provided

            session['questions'] = questions[start_range:end_range]  # select the range of questions
        # delete wrong_answers.json file if it exists
        if os.path.exists('wrong_answers.json'):
            os.remove('wrong_answers.json')

        return redirect(url_for('quiz', question_number=0))

    return render_template('index.html', questions=questions)



@app.route('/question/<int:question_number>', methods=['GET', 'POST'])
def quiz(question_number):

    # # Check if 'questions' is in the session
    # if 'questions' not in session:
    #     # If not, redirect to the main page (or any page you want)
    #     print
    #     return redirect(url_for('home'))
    conn = sqlite3.connect(db_string)
    number_question = session['questions'][question_number]["question_number"]
    query = "SELECT * FROM questions where question_number = {}".format(number_question)
    df = pd.read_sql_query(query, conn)
    question = df.to_dict('records')[0]
    question = html.unescape(question)
    question['answers'] = [question['answer1'], question['answer2'], question['answer3'], question['answer4'], question['answer5'], question['answer6']]
    question['answers'] = [answer for answer in question['answers'] if answer != '']  # remove empty answers

    if request.method == 'POST':
        # User submitted answer, store in session
        answer = request.form.getlist('answer')
        session[str(question_number)] = answer 
        user_answer = session.get(str(question_number), [])
        correct_answer = str(question['correct']).split('|')
        if set(user_answer) == set(correct_answer):
            session['score'] =session['score'] + 1

        # Go to correction page
        return redirect(url_for('correction', question_number=question_number))

    return render_template('quiz.html', question=question, question_number=question_number, questions=session['questions'])


@app.route('/correction/<int:question_number>', methods=['GET', 'POST'])
def correction(question_number):

    conn = sqlite3.connect(db_string)
    number_question = session['questions'][question_number]["question_number"]
    query = "SELECT * FROM questions where question_number = {}".format(number_question)
    df = pd.read_sql_query(query, conn)
    question = df.to_dict('records')[0]
    question = html.unescape(question)
    user_answer = session.get(str(question_number), [])
    correct_answer = str(question['correct']).split('|')
    question['answers'] = [question['answer1'], question['answer2'], question['answer3'], question['answer4'], question['answer5'], question['answer6']]
    question['answers'] = [answer for answer in question['answers'] if answer != '']  # remove empty answers
    print(user_answer)
    print(correct_answer)
    if request.method == 'POST':
        # Write all answers to the file
        if user_answer != []: 
            for answer in user_answer:
                if answer not in correct_answer:
                    with open('wrong_answers.json', 'a') as f:
                        json.dump({
                            'question_number': question['question_number'],
                            'question': question['question_text'],
                            'user_answer': user_answer,  # store as list
                            'correct_answer': correct_answer,  # store as list
                            'Explanation' : question['explanation'],
                            'All options' : question['answers']   # Write all answer options to the file
                        }, f)
                        f.write('\n')
        else:
            with open('wrong_answers.json', 'a') as f:
                json.dump({
                    'question_number': question['question_number'],
                    'question': question['question_text'],
                    'user_answer': user_answer,  # store as list
                    'correct_answer': correct_answer,  # store as list
                    'Explanation' : question['explanation'],
                    'All options' : question['answers']   # Write all answer options to the file
                }, f)
                f.write('\n')

        if question_number < len(session['questions']) - 1:
            return redirect(url_for('quiz', question_number=question_number + 1))
        else:
            # All questions answered, calculate score and display results
            

            answers = []
            with open('wrong_answers.json', 'r') as f:
                for line in f:
                    answer = json.loads(line)
                    answers.append(answer)

            
            percent = (session['score'] / len(session['questions'])) * 100
            return render_template('results.html', score=session['score'] , total=len(session['questions']), percent=percent, answers=answers)
    return render_template('correction.html', question=question, user_answer=user_answer, correct_answer=correct_answer)


if __name__ == '__main__':
    app.run(debug=True)
