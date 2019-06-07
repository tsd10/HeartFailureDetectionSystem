import os
from flask_sqlalchemy import SQLAlchemy
from flask import request,Flask, render_template, url_for, flash, redirect, send_from_directory
from forms import RegistrationForm, LoginForm, MyLoginForm
from plot import do_plot
from flask import Flask, send_file, make_response 
import urllib.request
import json
from flask_bootstrap import Bootstrap
import pickle
import re
import numpy as np
from numpy import array

app = Flask(__name__)


app.config['SECRET_KEY']= 'c698baeb61c95d216dc24d8254331da1'
app.config['SQLALCHEMY_DATABASE_URI']='/sqlite:///site.db'

db=SQLAlchemy(app)

posts=[
    {
        'author':'Tushar Deshpande',
        'title':'Blog Posts',
        'content':'First-post-content',
        'date_posted':'4 May,2019'
    },
    {
        'author':'Tush Deshpande',
        'title':'Blog Post 2',
        'content':'Second-post-content',
        'date_posted':'5 May,2019'
    }
		
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title='about')

@app.route("/home2")
def home2():
	return redirect(url_for('static',filename='Login/home.html'))

@app.route("/register",methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
    	flash(f'Account created for {form.username.data}!','success')
    	return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)

@app.route("/register2")
def register2():
    form2=LoginForm()
    # if form2.validate_on_submit():
    # 	flash(f'Account created for {form.username.data}!','success')
    # 	return redirect(url_for('home2'))
    return render_template('register2.html')


@app.route("/login",methods=['GET','POST'])
def login():
    lform=LoginForm()
    flash('Enter success')
    if lform.validate_on_submit():
        if lform.email.data == "admin@blog.com" and lform.password.data == "password":
            flash('You have been logged in!','success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful.Please check username and password','danger')
    return render_template('login.html', title='Login', form=lform)


@app.route("/test",methods=['GET','POST'])
def test():
    test=MyLoginForm()
    if test.validate_on_submit():
       	if test.username.data == 'admin@abc.com' and test.password.data == "password":
       		flash('You have been logged in!','success')
       		return redirect(url_for('blackboard'))
       	else:
          	flash('Login Unsuccessfull.Please check username and password','danger')
    return render_template('test.html',title='Register',form=test)


@app.route("/blackboard",methods=['GET','POST'])
def blackboard():
	return render_template('blackboard.html')

@app.route("/hf_detect",methods=['GET','POST'])
def hf_detect():
    #hf_dt=hf_d()
    return render_template('hf_detect.html')

@app.route("/hf_d",methods=['POST'])
def move_forward():
    input1=hf_detect()
    if request.method=='POST':
        avghbt=request.form['avghbt']
        palpd=request.form['palpd']
        BMI=request.form['BMI']
        age=request.form['age']
        cholestrol=request.form['cholestrol']
        exercise=request.form['exercise']
        if request.form.get('smoker'):
            smoker="Y"
        else:
            smoker="N"
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
        #result = response.read()
        result = response.read()
        print("**************") 
        mystr = result.decode("utf8")
        print(mystr)
        test=mystr.find('Labels')
        print(test)
        test=test+9
        scored_label=mystr[test]
        #scored_probabilities=mystr[]
        test2=mystr.find('Probabilities')
        print("Index of prob")
        print(test2)
        scored_probabilities=""
        index_test2=test2+16
        index_till=index_test2+7
        for i in range(index_test2,index_till):
            scored_probabilities+=mystr[i]
        print("THe scored label is:")
        print(mystr[184])
        print("THe scored probability is:")
        print(scored_probabilities)
        print(test)
        print("SEE ABOVE")
        # if type(result) == str:
        #     result=1
        # else:
        #     result=0
        # print(result)
        #print(result.Results)
        print(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))
    return render_template('result.html',i=1,prediction_text=result,label=scored_label,probability=scored_probabilities)

    

@app.route("/hf_type",methods=['GET','POST'])
def hf_type():
    #hf_dt=hf_d()
    return render_template('hf_type.html')


@app.route("/hf_t",methods=['POST'])
def hf_t():
    if request.method=='POST':
        pa_s=request.form['pa_s']
        pa_s=int(re.search(r'\d+',pa_s).group())
        pa_d=request.form['pa_d']
        pa_d=int(re.search(r'\d+',pa_d).group())
        hr=request.form['hr']
        hr=int(re.search(r'\d+',hr).group())
        weight=request.form['weight']
        weight=int(re.search(r'\d+',weight).group())
        NYHA=request.form['NYHA']
        NYHA=int(re.search(r'\d+',NYHA).group())
        BNP=request.form['BNP']
        BNP=int(re.search(r'\d+',BNP).group())
        ef=request.form['ef']
        ef=int(re.search(r'\d+',ef).group())
        age=request.form['age']
        age=int(re.search(r'\d+',age).group())
        if request.form.get('sex'):
            sex=0
        else:
            sex=1
        if request.form.get('fib_atr'):
            fib_atr=1
        else:
            fib_atr=0
        if request.form.get('bloc_bran'):
            bloc_bran=1
        else:
            bloc_bran=0
        if request.form.get('tan_ventr'):
            tan_ventr=1
        else:
            tan_ventr=0  
        final_model='/home/tushar/Heart_Failure_BE_Project/Final/Heart_Failure_Evaluation-Type_OF_HF/final_model.sav'              
        final_score='/home/tushar/Heart_Failure_BE_Project/Final/Heart_Failure_Evaluation-Type_OF_HF/final_score.sav'
        loaded_model = pickle.load(open(final_model, "rb"))
        with open(final_score, "rb") as f:
            var_you_want_to_load_into = pickle.load(f)
        example_measures = np.array([[pa_s,pa_d,hr,weight,BNP,NYHA,ef,sex,age,fib_atr,bloc_bran,tan_ventr]])
        example_measures = example_measures.reshape(len(example_measures), -1)
        prediction = loaded_model.predict(example_measures)
        print(prediction)
        acc_1=round(var_you_want_to_load_into[0],3)
        acc_2=round(var_you_want_to_load_into[1],3)
        #pa_s,pa_d,hr,weight,BNP,NYHA,EF,sex,age,fib_atr,bloc_bran,tac_ventr
    return render_template('result.html',result=prediction,i=2,acc1=acc_1,acc2=acc_2,accuracy=var_you_want_to_load_into)

