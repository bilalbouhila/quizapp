#Flask Quiz Application
#Introduction
This Flask application allows users to take quizzes. The questions are fetched from an SQLite database, and the user's responses are tracked throughout the session. At the end of the quiz, users can see their score and review the questions they got wrong.

#Features
Home Page with Quiz Configuration: Users can choose the mode (exam or training) and specify the number of questions they want to answer.
Quiz Page: Displays the questions one by one, allowing users to submit their answers.
Correction Page: After answering each question, users can see the correct answer and their response.
Results Page: At the end of the quiz, users will see their total score, percentage, and a review of the questions they got wrong.
#How to Use
Clone the Repository: First, clone this repository to your local machine using git clone [repository-url].
Install Dependencies: Navigate to the project directory and run pip install -r requirements.txt to install all required libraries.
Run the Application: In the project directory, execute python app.py. This will start the Flask development server.
Access the App: Open your browser and navigate to http://127.0.0.1:5000/ to access the home page of the app.
#How to Change the Database
Using questions.csv
The primary way to manage quiz questions is through the questions.csv file. This file provides an easy way to add, modify, or delete quiz questions.

##Schema
The schema for the questions.csv file is as follows:

Question_number:	A unique identifier for each question.
Question : 	The actual question text.
NumCorrect :	Number of correct answers (1 for single choice questions, >1 for multiple).
Answer1-Answer6:The potential answers for the question. At most 6 answers are allowed.
Correct:	The text of the correct answer(s). Multiple correct answers are separated by a |
Explanation:	An explanation for the correct answer, if applicable.
#Guidelines for Modifying questions.csv
Adding Questions: Simply add a new row at the end of the CSV file. Ensure that you maintain the schema format.
Deleting Questions: Delete the entire row corresponding to the question you wish to remove.
Modifying Questions: Edit the relevant row in the CSV file.
Answer Limit: If a question has fewer than 6 possible answers, leave the excess "Answer" columns empty. If you have more than 6 potential answers, only include the first 6 and adjust the question accordingly.
Multiple Correct Answers: If there's more than one correct answer, make sure NumCorrect reflects the correct count, and use a | (pipe) to separate the correct answers in the Correct column.
##Updating the SQLite Database
After making changes to the questions.csv file, you'll need to update the SQLite database (questions.db) to reflect these changes. You can achieve this by importing the CSV data into SQLite usint init_db.py

By running this script, you'll replace the data in the questions.db SQLite database with the updated data from the questions.csv file.

#Contributing
Feel free to fork this repository, make changes, and submit pull requests. Feedback and contributions are always welcome!
