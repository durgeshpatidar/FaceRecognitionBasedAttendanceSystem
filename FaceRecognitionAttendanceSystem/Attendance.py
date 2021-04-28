import tkinter as tk
from tkinter import *
import cv2,os,csv
import pandas as pd
import datetime
import time

window = tk.Tk()

window.title("Face_Recogniser")

#window.geometry('1300x700')

#for window background color
window.configure(background='white')

#for full screen window 
window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
message = tk.Label(window, text="Face-Recognition-Based-Attendance-Management-System" ,bg="Green"  ,fg="white"  ,width=45  ,height=3,font=('times', 30, 'italic bold underline')) 
message.place(x=150, y=20)

lbl3 = tk.Label(window, text="Attendance list: ",width=20  ,fg="red"  ,bg="white"  ,height=2 ,font=('times', 15, ' bold  underline')) 
lbl3.place(x=150, y=300)



message2 = tk.Label(window, text="" ,fg="red" ,justify=tk.RIGHT  ,bg="light cyan",activeforeground = "green",width=45 ,height=10  ,font=('times', 15, ' bold ')) 
message2.place(x=500, y=300)


def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel\Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("StudentDetails\StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names)    
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray,1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            print("id="+str(Id)+"  confidence="+str(conf))                                   
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
                aa=aa[0]
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                
            else:
                Id='Unknown'                
                tt=str(Id)  
            #if(conf > 75):
                #noOfFile=len(os.listdir("ImagesUnknown"))+1
                #cv2.imwrite("ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('attendance',im) 
        if (cv2.waitKey(1)==ord('q')):
            break
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    global fileName;
    fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName,index=False)
    cam.release()
    cv2.destroyAllWindows()
    print(attendance)
    res=attendance
    message2.configure(text=res)
    takeImg = tk.Button(window, text="View attendance", command=openf  ,fg="red"  ,bg="deep sky blue"  ,width=20  ,height=2, activebackground = "deep sky blue" ,font=('times', 15, ' bold '))
    takeImg.place(x=150, y=500)

def openf():
	os.system(fileName)

trackImg = tk.Button(window, text="Attendance", command=TrackImages  ,fg="red"  ,bg="yellow"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
trackImg.place(x=150, y=200)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="black"  ,bg="red"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=500, y=200)

copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0,font=('times', 20, 'italic bold underline'))
copyWrite.tag_configure("superscript", offset=10)
copyWrite.insert("insert", "Developed by: Durgesh Patidar")
copyWrite.configure(state="disabled",fg="red"  )
copyWrite.pack(side="left")
copyWrite.place(x=830, y=700)


window.mainloop()