import PySimpleGUI as sg
from utils import text_file, Pdf, load_word2vec, retrieve, print_output_sents
import random


word2vec = load_word2vec()
print(word2vec.most_similar('snake', topn = 5))


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
        [sg.Checkbox('word2vec', key = '-WORD2VEC-')],
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
               [sg.Button('Shuffle', enable_events=True, key='-SHUFFLE-'),
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

        #Clear output box
        window2['-WIN2 TEXT-']('')

        #Get user query
        query = values['-QUERY-']

        #Get the list of pdfs/txt_files user has chosen
        files = values['-FILE LIST-']

        output_sents_zipped, num_sents_found = retrieve(files, query, pdf_obj, txt_obj)

        #Display the legend
        for i, file in enumerate(files):
            # Create legend denoting which color corresponds to which document
            window2['-LEGEND-'].print(file, end='', background_color=background_colors[i])
            window2['-LEGEND-'].print('\n', end='')

        #Print the color-coded output sentences
        print_output_sents(output_sents_zipped, files, background_colors, cprint)

        #Print the number of sentences that were found
        window2['-WIN2 NUM SENTS-'].update(f"Found {num_sents_found} sentences containing '{query}'.")


        #For word2vec
        if values['-WORD2VEC-'] == True:

            w2v_sents = []

            # Get the 20 most similar words to the query and batch query the results against the document(s)
            topn = word2vec.most_similar(query, topn=20)

            # Loop through the word2vec results, which come in a list of tuples that each take the form: (word, similarity_score)
            for word, _ in topn:
                output_sents_zipped, _ = retrieve(files, word, pdf_obj, txt_obj)

                w2v_sents += output_sents_zipped

            # Print how many word2vec sentences it found
            cprint(f"Found {len(w2v_sents)} potentially related sentences using word2vec.", text_color='red', end = '\n\n')

            # Print w2v_sents
            print_output_sents(w2v_sents, files, background_colors, cprint)

            # for sent in w2v_sents:
            #     cprint(sent, background_color = background_color[i])

    elif event == '-SHUFFLE-':
        #Clear the output box
        window2['-WIN2 TEXT-']('')
        random.shuffle(output_sents_zipped)
        print_output_sents(output_sents_zipped, files, background_colors, cprint)

        
window.close()
