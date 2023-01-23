# import the necessary packages
from flask import Flask, render_template, Response,redirect,flash,url_for,request,jsonify
from camera import VideoCamera
from datetime import datetime
from flask_socketio import SocketIO, emit
from io import StringIO 
import io
import base64
import imutils
import pandas as pd
import numpy as np
from PIL import Image
import cv2
from flask_cors import CORS,cross_origin
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
cors = CORS(app,resources={r'/*':{"origins":'*'}})
socketio = SocketIO(app)

def hours(x):
    
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
    
    
    return render_template('index.html',column_names=data1.columns.values, row_data=list(data1.values.tolist()))
def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



@app.route('/register', methods =['GET', 'POST'])
@cross_origin(origins={"http://192.168.0.28:8080"})
def register():
    msg = ''
    if request.method == 'POST':
        name= request.get_json().get("fname")
        id= request.get_json().get("national")
        video = VideoCamera()
        video.TakeImages(id,name)
        video.TrainImages()
        return "Name: "+str(name)+"\nID: "+str(id)
    return "not correct"
@app.route('/analysis', methods =['GET', 'POST'])
@cross_origin(origins={"http://192.168.0.28:8080"})
def analysis():
    msg = ''
    if request.method == 'POST' and 'fname' in request.form and 'national' in request.form:
        name= request.form['fname']
        id= request.form['national']
        video = VideoCamera()
        video.TakeImages(id,name)
        video.TrainImages()
    return render_template("analysis.html")
        
@app.route('/login', methods =['GET', 'POST'])
@cross_origin(origins={"http://192.168.0.28:8080"})
def login():
    msg = ''
    if request.method == 'POST' and 'pass' in request.form and 'national' in request.form:
        pas= request.form['pass']
        id= request.form['national']
        print(id)
        print(pas)
        if pas==str(123) and id =='1':
            return redirect(url_for('register'))
        elif pas == str(456) and id == '2':
            return redirect(url_for('analysis'))
    return redirect(url_for('index'))
        
        

@app.route('/api/attendance')
@cross_origin(origins={"http://192.168.0.28:8080"})
def attendance():
    video = VideoCamera()
    resp = video.TrackImages()
    if(resp is not None):
        return resp
    return "Attendend successfully"
@app.route('/api/attendance/list')
@cross_origin(origins={"http://192.168.0.28:8080"})
def attendancelist():
    data = pd.read_csv("Attendance/Attendance.csv")
    fill_date = datetime.today().strftime('%d-%m-%Y')
    data1=data[data['Date']==str(fill_date)]
    dic = data1.to_dict('records')
    print(jsonify(dic))
    print("hello")
    return jsonify(dic)

@app.route('/api/filter/attendance/list')
@cross_origin(origins={"http://192.168.0.28:8080"})
def filterattendancelist():
    data = pd.read_csv("Attendance/Attendance.csv")
    dic = data.to_dict('records')
    
    return jsonify(dic)

@app.route('/api/attendance/analysis')
@cross_origin(origins={"http://192.168.0.28:8080"})
def attendanceanalysis():
    date= request.get_json().get("date")
    
    print(date)
    
    data = pd.read_csv("Attendance/Attendance.csv")
    if(data.shape[0] >0):
        data['Hour']=data.apply(lambda x:hours(x),axis=1)
        data = data[['Name','Hour']].groupby('Name',as_index=False).sum()
       
    else:
        # initialize list of lists
        data = [['Non came', 0], ['nick', 0]]
        
        # Create the pandas DataFrame
        data = pd.DataFrame(data, columns=['Name', 'Hour'])
        print("no data")    
    dic = {}
    dic["Name"] =data['Name'].tolist()
    dic["Hour"] = data['Hour'].tolist()
    
    return jsonify(dic)
@app.route('/test')
def test():
    cap = cv2.VideoCapture("./RecordedVideo.webm")
    if (cap.isOpened()== False):
        msg = "No"
    # Give a error message
    

    # Read until video is completed
    while(cap.isOpened()):
        msg = "Yes"
        
    # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
        # Display the resulting frame
            cv2.imshow('Frame', frame)
            
        # Press Q on keyboard to exit
            if cv2.waitKey(75) & 0xFF == ord('q'):
                break
    
    # Break the loop
        else:
            break
    return msg

@socketio.on('image')
@cross_origin(origins={"http://192.168.0.28:8080"})
def image(data_image):
    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    # Process the image frame
    frame = imutils.resize(frame, width=700)
    frame = cv2.flip(frame, 1)
    imgencode = cv2.imencode('.jpg', frame)[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData

    # emit the frame back
    emit('response_back', stringData)
 
if __name__ == '__main__':
    # defining server ip address and port
    app.run(host="0.0.0.0",port='5000', debug=True)