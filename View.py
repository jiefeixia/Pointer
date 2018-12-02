from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image


class JobFinder(object):
    def __init__(self):
        self.window = Tk()
        self.window.title = "Pointer"
        self.window.geometry("720x580+500+300")


    def setupGUI(self):
        # color = "#024f26"
        color = "#eeeeee"
        self.window.configure(background=color)
        mainFrame = tk.Frame(self.window, bg=color)
        searchFrame = tk.Frame(mainFrame, bg=color)
        tk.Label(searchFrame, text="Address", bg=color).grid(row=0, column=0,padx=5)
        tk.Entry(searchFrame).grid(row=0, column=1)
        states = ttk.Combobox(searchFrame, state="readonly", width=5, values=["CA", "PA", "OH"]).grid(row=0, column=2,padx=5)
        tk.Label(searchFrame, text="Job Category", bg=color).grid(row=0, column=3)
        ttk.Combobox(searchFrame, state="readonly", width=15, values=["Data Scientist", "Software Developing Engineer", "Consultant"]).grid(row=0,
                                                                                                                column=4,padx=5)
        bnSearch = ttk.Button(searchFrame, text="Search",  command=self.search )
        bnSearch.grid(row=0, column=5,)

        resultFrame = tk.Frame(mainFrame, bg=color)
        tk.Label(resultFrame, text="Course List:", bg=color).grid(row=0, column=0,sticky="w",padx=10)
        tk.Label(resultFrame, text="Course Description:", bg=color).grid(row=0, column=1,sticky="w")

        # set couseList
        courseListFrame = tk.Frame(resultFrame,bg=color)
        courseListFrame.grid(row=1, column=0, rowspan=2,sticky="nw",padx=10)

        courseListScrollbar = Scrollbar(courseListFrame,bg=color,relief=SUNKEN)
        courseListScrollbar.pack(side=RIGHT,fill=Y)
        self.lbCourseList = tk.Listbox(courseListFrame, height=25,width=30,yscrollcommand=courseListScrollbar.set,relief=SUNKEN)
        self.lbCourseList.pack()
        courseListScrollbar.config(command=self.lbCourseList.yview)




        self.labImage = tk.Label(resultFrame, width=370, height=150,relief=SUNKEN,bg=color)
        self.labImage.grid(row=1, column=1,sticky="w")


        # set course description
        courseDescriptionFrame = Frame(resultFrame,bg=color)
        courseDescriptionFrame.grid(row=2,column=1)
        courseDescriptionScrollbar = Scrollbar(courseDescriptionFrame,bg=color,relief=SUNKEN)
        courseDescriptionScrollbar.pack(side=RIGHT,fill=Y)
        self.labCourseDescription = tk.Text(courseDescriptionFrame, wrap=WORD,height=17,width=50,yscrollcommand=courseDescriptionScrollbar.set,relief=SUNKEN)
        self.labCourseDescription.pack()
        courseDescriptionScrollbar.config(command=self.labCourseDescription.yview)

        Label(self.window,text="Pointer",bg=color,font=("Times New Roman",44)).pack(fill=X)
        searchFrame.pack(fill=X,padx=10)
        resultFrame.pack(fill=X,pady=10,padx=10)

        # binding
        self.lbCourseList.bind("<<ListboxSelect>>",self.courseSelected)

        mainFrame.pack()

        self.initData()

        self.window.mainloop()

    def initData(self):
        for i in range(30):
            self.lbCourseList.insert(END, "course" + str(i))

        imageFileName = "./flower1.jpg"
        imgFile = Image.open(imageFileName)

        img = ImageTk.PhotoImage(imgFile.resize((370,150),Image.ANTIALIAS))
        self.labImage.configure(image=img)
        self.labImage.image=img

        fileCourseDesc = open("./courseDesc.txt", "r")
        courseContent = fileCourseDesc.read()
        self.labCourseDescription.configure(state=NORMAL)
        self.labCourseDescription.insert(END,courseContent)
        self.labCourseDescription.configure(state=DISABLED)
        fileCourseDesc.close()

    def search(self):
        print("search")

    def courseSelected(self,event):
        print("selected: " + str(self.lbCourseList.curselection()))


jobFinder = JobFinder()
jobFinder.setupGUI()
