# Proj_main.py
# CS 361 Project - Aimee Bogle
# This is the development build for CS361 project. This code will launch an application with that will connect to 
# OSM maps and assist the user in finding hiking trails near a searchable location. The application will allow for user accounts,
# a help page, contact page, as well as a main search page and a results page. 
# Future builds: Working to integrate the OSM maps to use for hiking waypoints, connecting DB to create user accounts, building an
# addiitonal window to view maps and download to device for offline use. 

import PySimpleGUI as sg


sg.theme('DarkGrey13')
sg.set_options(font=("Avenir Next", 16))

def make_window1():
    """ Application Homescreen """

    layout = [[sg.Push(), sg.Image('logo.png'), sg.Push()],
              [sg.Push(), sg.Text('Search Trails by State: '), sg.Push()], 
              [sg.Push(), sg.InputText('', size =(30,1), key='search'), sg.Push()],
              [sg.Push(), sg.Button('Submit'), sg.Button('Exit'), sg.Push()],
              [sg.VPush(), sg.Button('Help'), sg.Push()]]

    return sg.Window('The Adventurer', layout, size=(1000, 950), finalize=True)


def make_window2():
    """ Help Instructions Window """

    layout =[[sg.Push(), sg.Image('logo_small.png'), sg.Push()],
            [sg.Push (), sg.Text('To search for an adventure area, follow the below steps!'), sg.Push()],
            [sg.Push(), sg.Text('1. Enter a state in the search bar and hit submit'), sg.Push()],
            [sg.Push(), sg.Text('2. To find adventure areas by park name, city, or activity select \nthe Advanced Search options'), sg.Push()],
            [sg.Push(), sg.Text('3. Maps can be downloaded to your device for offline usage by selecting \nthe download icon and saving chosing a loction on your device to save it to'), sg.Push()],
            [sg.Push(), sg.Text('For more help, please contact us using the link below!'), sg.Push()],
            [sg.Push(), sg.Button('OK'), sg.Button('Contact Us'), sg.Push()]]     

    return sg.Window('Help', layout, size=(1000, 950), finalize=True)

def make_window3():
    """ Primary Search results window """

    layout = [[sg.Push(), sg.Image('logo_small.png'), sg.Push()],
             [sg.Push(), sg.Text('Search Results Page', font=('Avenir 20')), sg.Push()],
             [sg.Push(), sg.Button('OK'), sg.Button('Back'), sg.Push()]]
             

    return sg.Window('Search Results', layout, size=(1000,950), finalize=True)

def make_window4():
    """ A contact form for users to complete as needed """

    layout = [[sg.Push(), sg.Image('logo_small.png'), sg.Push()],
             [sg.Push(), sg.Text('Contact Us', font=('Avenir 20')), sg.Push()],
             [sg.Text('Name: ', size=(10,1)), sg.InputText('', key='contact_name')],
             [sg.Text('Email: ', size=(10,1)), sg.InputText('', key='contact_email')],
             [sg.Text('Question: ', size=(10,1)), sg.InputText('', key='contact_question')],
             [sg.Push(), sg.Button('Send'), sg.Button('Back'), sg.Push()]]

    return sg.Window('Contact Us', layout, size=(1000, 950), finalize=True)

def main():

    """ Main window which holds the event loop """
    
    window1, window2, window3, window4 = make_window1(), None, None, None
    
    while True:

        window, event, values = sg.read_all_windows()

        if window == window1 and event in (sg.WIN_CLOSED, 'Exit'):
            break

        # Window 1
        if event == 'Submit' and not window3:
            user_search = str(values['search'])
            window3 = make_window3()

        elif event == 'Help' and not window2:
            window2 = make_window2()

        # Window 2
        if window == window2 and event in(sg.WIN_CLOSED, 'OK'):
            window2.close()
            window2 = None

        elif event == 'Contact Us' and not window4:
            window4 = make_window4()

        # Window3 
        if window == window3 and event in(sg.WIN_CLOSED, 'OK', 'Back'):
            window3.close()
            window3 = None

        # Window4
        if window == window4 and event in(sg.WIN_CLOSED, 'Back'):
            window4.close()
            window4 = None

        elif window == window4 and event == 'Send':
            contact_name = str(values['contact_name'])
            contact_email = str(values['contact_email'])
            contact_question = str(values['contact_question'])
            window4.close()
            window4 = None 

    window1.close()
    if window2 is not None:
        window2.close()
    if window3 is not None:
        window3.close()
    if window4 is not None:
        window4.close()

if __name__ == '__main__':
    main()