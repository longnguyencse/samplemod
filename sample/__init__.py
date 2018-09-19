#!/usr/bin/env python
from tkinter import *
from tkinter import StringVar, ttk
from tkinter.filedialog import askopenfilename
import tkinter.messagebox


import requests
import json
import os
import datetime

from hdfs import InsecureClient
from hdfs.util import HdfsError

LABEL_FILE_UPLOAD = 'Choose file'
LABEL_PROJECT_TYPE = 'Project Type'
LABEL_FILE_NAME = 'File Name'
LABEL_FILE_TYPE = 'File type'
LABEL_FILE_SIZE = 'File Size'
LABEL_WEATHER = 'Weather'
LABEL_LOCATION = 'Location'
LABEL_HDFS_PATH = 'Hdfs location path'
LABEL_FILE_EXTENSION = 'File Extension'
LABEL_TOTAL_FRAME = 'Total frame'
LABEL_IMG_WIDTH = 'Image width'
LABEL_IMG_HEIGHT = 'Image height'
LABEL_FRAMES_PER_SECOND = 'Fps'

TEXT_TOOL_TITLE = 'Tool copy file V2'

ABOUT_TEXT = 'Upload success'
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
MSG_HDFS_UPLOAD_COMPLETED = 'Upload file to hdfs success'

COMBOBOX_PROJECT_TYPE_INPUT_VALUE = 'Manual Input'


CONFIG_FILE_NAME = 'config.json'
CONFIG_HDFS_TOTAL_KEY = 'hdfs_config'
CONFIG_HDFS_URL_KEY = 'url'
CONFIG_HDFS_USERNAME_KEY = 'username'
CONFIG_HDFS_FOLDER_PATH_KEY = 'path_folder_org_data'
CONFIG_HDFS_ACCESS_URL_KEY = 'hdfs_location_file_access'
CONFIG_SERVER_URL_KEY = 'server_vertx_url'

VERT_API_SUBFIX_URL = '/files/update_file_info'
root = Tk()

# with open(CONFIG_FILE_NAME) as json_data_file:
#     data = json.load(json_data_file);
#     print(data)
# hdfs_config = data[CONFIG_HDFS_TOTAL_KEY]
hdfs_config = "/ifp/python"
print(hdfs_config)
# hdfs_url = hdfs_config[CONFIG_HDFS_URL_KEY]
# hdfs_username = hdfs_config[CONFIG_HDFS_USERNAME_KEY]
# server_vertx_url = data[CONFIG_SERVER_URL_KEY]
# print(server_vertx_url)

# upload file to hdfs

# client = InsecureClient('http://192.168.1.168:50070', user='vndev')
client = InsecureClient("http://ifp-hadoop-nn1.at.mikorn.com:50070", user="vndev")
file_name = ''
# hdfs_path = '/user/hdfs/wiki/'


def quit():
    global root
    root.quit()

# client.upload(hdfs_path, file_name)

#This is where we lauch the file manager bar.
def OpenFile():
    name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                           filetypes=(("Bin File", "*.bin"), ("Text File", "*.zip"), ("All Files", "*.*")),
                           title="Choose a file."
                           )
    print(name)
    #Using try in case user types in unknown file or closes without choosing a file.
    try:
        with open(name, 'r') as UseFile:
            buttonBrowse['text']=UseFile.name
            file_name = UseFile.name
            print(file_name)
            os.path.split(file_name)
            print(os.path.split(file_name)[1])
            org_file_name = os.path.split(file_name)[1]
            entrySpaceFileName.config(state='normal')
            entrySpaceFileName.delete(0, END)
            entrySpaceFileName.insert(0, org_file_name)
            entrySpaceFileName.config(state='disabled')

            file_size = getSize(file_name)
            entrySpaceFileSize.config(state='normal')
            entrySpaceFileSize.delete(0, END)
            entrySpaceFileSize.insert(0, file_size)
            entrySpaceFileSize.config(state='disabled')
    except:
        print("No file exists")

def getSize(filename):
    st = os.stat(filename)
    return st.st_size

def projectTypeValueChange(index, value, op):
    print("combobox updated to ", comboboxProjectType.get())
    if COMBOBOX_PROJECT_TYPE_INPUT_VALUE == comboboxProjectType.get():
        entryProjType.config(state='normal')
    else:
        entryProjType.config(state='disabled')
        # print ("combobox updated to1 ", comboboxProjectType.get())


# Title is the name of application (like title web application)
Title = root.title(TEXT_TOOL_TITLE)
root.geometry('700x550')
root.config(background="#819FF7") #sets background color to white
labelfont = ('times', 14)

