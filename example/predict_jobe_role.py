from fileinput import filename
from flask import Flask,request,jsonify
import numpy as np
import pickle
from csv import reader
model = pickle.load(open('model.pkl','rb'))

app = Flask(__name__)


def read_data(filename, mode): # read data by giving the filename and the mode to read
    with open(filename,  mode) as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            # row variable is a list that represents a row in csv
            print(row)

       
@app.route('/')
def index():
    return "Hello world"

@app.route('/predict',methods=['POST'])
def predict():
    ID =  request.get_json()['ID']
    CGPA = request.get_json()['CGPA']
    SL_SCORE = request.get_json()['SL_SCORE']
    MC_SCORE = request.get_json()['MC_SCORE']
    P_CONTEST = request.get_json()['P_CONTEST']
    CF_PRACTICE = request.get_json()['CF_PRACTICE']
    KAGGLE_PRACTICE = request.get_json()['KAGGLE_PRACTICE']
    SH_PER_DAY = request.get_json()['SH_PER_DAY']
    NUMBER_OF_INTERNSHIP = request.get_json()['NUMBER_OF_INTERNSHIP']
    SPECIALIZATION = request.get_json()['Specialization']
    Completed_projects = request.get_json()['Completed_projects']

    jobs_tostring = ['No job', 'Data Scientist', 'App Developer', 'ML engineer',
       'Software Engineer', 'Data Analyst', 'Network Engineer',
       'Web Designer', 'Data Engineer', 'Web Developer',
       'Cyber Security Analyst', 'UI Designer', 'Backend Engineer',
       'DevOps Engineer', 'QA Engineer', 'MlOps Engineer',
       'FullStack Engineer', 'Frontend Developer', 'Security Engineer',
       'Data Architect']
    input_query = np.array([[ID, CGPA, SL_SCORE ,MC_SCORE, P_CONTEST, CF_PRACTICE, KAGGLE_PRACTICE ,SH_PER_DAY ,NUMBER_OF_INTERNSHIP ,SPECIALIZATION , Completed_projects ]])
    # print (input_query)
    # input_query = np.array([["1821881", "3.", SL_SCORE ,MC_SCORE, P_CONTEST, CF_PRACTICE, KAGGLE_PRACTICE ,SH_PER_DAY ,NUMBER_OF_INTERNSHIP ,Specialization  ,Completed_projects ]])

    result = model.predict(input_query)
    print(result)

    return jsonify({'Job Role':str(jobs_tostring[int(result)])})

if __name__ == '__main__':
    app.run(debug=True)

  #  ID CGPA SL_SCORE MC_SCORE P_CONTEST CF_PRACTICE KAGGLE_PRACTICE
#  SH_PER_DAY NUMBER_OF_INTERNSHIP JOB_ROLE  Specialization  Completed_projects

