# PRECOGNITO
A Blockchain &amp; Machine Learning-Based Student Record Authentication System

# Table of Contents
1. [Introduction](#introduction)
2. [How to Install](#how-to-install)
3. [How to Use](#how-to-use)
4. [License](#license)


<a name="introduction"></a>
# Introduction
PreCogNito is a blockchain-based student record authentication system. It is a decentralized application that allows students to store their academic records on a blockchain network. The application uses a machine learning model to verify the authenticity of the records. The application is built using the Ethereum blockchain network and the machine learning model is built using the Python programming language.

<a name="installation"></a>
# How to Install
1. Clone the repository
2. Install the dependencies
3. Run the application

## 1. Clone the repository
Clone the repository using the following command:
```
git clone https://github.com/tahsinmurtaj16/PreCogNito.git
```

## 2. Install the dependencies
Install the dependencies using the following command:
```
cd PreCogNito
pip install -r requirements.txt
```

## 3. Run the application
Run the application using the following command:
```
cd api
python app.py
```

<a name="Usage"></a>
# How to Use

## 1. Load data into Blockchain Network
Load data into the blockchain network using the following command:

```bash
curl --location 'http://localhost:5000/predict' \
--data '{
    "id": 1828531,
    "cgpa": 3.4,
    "sl_score": 6,
    "mc_score": 5,
    "p_contest": 0,
    "cf_practice": 0,
    "kaggle_practice": 0,
    "sh_per_day": 10,
    "number_of_internship":2,
    "specialization": 2,
    "completed_projects": 4,
    "model": "rf"
}'
```

```json
{
    "Job Role": "['Network Engineer']"
}
```


A detailed description of the parameters is given below:

| Parameter | Description |
| :--- | :--- |
| `id` | The student ID |
| `cgpa` | The CGPA of the student |
| `sl_score` | The score of the student in the software lab |
| `mc_score` | The score of the student in the microprocessor lab |
| `p_contest` | The number of programming contests the student participated in |
| `cf_practice` | The number of problems the student solved on Codeforces |
| `kaggle_practice` | The number of problems the student solved on Kaggle |
| `sh_per_day` | The number of hours the student spends on self-study per day |
| `number_of_internship` | The number of internships the student has completed |
| `specialization` | The specialization of the student |
| `completed_projects` | The number of projects the student has completed |
| `model` | The machine learning model to be used for prediction |


# License

```txt

MIT License

Copyright (c) 2023 tahsinMurtaj16

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```