@app.route("/result",methods=['GET','POST'])
def result():
    #hf_dt=hf_d()
    return render_template('result.html')

@app.route("/hf_detect_cnn")
def hf_cnn():
    return render_template('hf_detect_cnn.html')


@app.route("/hf_cnn_t",methods=['GET','POST'])
def hf_cnn_t():
    if request.method=='POST':
        t_input=request.form['t_input']
        t_input=int(re.search(r'\d+',t_input).group())
        final_model='/home/tushar/final_model.sav' 
        loaded_model = pickle.load(open(final_model, "rb")) 
        test_data_file='/home/tushar/full_datafile.sav'
        with open(test_data_file, "rb") as f:
            test_data = pickle.load(f)
        example_measures = test_data.iloc[t_input]
        X=example_measures
        example_measures=example_measures/255.0
        example_measures = example_measures.values.reshape(-1,500,1)
        y_pred_classes=loaded_model.predict_classes(example_measures)
        print(y_pred_classes)
        test=np.amax(X)
        print(test)
        print("SEE ABOVE")
        # Xnew = array([[test_data[t_input]]])
        # X=Xnew
        # Xnew = Xnew.reshape(-1,500,1)
        # # make a prediction
        # ynew = loaded_model.predict_classes(Xnew)
        # # show the inputs and predicted outputs
    return render_template('result.html',i=4,result=y_pred_classes,data=test,loop=500)



@app.route("/testing")
def testing():
	return render_template('testing.html')

@app.route("/hf_severity",methods=['GET','POST'])
def hf_severity():
    #hf_dt=hf_d()
    return render_template('hf_severe.html')


@app.route("/hf_s",methods=['GET','POST'])
def hf_s():
    if request.method=='POST':
        age=request.form['age']
        if type(age) == str:
            print(age)
        age=int(re.search(r'\d+',age).group())
        print(age)
        print("SEE AGE ABOVE")
        if request.form.get('sex'):
            sex=0
        else:
            sex=1
        cp=request.form['cp']
        cp=int(re.search(r'\d+',cp).group())
        trestbps=request.form['trestbps']
        trestbps=int(re.search(r'\d+',trestbps).group())
        cholestrol=request.form['cholestrol']
        cholestrol=int(re.search(r'\d+',cholestrol).group())
        fbs=request.form['fbs']
        fbs=int(re.search(r'\d+',fbs).group())
        restecg=request.form['restecg']
        restecg=int(re.search(r'\d+',restecg).group())
        thalach=request.form['thalach']
        thalach=int(re.search(r'\d+',thalach).group())
        if request.form.get('exang'):
            exang=1
        else:
            exang=0
        oldpeak=request.form['oldpeak']
        oldpeak=int(re.search(r'\d+',oldpeak).group())
        slope=request.form['slope']
        slope=int(re.search(r'\d+',slope).group())
        ca=request.form['ca']
        ca=int(re.search(r'\d+',ca).group())
        thal=request.form['thal']
        thal=float(re.search(r'\d+',thal).group())
        filename='/home/tushar/Heart_Failure_BE_Project/Final/HeartFailurePrediction-severity_of_hf/HeartFailurePrediction-master/finalized_model.sav'
        datafile='/home/tushar/Heart_Failure_BE_Project/Final/HeartFailurePrediction-severity_of_hf/HeartFailurePrediction-master/datafile.sav'
        sc_classifier='/home/tushar/Heart_Failure_BE_Project/Final/HeartFailurePrediction-severity_of_hf/HeartFailurePrediction-master/sc_transform.sav'
        loaded_model = pickle.load(open(filename, "rb"))
        sc = pickle.load(open(sc_classifier, "rb"))
        sample_patient = sc.transform(np.array([[age,sex,cp,trestbps,cholestrol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]]))
        with open(datafile, "rb") as f:
            var_you_want_to_load_into = pickle.load(f)
        #test=array([[54,1,4,168,350,0,2,167,1,2.8,2,2,7]])       
        s_result = loaded_model.predict(sample_patient)
        print(s_result*100)    
        test=np.amax(s_result)
        print("SEE BELOW")
        print(test)
    return render_template('result.html',s_label=s_result*100,i=3,c_test=test)


@app.route('/plots/breast_cancer_data/correlation_matrix', methods=['GET'])
def correlation_matrix():
    bytes_obj = do_plot()
    
    return send_file(bytes_obj,
                     attachment_filename='plot.png',
                     mimetype='image/png')
    return render_template('test.html')


 
if __name__== '__main__':
 	app.run(debug=True)   

