from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import urllib.request
import json

class hf_d(FlaskForm):
    avghbt = StringField('avghbt',
                           validators=[DataRequired(), Length(min=2, max=20)])
    palpd = StringField('palpd',
                           validators=[DataRequired(), Length(min=2, max=20)])
    BMI = StringField('BMI',
                           validators=[DataRequired(), Length(min=2, max=20)])
    age = StringField('age',
                           validators=[DataRequired(), Length(min=2, max=20)])
    cholestrol = StringField('cholestrol',
                           validators=[DataRequired(), Length(min=2, max=20)])
    smoker = BooleanField('smoker')
    exercise = StringField('exercise',
                           validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Login')
    data = {
        "Inputs": {
                "input1":
                [
                    {
                            'AVGHEARTBEATSPERMIN': avghbt,   
                            'PALPITATIONSPERDAY': palpd,   
                            'CHOLESTEROL': cholestrol,   
                            'BMI': BMI,   
                            'AGE': age,   
                            'SMOKERLAST5YRS': smoker,   
                            'EXERCISEMINPERWEEK': exercise,   
                    }
                ],
        },
    "GlobalParameters":  {
    }
}

body = str.encode(json.dumps(data))

url = 'https://ussouthcentral.services.azureml.net/workspaces/e293e69595da4913a5ba4bb8bdc439a8/services/1df4e41d9fe6467e9ffcc2814d73f748/execute?api-version=2.0&format=swagger'
api_key = '6N2NLKFuV7HCGXzCuHslPlHVuxSJKPxjeihSY2hPRhEcYXxB8LfmziygDuUoguMHyhfEDl3IU1CA+4NJumc76g==' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(json.loads(error.read().decode("utf8", 'ignore')))