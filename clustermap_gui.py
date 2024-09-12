import PySimpleGUI as sg
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import numpy as np
import pandas as pd
import csv
from sklearn import preprocessing
from sklearn.preprocessing import normalize

def load_csv(x):
    with open(x, "r") as csv_file: #Loading the CSV File
        reader = csv.reader(csv_file)
        list = []
        for row in reader:
            list.append(row)
        csv_file.close()

    array = np.array(list)

    dim = array.shape #Color Conditions (If Needed) + Columns Deleting
    row, colmn = dim
    labels = {}
    for i in range(colmn):
        list1 = []
        for x in range(row):
            list1.append(array[x,i])
        list2 = list1[1:]
        labels[array[0,i]] = list2
    arr = array[0].tolist()
    return arr, labels

def input_npy():
    for x in sys.argv:
        if x[-4:] == '.npy':
            FNAME = x
            return FNAME
    return False

def input_csv():
    for x in sys.argv:
        if x[-4:] == '.csv':
            FNAME = x
            arr, labels = load_csv(FNAME)
            return FNAME, arr, labels
    return False, [], None

if __name__ == '__main__': #NPY & CSV File Should be a Space After .PY + Space Btwn Each Other (.py .csv .npy or .py .npy .csv)
    arg = input_npy()
    arg1, arr, labels = input_csv()
    if arg == False and arg1 == False:
        print('No NPY File was Provided')
        print('No CSV File was Provided')
        arg = ''
        arg1 = ''
    elif arg1 == False and arg != False:
        print('No CSV File was Provided')
        arg1 = ''
    elif arg == False and arg1 != False:
        print('No NPY File was Provided')
        arg = ''

sg.theme('GreenTan')

def gen_layout(): #What PySimpleGUI Looks Like to Audience
    file_input = [[sg.Text('Choose a NPY (Features) File to Convert', font=('Helvetica', 16), key='-FBTXT-')],
                  [sg.Input(default_text=arg, font=('Helvetica', 16), key='-FNAME-'), sg.FileBrowse(file_types=(("Text Files", "*.npy"),))],
                  [sg.Text('_' * 100, size=(67, 1))],

                  [sg.Text('Choose a CSV (Categories) File to Convert', font=('Helvetica', 16), key='-FBTXT-')],
                  [sg.Input(default_text=arg1, enable_events=True, font=('Helvetica', 16), key='-FEAT-'), sg.FileBrowse(file_types=(("Text Files", "*.csv"),))],
                  [sg.Text('_' * 100, size=(67, 1))]]
    dwnld_layout = [[sg.Text('Choose Path/Folder + Name for Clustermap', font=('Helvetica', 16), key='-FBTXT-')],
                    [sg.Input(default_text='', font=('Helvetica', 16), key='-FILDWN-'), sg.FolderBrowse("Enter")],
                    [sg.Text('_' * 100, size=(67, 1))]]
    colmn_layout = [[sg.Text('Choose a Row & Value from the CSV File to Edit', font=('Helvetica', 16), key='-COLTXT-')],
                    [sg.Listbox(values=arr, size=(30, 6), select_mode=sg.SELECT_MODE_EXTENDED, enable_events=True, key='-LIST-'),
                     sg.Listbox(values=[], size=(30, 6), select_mode=sg.SELECT_MODE_EXTENDED, enable_events=True, key='-LIST1-')],
                    [sg.Button('Edit'), sg.Button('Save'), sg.Button('Help')],
                    [sg.Input(default_text='', font=('Helvetica', 16), key='-LEDIT-')],
                    [sg.Button('Submit'), sg.Button('Reset'), sg.Button('Cancel')]]
    return file_input + dwnld_layout + colmn_layout

def help_layout(): #What the Tutorial/Help Section Looks Like
    tut_txt = """Help Section

NPY File:
Your NPY file is the file that'll be clustered. It's the file that contains your patients and features. It
should be an array without any holes. It will be normalized in this code.

CSV File:
Your CSV file will be shown in row(s) beside the NPY file (the map). The CSV file contains the
patients and the categories. Its rows should be one more than the NPY file's rows. The values
shouldn't have any holes and can be edited on the main page. It will be normalized by columns
in this code. The first row should be the label names.

Example NPY Input                                Example CSV Input
[[1 0 0 4 2 0 3]                       IS  ASCT  Proportion of Edema  Gender  A/E
 [1 4 3 1 1 4 0]                       0       0                       2                       0         2
 [4 1 0 0 3 4 3]                       0       0                       1                       1         2
 [0 1 4 4 0 4 4]                       0       0                       2                       1         3
 [2 3 2 1 3 2 4]]                      1       1                       3                       1         3
                                       0       0                       1                       1         2
Shape: (5,7)                                                   Shape: (6,5)

For this CSV, every time "Male," or "M," is mentioned, it's set to 0, and "Female," or "F," is set
to 1 in Gender. Every occurrence of "E" is set to 2 and "A" is set to 3 in A/E.

For the Path/Folder + Name for Clustermap, it's fine if you leave it blank. In that case, no file
would be downloaded. But, if you don't, or want a file to be downloaded, an example of the
necessary text is: '/Users/anishdhawan/Downloads/Clustermap_GUI.png'. The 'Browse' button
only returns the Path/Folder, or '/Users/anishdhawan/Downloads/' for example."""

    text_section = [[sg.Text(tut_txt, size=(71, 28), font=('Helvetica', 16), key='-HPTXT-')]]
    return sg.Window('Exit to Continue Editing on Clustermap_GUI', text_section)

