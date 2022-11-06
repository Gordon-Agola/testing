# import the necessary packages
from flask import Flask, render_template, Response,redirect,flash,url_for,request,jsonify
# from camera import VideoCamera
from datetime import datetime

import pandas as pd
import numpy as np
# from PIL import Image
# import cv2

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def hours(x):
    print(x['Time Out'])
    if(len(str(x['Time Out']))>5 ):
        t1 = datetime.strptime(str(x['Time In']), "%H:%M:%S")
            
            
        t2 = datetime.strptime(str(x['Time Out']), "%H:%M:%S")
            

            # get difference
        delta = t2 - t1
        seconds = delta.total_seconds() % (24 * 3600)
        hour = seconds // 3600
    else:
        hour = 0
    
    return hour

@app.route('/')
def index():
    data = pd.read_csv("Attendance/Attendance.csv")
    fill_date = datetime.today().strftime('%d-%m-%Y')
    data1=data[data['Date']==str(fill_date)]
    
    
    return data1
# def gen(camera):
#     while True:
#         #get camera frame
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



# @app.route('/register', methods =['GET', 'POST'])
# @cross_origin(origins={"http://localhost:8080"})
# def register():
#     msg = ''
#     if request.method == 'POST' and 'fname' in request.form and 'national' in request.form:
#         name= request.form['fname']
#         id= request.form['national']
#         video = VideoCamera()
#         video.TakeImages(id,name)
#         video.TrainImages()
#     return render_template("reg_form.html")
# @app.route('/analysis', methods =['GET', 'POST'])
# @cross_origin(origins={"http://localhost:8080"})
# def analysis():
#     msg = ''
#     if request.method == 'POST' and 'fname' in request.form and 'national' in request.form:
#         name= request.form['fname']
#         id= request.form['national']
#         video = VideoCamera()
#         video.TakeImages(id,name)
#         video.TrainImages()
#     return render_template("analysis.html")
        
# @app.route('/login', methods =['GET', 'POST'])
# @cross_origin(origins={"http://localhost:8080"})
# def login():
#     msg = ''
#     if request.method == 'POST' and 'pass' in request.form and 'national' in request.form:
#         pas= request.form['pass']
#         id= request.form['national']
#         print(id)
#         print(pas)
#         if pas==str(123) and id =='1':
#             return redirect(url_for('register'))
#         elif pas == str(456) and id == '2':
#             return redirect(url_for('analysis'))
#     return redirect(url_for('index'))
        
        

# @app.route('/api/attendance')
# @cross_origin(origins={"http://192.168.0.243:8080"})
# def attendance():
#     video = VideoCamera()
#     resp = video.TrackImages()
#     if(resp is not None):
#         return resp
#     return "Attendend successfully"
# @app.route('/api/attendance/list')
# @cross_origin(origins={"http://192.168.0.243:8080"})
# def attendancelist():
#     data = pd.read_csv("Attendance/Attendance.csv")
#     fill_date = datetime.today().strftime('%d-%m-%Y')
#     data1=data[data['Date']==str(fill_date)]
#     dic = data1.to_dict('records')
#     print(jsonify(dic))
#     print("hello")
#     return jsonify(dic)

# @app.route('/api/attendance/analysis')
# @cross_origin(origins={"http://192.168.0.243:8080"})
# def attendanceanalysis():
    
#     data = pd.read_csv("Attendance/Attendance.csv")
#     if(data.shape[0] >0):
#         data['Hour']=data.apply(lambda x:hours(x),axis=1)
#         data = data[['Name','Hour']].groupby('Name',as_index=False).sum()
       
#     else:
#         # initialize list of lists
#         data = [['Non came', 0], ['nick', 0]]
        
#         # Create the pandas DataFrame
#         data = pd.DataFrame(data, columns=['Name', 'Hour'])
#         print("no data")    
#     dic = {}
#     dic["Name"] =data['Name'].tolist()
#     dic["Hour"] = data['Hour'].tolist()
#     print(jsonify(dic))
#     print("hello")
#     return jsonify(dic)



 
if __name__ == '__main__':
    # defining server ip address and port
    app.run()