import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import csv
import numpy as np
from PIL import Image, ImageTk
import tkinter.ttk as ttk
from tkinter import messagebox
import tkinter.font as font

window = tk.Tk()
window.title("Face_Recogniser")
#for set window size 
#window.geometry('1300x700')

#for window background color
window.configure(background='white')

#for full screen window 
window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

messag = tk.Label(window, text="Face-Recognition-Based-Attendance-Management-System" ,bg="Green"  ,fg="white"  ,width=45  ,height=3,font=('times', 30, 'italic bold underline')) 

messag.place(x=150, y=20)

lbl = tk.Label(window, text="Enter scholar No",width=20  ,height=2  ,fg="red"  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
lbl.place(x=150, y=200)

txt = tk.Entry(window,width=20 ,bg="white" ,fg="red",font=('times', 15, ' bold '))
txt.place(x=500, y=215)

lbl2 = tk.Label(window, text="Enter Name",width=20  ,fg="red"  ,bg="yellow"    ,height=2 ,font=('times', 15, ' bold ')) 
lbl2.place(x=150, y=300)

txt2 = tk.Entry(window,width=20  ,bg="white"  ,fg="red",font=('times', 15, ' bold ')  )
txt2.place(x=500, y=315)

#method for clear first text box
def clear():
    txt.delete(0, 'end')
#method for clear second text box
def clear2():
    txt2.delete(0, 'end')    
#method for checking user input scholar number is numerical or not
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
#method for taking 
def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    name1=name.replace(" ","")
    if(is_number(Id) and name1.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('We taking your picture and train them',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 60
            elif sampleNum>60:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for ID : " + Id +" Name : "+ name
        row = [Id , name]
        with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        messagebox.showinfo(title="alert" ,message=res)
    else:
        if(is_number(Id)):
            messagebox.showinfo(title="alert" ,message='Enter Alphabetical Name')
        if(name1.isalpha()):
        	messagebox.showinfo(title="alert" ,message='Enter Numeric Scholar number')

def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained Successfully"
    messagebox.showinfo(title="alert" ,message=res)

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #create empty face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

clearButton = tk.Button(window, text="Clear", command=clear  ,fg="red"  ,bg="yellow"  ,width=8  ,height=1 ,activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton.place(x=750, y=200)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="red"  ,bg="yellow"  ,width=8  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold '))
clearButton2.place(x=750, y=300)    
takeImg = tk.Button(window, text="Take Images", command=TakeImages  ,fg="red"  ,bg="deep sky blue"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=150, y=500)
trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="red"  ,bg="green2"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
trainImg.place(x=500, y=500)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="black"  ,bg="red"  ,width=20  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=800, y=500)

copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0,font=('times', 20, 'italic bold underline'))
copyWrite.tag_configure("superscript", offset=10)
copyWrite.insert("insert", "Developed by: Durgesh Patidar")
copyWrite.configure(state="disabled",fg="red"  )
copyWrite.pack(side="left")
copyWrite.place(x=830, y=700)
 
window.mainloop()