label_0 = Label(root, text="Uploader Client", width=20, font=("bold", 22), bg="#819FF7")
label_0.place(x=90, y=20)


theLabelProjType = Label(root, text=LABEL_PROJECT_TYPE, font=labelfont, bg="#819FF7")
# theLabelProjType.grid(row=0, column=0)
theLabelProjType.place(x=20, y=100)

entryProjType = Entry(root, font=labelfont)
entryProjType.config(state='disabled')
entryProjType.place(x=450, y=100)
# entryProjType.grid(row=0, column=2)
entryProjType.insert(0, '')

valueProjectType = StringVar()
valueProjectType.trace('w', projectTypeValueChange)
comboboxProjectType = ttk.Combobox(root, textvariable=valueProjectType, state='readonly', font=labelfont)
comboboxProjectType['values'] = ('PD', 'VD', 'AVT', COMBOBOX_PROJECT_TYPE_INPUT_VALUE)
comboboxProjectType.current(0)
comboboxProjectType.place(x=150, y=100)

theLabel02 = Label(root, text=LABEL_FILE_TYPE, font=labelfont, bg="#819FF7")
theLabel02.place(x=20, y=130)

# theLabel02.grid(row=2, column=0)
#
valueFileType = StringVar()
comboboxFileType = ttk.Combobox(root, textvariable=valueFileType, state='readonly', font=labelfont)
comboboxFileType['values'] = ('video', 'image')
comboboxFileType.current(0)
comboboxFileType.place(x=150, y=130)

theLabel01 = Label(root, text=LABEL_FILE_NAME, font=labelfont, bg="#819FF7")
theLabel01.place(x=20, y=160)
# theLabel01.grid(row=1, column=0)

entrySpaceFileName = Entry(root, font=labelfont)
entrySpaceFileName.config(state='disabled')
entrySpaceFileName.place(x=150, y=160)
# entrySpaceFileName.grid(row=1, column=1)

#
theLabel03 = Label(root, text=LABEL_FILE_SIZE, font=labelfont, bg="#819FF7")
theLabel03.place(x=20, y=190)
# theLabel03.grid(row=3, column=0)
#
entrySpaceFileSize = Entry(root, font=labelfont)
entrySpaceFileSize.config(state='disabled')
entrySpaceFileSize.place(x=150, y=190)
# entrySpaceFileSize.grid(row=3, column=1)
entrySpaceFileSize.insert(0, '')
#
theLabel04 = Label(root, text=LABEL_WEATHER, font=labelfont, bg="#819FF7")
theLabel04.place(x=20, y=220)
# theLabel04.grid(row=4, column=0)
#
entrySpaceWeather = Entry(root, font=labelfont)
entrySpaceWeather.place(x=150, y=220)
# entrySpaceWeather.grid(row=4, column=1)
entrySpaceWeather.insert(0, 'Rain')
#
theLabel05 = Label(root, text=LABEL_LOCATION, font=labelfont, bg="#819FF7")
theLabel05.place(x=20, y=250)
# theLabel05.grid(row=5, column=0)
#
entrySpaceLocation = Entry(root, font=labelfont)
entrySpaceLocation.place(x=150, y=250)
# entrySpaceLocation.grid(row=5, column=1)
entrySpaceLocation.insert(0, 'Ho Chi Minh')
#
# path_folder = hdfs_config[CONFIG_HDFS_FOLDER_PATH_KEY]
#
#
theLabel08 = Label(root, text=LABEL_TOTAL_FRAME, font=labelfont, bg="#819FF7")
theLabel08.place(x=20, y=280)
# theLabel08.grid(row=8, column = 0)
#
entrySpaceTotalFrames = Entry(root, font=labelfont)
entrySpaceTotalFrames.place(x=150, y=280)
# entrySpaceTotalFrames.grid(row=8, column=1)
entrySpaceTotalFrames.insert(0, '100')
#
theLabel09 = Label(root, text=LABEL_IMG_WIDTH, font=labelfont, bg="#819FF7")
theLabel09.place(x=20, y=310)
# theLabel09.grid(row=9, column=0)
#
entrySpaceImgWidth = Entry(root, font=labelfont)
entrySpaceImgWidth.place(x=150, y=310)
# entrySpaceImgWidth.grid(row=9, column=1)
entrySpaceImgWidth.insert(0, '1024')
#
#
theLabel10 = Label(root, text=LABEL_IMG_HEIGHT, font=labelfont, bg="#819FF7")
theLabel10.place(x=20, y=340)
# theLabel10.grid(row=10, column=0)
#
entrySpaceImgHeight = Entry(root, font=labelfont)
entrySpaceImgHeight.place(x=150, y=340)
# entrySpaceImgHeight.grid(row=10, column=1)
entrySpaceImgHeight.insert(0, '769')
#
theLabel11 = Label(root, text=LABEL_FRAMES_PER_SECOND, font=labelfont, bg="#819FF7")
theLabel11.place(x=20, y=370)
# theLabel11.grid(row=11, column=0)
#
entrySpaceFPS = Entry(root, font=labelfont)
entrySpaceFPS.place(x=150, y=370)
# entrySpaceFPS.grid(row=11, column=1)
entrySpaceFPS.insert(0, '30')
#
theLabelFileUpload = Label(root, text=LABEL_FILE_UPLOAD, font=labelfont, bg="#819FF7")
theLabelFileUpload.place(x=20, y=400)
# theLabelFileUpload.grid(row=12, column=0)
#
buttonBrowse = Button(root, text='Open File', font=labelfont, command=OpenFile)
buttonBrowse.place(x=150, y=400)
# buttonBrowse.grid(row=12, column=1)
#
today = datetime.datetime.now()
created_time = today.strftime(DATE_TIME_FORMAT)[:-3]
print(created_time)



