import pandas as pd
import pickle
import json
import requests
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def create_model(outfile):
    id = []
    cgpa = []
    sl_score = []
    mc_score = []
    p_contest = []
    cf_practice = []
    kaggle_practice = []
    sh_per_day = []
    number_of_internship = []
    job_role = []
    specialization = []
    completed_projects = []

    requests.post("http://127.0.0.1:5000/init", json={'file_name': 'student.csv'})
    raw_data = json.loads(requests.get("http://127.0.0.1:5000/get_all_data").text)
    for i in range(1, len(raw_data)):
        id.append(int(raw_data[i]["id"]))
        cgpa.append(float(raw_data[i]["cgpa"]))
        sl_score.append(int(raw_data[i]["sl_score"]))
        mc_score.append(int(raw_data[i]["mc_score"]))
        p_contest.append(int(raw_data[i]["p_contest"]))
        cf_practice.append(int(raw_data[i]["cf_practice"]))
        kaggle_practice.append(int(raw_data[i]["kaggle_practice"]))
        sh_per_day.append(int(raw_data[i]["sh_per_day"]))
        number_of_internship.append(int(raw_data[i]["number_of_internship"]))
        job_role.append(raw_data[i]["job_role"])
        specialization.append(raw_data[i]["specialization"])
        completed_projects.append(int(raw_data[i]["completed_projects"]))

    df = pd.DataFrame(
        data={ "id": id, "cgpa": cgpa, "sl_score": sl_score, "mc_score": mc_score,
         "p_contest": p_contest, "cf_practice": cf_practice,
         "kaggle_practice": kaggle_practice, "sh_per_day": sh_per_day,
          "number_of_internship": number_of_internship, "job_role": job_role, 
         "specialization": specialization, "completed_projects": completed_projects,
        },
    )
    label_encoder = preprocessing.LabelEncoder()
    print (df['specialization'].unique())
    df["specialization"] = label_encoder.fit_transform(df["specialization"])
    print(df["specialization"])
   
    job_role_x = df.drop(columns=["job_role"])  # all data without job role
    job_role_y = df["job_role"]  # Only the job role colum

    X_train, X_test, y_train, y_test = train_test_split(
        job_role_x,
        job_role_y,
        test_size=0.3,
        random_state=2,
    )

    X_train = X_train.fillna(X_train.mean())
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    print (accuracy_score(y_test, y_pred))

    pickle.dump(rf, open(outfile, "wb"))

create_model("model.pkl")