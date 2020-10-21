import PySimpleGUI as sg
import sys
from PIL import Image
from utils import text_file, Pdf
import random



#List of all file names for display in '-FILE LIST-'
files_list = []

#Dictionary of all pdf objects to check if file is in list so as to not create the same pdf objects every time another pdf is uploaded
#Keys are the filename and the values are the Pdf object corresponding to the filename
pdf_obj = {}

#Dictionary of all text file objects
txt_obj = {}


#For printing color to the output so as to differentiate results coming from different documents
cprint = sg.cprint

#List of possible background colors for cprint to use
background_colors = ['yellow', 'orange']



def make_win1():
    file_list_column = [
        [sg.Text('Upload file'), sg.In(size=(25, 1), enable_events=True, key='-FILES-'), sg.FileBrowse()],
        [sg.Listbox(values=[], size=(40, 20), enable_events=True, select_mode='multiple', key='-FILE LIST-')]]

    file_text_column = [[sg.Text('Enter query: '), sg.In(size=(25, 1), enable_events=True, key='-QUERY-'),
                         sg.Button("Find", enable_events=True, key='-FIND-')]]

                        # [sg.Text(size=(40, 1), key='-NUM SENTS-')],
                        # [sg.Multiline(enable_events=True, key='-TEXT-', size=(40, 20), disabled=True)]]

    full_layout = [[
        sg.Column(file_list_column),
        sg.VSeparator(),
        sg.Column(file_text_column)]]

    return sg.Window('Concord', full_layout, finalize= True)

def make_win2():
    layout = [[sg.Text(size=(40, 1), key='-WIN2 NUM SENTS-')],
               [sg.Button('Shuffle', enable_events=True, key='-SHUFFLE-'), sg.Checkbox('word2vec', enable_events=True, key = '-WORD2VEC-'),
                sg.Multiline(size = (50,1), enable_events=True, disabled=True, key = '-LEGEND-')],
               [sg.Multiline(enable_events=True, disabled=True, key='-WIN2 TEXT-', size=(150, 50))],
               [sg.Button('Exit')]]
    return sg.Window('Second Window', layout, finalize=True)

window1, window2 = make_win1(), None

#--------EVENT LOOP---------------
while True:
    window, event, values = sg.read_all_windows()


    if event == sg.WIN_CLOSED:
        window.close()
        if window == window2:
            window2 = None
        elif window == window1:
            break


    #fname = values['-FILES-'].split('/')[-1]

    elif event== '-FILES-':
        fname = values['-FILES-'].split('/')[-1]
        file_path = values['-FILES-']

        #If the file is not in pdf_objects list, create pdf object and append it
        if fname not in files_list:
            files_list.append(fname)
            #Check if pdf or text file
            if fname.endswith('.pdf'):
                pdf = Pdf(file_path)
                pdf_obj[fname] = pdf
            elif fname.endswith('.txt'):
                txt_file = text_file(file_path)
                txt_obj[fname] = txt_file
        else:
            print('File is already in your environment!')

        window['-FILE LIST-'].update(files_list)


    elif event == '-FIND-':
        if not window2:
            window2 = make_win2()

        # Tells cprint which widget element to print the colored text in
        sg.cprint_set_output_destination(window2, '-WIN2 TEXT-')

        #Initialize num_sents_found and output_sents
        num_sents_found = 0
        output_sents=  []

        #Clear output box
        window2['-WIN2 TEXT-']('')

        #Get user query
        query = values['-QUERY-']

        #Get the list of pdfs/txt_files user has chosen
        files = values['-FILE LIST-']

        #Initialize zipped list, which will contain all output sentences along with corresponding index telling which file they belong in
        output_sents_zipped = []


        for i, file in enumerate(files):
            if file.endswith('.pdf'):
                pdf = pdf_obj[file]
                output_sents = pdf.get_sents(query)
                num_sents_found += len(output_sents)

                output_sents_zipped += list(zip([i]*num_sents_found, output_sents))

            elif file.endswith('.txt'):
                txt = txt_obj[file]
                output_sents = txt.get_sents(query)
                num_sents_found += len(output_sents)

                output_sents_zipped = list(zip([i]*num_sents_found, output_sents))

            # Create legend denoting which color corresponds to which document
            window2['-LEGEND-'].print(file, end='', background_color=background_colors[i])
            window2['-LEGEND-'].print('\n', end='')

        for i, sent in output_sents_zipped:
            # If user only chose one file, no need to highlight it a certain color
            if len(files) == 1:
                cprint(sent, end = '\n\n')
            else:
                #win2['-WIN2 TEXT-'].print(sent, end=  '\n\n')
                cprint(sent, background_color=background_colors[i], end = '\n\n')

        window2['-WIN2 NUM SENTS-'].update(f"Found {num_sents_found} sentences containing '{query}'.")


    elif event == '-SHUFFLE-':
        #Clear the output box
        window2['-WIN2 TEXT-']('')

        random.shuffle(output_sents_zipped)

        for i, sent in output_sents_zipped:
            if len(files) == 1:
                cprint(sent, end='\n\n')
            else:
                # win2['-WIN2 TEXT-'].print(sent, end=  '\n\n')
                cprint(sent, background_color=background_colors[i], end='\n\n')

window.close()