def showPopUp():
    tkinter.messagebox.showinfo('Notifications', MSG_HDFS_UPLOAD_COMPLETED)

def showPopUpError(error):
    tkinter.messagebox.showerror('ERROR', error)

def submit():
    print('Submit')
    url = ""
    print(url)
    project_type = comboboxProjectType.get()
    if COMBOBOX_PROJECT_TYPE_INPUT_VALUE == project_type :
        project_type = entryProjType.get()

    file_id = entrySpaceFileName.get()
    # file_type = entrySpaceFileType.get()
    file_type = comboboxFileType.get()
    file_size = entrySpaceFileSize.get()
    # created_time = entrySpace03.get()
    weather = entrySpaceWeather.get()
    location = entrySpaceLocation.get()
    # hdfsPath = entrySpace06.get()
    # hdfsPath = path_folder
    hdfsPath = "ifp/python"
    # extension = entrySpace07.get()
    totalFrame = entrySpaceTotalFrames.get()
    imgWidth = entrySpaceImgWidth.get()
    imgHeight = entrySpaceImgHeight.get()
    fps = entrySpaceFPS.get()
    file_name = buttonBrowse['text']
    # client._proxy('proxy_host:proxy_port', 'http')
    try:
        result = client.upload(hdfsPath, file_name)
        print(result.__contains__(hdfsPath))
        if (result.__contains__(hdfsPath)):
            print(result)
            # showPopUp()
    except  HdfsError as err:
        print(err)
        showPopUpError(err)

        return

    #url = 'http://192.168.1.56:8084/files/save_gt_data_v2' # Set destination URL here
    hdfs_full_path = hdfs_config[CONFIG_HDFS_ACCESS_URL_KEY] + hdfsPath + "/" + file_id

    post_fields = {
        'project_type' : project_type,
        'file_name': file_id,
        'file_type': file_type,
        'file_size': file_size,
        'created_time': created_time,
        'weather': weather,
        'location': location,
        'hdfs_location_path': hdfs_full_path,
        # 'file_extension': extension,
        'total_frames': int(totalFrame),
        'img_width': int(imgWidth, 0),
        'img_height': int(imgHeight, 0),
        'video_fps': int(fps, 0),
    }
    print(post_fields)
    headers = {'Content-type': 'application/json'}


    try:
        response = requests.post(url, json=post_fields, headers=headers)
        print(response.content)
        print("save gt_data success")
        showPopUp()
    except requests.exceptions.HTTPError as err:
        print("save gt_data failed")
        print(err)
        showPopUpError(err)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        showPopUpError(errc)
    except requests.exceptions.RequestException as e:
        print('Connection error: '+str(e))
        showPopUpError(e)
# Submit button

button = Button(root, text='Submit', command=submit, width=20, bg='brown', fg='white', font=labelfont)
button.place(x=200, y=470)
# button.grid(columnspan=2)
# Menu bar

menu = Menu(root)
root.config(menu=menu)
# file = Menu(menu)

# menu.add_command(label = 'Exit', command = lambda:exit())

# menu.add_command(label = 'Exit', command = quit)
# menu.add_cascade(label = 'File', menu = file)




root.mainloop()