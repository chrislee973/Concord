import PySimpleGUI as sg
import sys
from PIL import Image


file_list_column = [
    [sg.Text('File to open'),
     sg.In(size = (25,1), enable_events=True, key = '-FILES-'),
     sg.FileBrowse()
     ],

    [sg.Listbox(values=[], size=(40,20), enable_events=True, key = '-FILE LIST-')],
]

file_image_column = [[sg.Image(key = '-IMAGE-', size = (224,224))]]


full_layout = [
    [
    sg.Column(file_list_column),
    sg.VSeparator(),
    sg.Column(file_image_column)
    ]
]

window = sg.Window('Image viewer',layout = full_layout)

#Dict that stores displayed file name as keys and associated file path as the value
files_dict = {}

#List of all file names for display in '-FILE LIST-'
files_list = []

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    #fname = values['-FILES-'].split('/')[-1]

    if event== '-FILES-':
        fname = values['-FILES-'].split('/')[-1]
        files_list.append(fname)
        file_path = values['-FILES-']
        files_dict[fname] = file_path
        window['-FILE LIST-'].update(files_list)

    elif event == '-FILE LIST-':
        fname = values['-FILE LIST-'][0]
        fpath = files_dict[fname]
        image = Image.open(fpath).resize((228, 228), Image.ANTIALIAS)

        #Just the name w/o file extension
        name = values['-FILE LIST-'][0].split('.')[0]
        image.save('images/' + name + '.png')
        fpath = 'images/' + name + '.png'

        window['-IMAGE-'].update(fpath)

window.close()
