from flask import Flask, render_template, request, redirect, url_for, flash, session
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"


# Route for the root page
@app.route('/')
def index():
  session["responses"] = []
  survey_title = satisfaction_survey.title
  instructions = satisfaction_survey.instructions
  return render_template('index.html', title=survey_title, instructions=instructions)


# Route for handling questions
@app.route('/questions/<int:question_number>', methods=['GET', 'POST'])
def question(question_number):
  responses = session.get("responses", [])
  
  if len(responses) != question_number:
    # Trying to access questions out of order
    flash(f"Invalid question id: {question_number}.")
    return redirect(f"/questions/{len(responses)}")

  if question_number == len(satisfaction_survey.questions):
    # No more questions, redirect to the thank you page
    return redirect('/result')

  if request.method == 'POST':
    # Retrieve the answer from the form
    answer = request.form.get('answer')

    # Append the answer to the responses list
    responses.append(answer)
    session["responses"] = responses

    # Redirect to the next question
    return redirect(url_for('question', question_number=question_number + 1))

  # If it's a GET request, render the question template with the current question
  question_text = satisfaction_survey.questions[question_number].question
  return render_template('question.html', question_number=question_number, question_text=question_text)


# Route for the result page
@app.route('/result')
def result():
  responses = session.get("responses", [])
  responses_str = ', '.join(responses)  # Convert the responses list to a string
  return render_template('result.html', responses=responses_str, title=satisfaction_survey.title)


if __name__ == '__main__':
  app.run()