layout = gen_layout()
window = sg.Window('Clustermap_GUI', layout) #Window Title

while True:
    event, values = window.read() #Getting Input Values
    if event == 'Help': #Buttons
        win0 = help_layout()
        even0, val0 = win0.read()
        if even0 == sg.WIN_CLOSED:
            win0.close()
    if event in (sg.WIN_CLOSED, 'Cancel'):
        quit()
    clus = values['-FNAME-']
    feat = values['-FEAT-']
    if event == '-FEAT-':
        feat = values['-FEAT-']
        arr, labels = load_csv(feat)
        window['-LIST-'].update(arr)
        window['-LIST1-'].update([])
    if event == '-LIST-':
        while True:
            try:
                INDEX = int(''.join(map(str, window["-LIST-"].get_indexes())))
                locat = arr[INDEX]
                window['-LIST1-'].update(labels[locat])
                break
            except ValueError:
                break
    if event == "Edit":
        while True:
            try:
                INDEX1 = int(''.join(map(str, window["-LIST1-"].get_indexes())))
                window['-LEDIT-'].update(labels[locat][INDEX1])
                break
            except ValueError:
                break
    if event == "Save":
        while True:
            try:
                labels[locat][INDEX1] = values['-LEDIT-']
                window['-LIST1-'].update(labels[locat])
                window['-LEDIT-'].update('')
                break
            except NameError:
                break
    if event == 'Reset':
        window['-FNAME-'].update('')
        window['-FEAT-'].update('')
        window['-LIST-'].update([])
        window['-LIST1-'].update([])
        window['-LEDIT-'].update('')
        window['-FILDWN-'].update('')
    if event == 'Submit':
        break

npy_array = np.load(clus) #Loading the NPY File & Normalizing It
norm_features = normalize(npy_array, axis=0, norm='max')

data = labels #Normalizing the CSV
df = pd.DataFrame(data)
val = df.values
min_max_scaler = preprocessing.MinMaxScaler()
val_scaled = min_max_scaler.fit_transform(val)
normal_df = pd.DataFrame(val_scaled)
labels = normal_df.to_dict('list')

intlist = []
for i in range(len(arr)):
    intlist.append(i)
arr = intlist

for x in labels: #Turning Decimals into Integers (Group By Decimal Tenths - For Color Dict)
    for z in range(len(labels[x])):
        if labels[x][z] == 1.0:
            labels[x][z] = 10E+00
        if labels[x][z] >= 0.0 and labels[x][z] < 0.1:
            labels[x][z] = 0E+00
        if labels[x][z] >= 0.1 and labels[x][z] < 0.2:
            labels[x][z] = 1E+00
        if labels[x][z] >= 0.2 and labels[x][z] < 0.3:
            labels[x][z] = 2E+00
        if labels[x][z] >= 0.3 and labels[x][z] < 0.4:
            labels[x][z] = 3E+00
        if labels[x][z] >= 0.4 and labels[x][z] < 0.5:
            labels[x][z] = 4E+00
        if labels[x][z] >= 0.5 and labels[x][z] < 0.6:
            labels[x][z] = 5E+00
        if labels[x][z] >= 0.6 and labels[x][z] < 0.7:
            labels[x][z] = 6E+00
        if labels[x][z] >= 0.7 and labels[x][z] < 0.8:
            labels[x][z] = 7E+00
        if labels[x][z] >= 0.8 and labels[x][z] < 0.9:
            labels[x][z] = 8E+00
        if labels[x][z] >= 0.9 and labels[x][z] < 1.0:
            labels[x][z] = 9E+00

color_dict = {0E+00:'tab:blue', 1E+00:'tab:red', 2E+00:'tab:orange', 3E+00:'tab:purple', 4E+00:'tab:pink',
5E+00:'aquamarine', 6E+00:'tab:gray', 7E+00:'tab:green', 8E+00:'tab:olive', 9E+00:'tab:cyan', 10E+00:'tab:brown'}

row_colors = [] #Coloring the Rows

for x in arr:
    row_colors.append(([color_dict[int(label)] for label in labels[x]]))

colorm = "RdYlBu_r"

window.close()

a = sns.clustermap(
    norm_features,
    method = 'average',
    metric = "euclidean",
    figsize=(3.5, 3),
    row_cluster=True,
    row_colors=row_colors,
    dendrogram_ratio=(0, 0.05),
    cmap=colorm,
    cbar_pos=None,
    yticklabels=False,
    xticklabels=False,
    colors_ratio=[0.035, 0.035]
) #Should Show the Clustermap in a New Window

if values['-FILDWN-'] != '':
    a.savefig(values['-FILDWN-']) #Saves the Clustermap
    plt.show() #Shows the Clustermap

else:
    plt.show()
