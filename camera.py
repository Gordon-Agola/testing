# import the necessary packages
import cv2,os,csv
import numpy as np
from PIL import Image
import datetime
import time
import pandas as pd
import shutil
# defining face detector
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
ds_factor=0.6
class VideoCamera(object):
    # def __init__(self):
    #    #capturing video
    #    self.video = 0
    
    # def __del__(self):
    #     #releasing camera
    #     self.video.release()
    def assure_path_exists(self,path):
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)
    def check_haarcascadefile(self):
        exists = os.path.isfile("haarcascade_frontalface_default.xml")
        if exists:
            pass
        else:
            return "Some file is missing contact admin"
        
    def TakeImages(self,Id,name):
        self.video = cv2.VideoCapture(0)
        self.check_haarcascadefile()
        columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
        self.assure_path_exists("StudentDetails/")
        self.assure_path_exists("TrainingImage/")
        serial = 0
        exists = os.path.isfile("StudentDetails\StudentDetails.csv")
        if exists:
            with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
                reader1 = csv.reader(csvFile1)
                for l in reader1:
                    serial = serial + 1
            serial = (serial // 2)
            csvFile1.close()
        else:
            with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(columns)
                serial = 1
            csvFile1.close()
        
        if ((name.isalpha()) or (' ' in name)):
            
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0
            while (True):
                ret, img = self.video.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    # display the frame
                    cv2.imshow('Taking Images', img)
                # wait for 100 miliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 100:
                    break
            self.video.release()
            cv2.destroyAllWindows()
            res = "Images Taken for ID : " + Id
            row = [serial, '', Id, '', name]
            with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            return res
            
        else:
            if (name.isalpha() == False):
                res = "Enter Correct name"
                return res

########################################################################################

    def TrainImages(self):
        self.check_haarcascadefile()
        self.assure_path_exists("TrainingImageLabel/")
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        faces, ID = self.getImagesAndLabels("TrainingImage")
        try:
            recognizer.train(faces, np.array(ID))
        except:
            
            return 'Please Register someone first!!!'
        recognizer.save("TrainingImageLabel\Trainner.yml")
        res = "Profile Saved Successfully"
        return res
    ############################################################################################3

    def getImagesAndLabels(self,path):
        # get the path of all the files in the folder
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        # create empth face list
        faces = []
        # create empty ID list
        Ids = []
        # now looping through all the image paths and loading the Ids and the images
        for imagePath in imagePaths:
            # loading the image and converting it to gray scale
            pilImage = Image.open(imagePath).convert('L')
            # Now we are converting the PIL image into numpy array
            imageNp = np.array(pilImage, 'uint8')
            # getting the Id from the image
            ID = int(os.path.split(imagePath)[-1].split(".")[1])
            # extract the face from the training image sample
            faces.append(imageNp)
            Ids.append(ID)
        return faces, Ids
    def TrackImages(self):
        self.check_haarcascadefile()
        self.assure_path_exists("Attendance/")
        self.assure_path_exists("StudentDetails/")
        
        msg = ''
        i = 0
        j = 0
        recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
        exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
        if exists3:
            recognizer.read("TrainingImageLabel\Trainner.yml")
        else:
            return 'Data Missing!!! Please click on Save Profile to reset data!!'
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)

        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ['Id',  'Name',  'Date',  'Time In', 'Time Out']
        exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
        if exists1:
            df = pd.read_csv("StudentDetails\StudentDetails.csv")
        else:
            cam.release()
            cv2.destroyAllWindows()
            
        while True:
            ret, im = cam.read()
            bb = 'Unknown'
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
                serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
                if (conf < 50):
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                    ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                    ID = str(ID)
                    ID = ID[1:-1]
                    bb = str(aa)
                    bb = bb[2:-2]
                    attendance = [str(ID), bb,  str(date),  str(timeStamp),' ']

                else:
                    Id = 'Unknown'
                    bb = str(Id)
                cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
            cv2.imshow('Taking Attendance', im)
            if (cv2.waitKey(1) == ord('q') or bb != 'Unknown'):
                cam.release()
                break
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
        exists = os.path.isfile("Attendance\Attendance.csv")
        if exists:
            with open("Attendance\Attendance.csv", 'a+') as csvFile1:
                df = pd.read_csv("Attendance\Attendance.csv")
                con = 0
                
                for index, row in df.iterrows():
                    
                    if(row['Name']==attendance[1] and str(row['Date'])==attendance[2]):
                        
                        
                        if(len(row['Time Out'])>3):
                            
                            con = 2
                            break
                        else:
                            df.loc[index,'Time Out'] = str(timeStamp)
                            con = 1
                            break
                if(con==1):
                    df.to_csv('file_name.csv',index=False)
                    shutil.move("file_name.csv", "Attendance\Attendance.csv")
                elif(con==2):
                    return   "You cant check out twice" 
                else:
                    writer = csv.writer(csvFile1)
                    writer.writerow(attendance)
            csvFile1.close()
        else:
            with open("Attendance\Attendance.csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(col_names)
                writer.writerow(attendance)
            csvFile1.close()
        with open("Attendance\Attendance.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            df1 = pd.read_csv("Attendance\Attendance.csv")
            
            
                        
        csvFile1.close()
        cam.release()
        cv2.destroyAllWindows()

    def show_img_to_ui(self, image):
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    def get_frame(self):
            #extracting frames
            self.video = cv2.VideoCapture(0)
            ret, frame = self.video.read()
            frame=cv2.resize(frame,None,fx=ds_factor,fy=ds_factor,
            interpolation=cv2.INTER_AREA)                    
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            face_rects=face_cascade.detectMultiScale(gray,1.3,5)
            for (x,y,w,h) in face_rects:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                break
            # encode OpenCV raw frame to jpg and displaying it
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()