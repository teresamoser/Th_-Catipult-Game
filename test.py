import PySimpleGUI as sg

sg.theme('DarkAmber')   # Add a touch of color
#  All the stuff inside your window.
layout = [  [sg.Text('Determine Trajectory of Trebuchet')],
                [sg.Text('Enter launch force: '), sg.InputText()],
                [sg.Text('Enter launch angle: '), sg.InputText()],
                [sg.Button('Ok'), sg.Button('Cancel')] ]
    # Create the Window
window = sg.Window('Trajectory Entry', layout)
    # Event Loop to process "events" and get the "values" of the inputs
while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':
             # if user closes window or clicks cancel
            break
        print('You entered ', values[1])
window.close()