# Proj_main.py
# CS 361 Project - Aimee Bogle
# This is the development build for CS361 project. This code will launch an application with that will connect to 
# OSM maps and assist the user in finding hiking trails near a searchable location. The application will allow for user accounts,
# a help page, contact page, as well as a main search page and a results page. 
# Future builds: Working to integrate the OSM maps to use for hiking waypoints, connecting DB to create user accounts, building an
# addiitonal window to view maps and download to device for offline use. 

from tkinter import Frame
import PySimpleGUI as sg
from OSMPythonTools.api import Api
from OSMPythonTools import overpass
from folium import Popup
from pymongo import MongoClient


sg.theme('DarkGrey13')
sg.set_options(font=("Avenir Next", 16))
username = ''
password = ''
client = MongoClient()
db = client.CS361 
# newUser = {# Proj_main.py
# CS 361 Project - Aimee Bogle
# This is the development build for CS361 project. This code will launch an application with that will connect to 
# OSM maps and assist the user in finding hiking trails near a searchable location. The application will allow for user accounts,# Proj_main.py
# CS 361 Project - Aimee Bogle
# This is the development build for CS361 project. This code will launch an application with that will connect to 
# OSM maps and assist the user in finding hiking trails near a searchable location. The application will allow for user accounts,
# a help page, contact page, as well as a main search page and a results page. 
# Future builds: Working to integrate the OSM maps to use for hiking waypoints, connecting DB to create user accounts, building an
# addiitonal window to view maps and download to device for offline use. 

import threading
from tkinter import Frame
import PySimpleGUI as sg
from OSMPythonTools.api import Api
from OSMPythonTools import overpass
import folium 
from pymongo import MongoClient
import socket_server as ss
import socket_client as sc
import requests
import time
import linker as ytl

sg.theme('DarkGrey13')
sg.set_options(font=("Avenir Next", 16))
username = ''
password = ''
client = MongoClient()
db = client.CS361 
# newUser = {
#     "username": "",
#     "password": "",
#     "Name": "",
#     "Email": ""
# }
# newUser = db.User_Authentication 

############################# Function to pull out NP API Data into usable dict #################################
def trails_images():
    trail_images = {}
    i = 0
    for i in range (0,18,1):
        trail_images[i] = np_response['data'][i]['images'][0]['url']
        i += 1
    return trail_images

def trails_names():
    trail_names = {}
    i = 0
    for i in range (0,16,1):
        trail_names[i] = np_response['data'][i]['title']
        i+=0
    return trail_names
    
def trails_urls():
    trail_urls = {}
    i = 0
    for i in range (0,18,1):
        trail_urls[i] = np_response['data'][i]['url']
        i+=0
    return trail_urls

def trails_descriptiopn():
    trail_description = {}
    i = 0
    for i in range (0,18,1):
        trail_description[i] = np_response['data'][i]['url']
        i+=0
    return trail_description

def trails_coord():
    trail_coord = {}
    i = 0
    for i in range (0,18,1):
        trail_coord[i] = np_response['data'][i]['url']
        i+=0

    return trail_coord

################################## Function for adding a YouTube link on Search Page ##########################

def youtubeSearch(search):
    grabLink = open('link-service.txt', 'r+')
    grabLink.seek(0)
    grabLink.truncate()
    grabLink.write("Keywords: " + search + ' hiking' "\n")
    grabLink.close()
    time.sleep(10)

    grabLink = open('link-service.txt', 'r+')
    link = grabLink.read()
    grabLink.close()

    return link

################################# Application Windows ###########################################

def make_win_home():
    """ Application Homescreen """

    block_1 = [[sg.Push(), sg.Text('Search Trails by National Park Name: '), sg.Push(), sg.Push(), sg.Text('Convert an address to geocoordinates: '), sg.Push()],
               [sg.Push(), sg.InputText('', size=(40,1), enable_events = True, key='trail_search'), sg.Push(), sg.InputText('', size=(40,1), enable_events = True, key='geo')]]

    col_1 =[[sg.Push(), sg.Button('Submit', button_color=('black', '#f77c2f')), sg.Push(), sg.Button('Exit', button_color=('black', '#f77c2f')), sg.Push()],
            [sg.Push(), sg.Button('Help', button_color=('black', '#f77c2f')), sg.Push()]]

    col_2 = [[sg.Push(), sg.Button('Sign up', button_color=('black', '#f77c2f')), sg.Push(),sg.Button('Login', button_color=('black', '#f77c2f')), sg.Push()]]

    layout = [[sg.Push(), sg.Column(col_2)],
              [sg.Push(), sg.Image('logo.png'), sg.Push()],
              [sg.Push(), sg.Frame('', block_1, size=(900, 100), expand_x=True, expand_y=True, relief=sg.RELIEF_GROOVE, border_width=3), sg.Push()],
              [sg.Push(), sg.Column(col_1), sg.Push()]]

    return sg.Window('The Adventurer', layout, size=(900, 1000), finalize=True)

def make_map(user_search):
    """" Function to build and display a map """

    my_map1 = folium.Map(location = {user_search}, zoom_start=12)
    folium.CircleMarker(location = {user_search},
                    radius = 50, popup = ' FRI ').add_to(my_map1)
 
    map_display = my_map1.save("my_map1.html")

    return map_display

def make_win_help():
    """ Help Instructions Window """

    layout =[[sg.Push(), sg.Image('logo_small.png'), sg.Push()],
            [sg.Push (), sg.Text('To search for an adventure area, follow the below steps!'), sg.Push()],
            [sg.Push(), sg.Text('1. Enter a state in the search bar and hit submit'), sg.Push()],
            [sg.Push(), sg.Text('2. To find adventure areas by park name, city, or activity select \nthe Advanced Search options'), sg.Push()],
            [sg.Push(), sg.Text('3. Maps can be downloaded to your device for offline usage by selecting \nthe download icon and saving chosing a loction on your device to save it to'), sg.Push()],
            [sg.Push(), sg.Text('For more help, please contact us using the link below!'), sg.Push()],
            [sg.Push(), sg.Button('OK', button_color=('black', '#f77c2f')), sg.Button('Contact Us', button_color=('black', '#f77c2f')), sg.Push()]]     

    return sg.Window('Help', layout, size=(700, 800), finalize=True)


def make_win_search():
    """ Primary Search results window """

    trail_names = trails_names()

    # trail_names = {}
    # trail_images = {}
    # trail_urls = {}
    # trail_description = {}
    # trail_coord = {}
    # i = 0
    # j= 0

    # for i in range (0,18,1):
    #     trail_names[i] = np_response['data'][j]['title']
    #     trail_images[i] = np_response['data'][j]['images'][0]['url']
    #     trail_urls[i] = np_response['data'][j]['url']
    #     trail_description[i] = np_response['data'][j]['listingDescription']     
    #     trail_coord[i] = np_response['data'][j]['latLong']       
    #     i+=1
    #     j+=1


    block_1 = [[sg.Push(), sg.Image('logo_small.png'), sg.Push()], 
              [sg.Push(), sg.Text('Hiking Trails', font=('Avenir 40 bold'), text_color='#f77c2f'), sg.Push()]]

    trails =  [[sg.Push(), sg.Button(trail_names[0], key='trail0'),sg.Button(trail_names[1], key='trail1'), sg.Button(trail_names[2], key='trail2'), sg.Push()],
               [sg.Push(), sg.Button(trail_names[3], key='trail3'), sg.Button(trail_names[4], key='trail4'), sg.Button(trail_names[5], key='trail5'), sg.Push()], 
               [sg.Push(), sg.Button(trail_names[6], key='trail6'), sg.Button(trail_names[7], key='trail7'), sg.Button(trail_names[8], key='trail8'), sg.Push()], 
               [sg.Push(), sg.Button(trail_names[9], key='trail9'), sg.Button(trail_names[10], key='trail10'), sg.Button(trail_names[11], key='trail11'),sg.Push()],
               [sg.Push(), sg.Button(trail_names[12], key='trail12'), sg.Button(trail_names[13], key='trail13'), sg.Button(trail_names[14], key='trail14'),sg.Push()]]
    block_2 = [[sg.Push(), sg.Text('Get a better look at the trail by watching the video linked below!', font=('Avenir 20')), sg.Push()],
               [sg.Push(), sg.Text(ytLink, enable_events=True), sg.Push()]]
    block_3 = [[sg.Push(), sg.Button('OK', button_color=('black', '#f77c2f')), sg.Button('Back', button_color=('black', '#f77c2f')), sg.Push()]]

    layout = [[sg.Frame('', block_1, expand_x=True, expand_y=True)],
              [sg.Frame('', trails, expand_x=True, expand_y=True)],
              [sg.Frame('', block_2, expand_x=True,expand_y=True)],
              [sg.Frame('', block_3, expand_x=True, expand_y=True)]]
    
    return sg.Window('Search Results', layout, size=(1200,1000), finalize=True)

def make_win_trail():
    """ An information page on the selected trail """
    trail_names = trails_names()
    trail_images = trails_images()
    trail_urls = trails_urls()
    trail_description = trails_descriptiopn()
    trail_coord = trails_coord()

    layout = [[sg.Push(), sg.Image('logo_small.png'), sg.Push()],
             [sg.Push(), sg.Text(trail_names[0]), sg.Push()],
             [sg.Push(), sg.Text(trail_coord[0]), sg.Push()],
             [sg.Push(), sg.Text(trail_images[0]), sg.Push()],
             [sg.Push(), sg.Text(trail_description[0]), sg.Push()],
             [sg.Push(), sg.Text('For more info, visit here:'), sg.Text(trail_urls[0]), sg.Push()],
             [sg.Push(), sg.Button('OK', button_color=('black', '#f77c2f')), sg.Button('Back', button_color=('black', '#f77c2f')), sg.Push()]]
    

    return sg.Window('Trail Information', layout, size=(1200,1000), finalize=True)


def make_win_contact():
    """ A contact form for users to complete as needed """

    layout = [[sg.Push(), sg.Image('logo_small.png'), sg.Push()],
             [sg.Push(), sg.Text('Contact Us', font=('Avenir 20')), sg.Push()],
             [sg.Text('Name: ', size=(10,1)), sg.InputText('', key='contact_name')],
             [sg.Text('Email: ', size=(10,1)), sg.InputText('', key='contact_email')],
             [sg.Text('Question: ', size=(10,1)), sg.InputText('', key='contact_question')],
             [sg.Push(), sg.Button('Send', button_color=('black', '#f77c2f')), sg.Button('Back', button_color=('black', '#f77c2f')), sg.Push()]]

    return sg.Window('Contact Us', layout, size=(900, 1000), finalize=True)


def error_popup():
    """ Error message when invalid input is entered in """
    layout = [[sg.Push(), sg.Image('logo_smallest.png'), sg.Push()],
             [sg.Push(), sg.Text('A valid search entry is required', font=('Avenir 20')), sg.Push()],
             [sg.Push(), sg.Text('Please enter a city or state', font=('Avenir 20')), sg.Push()],
             [sg.Push(), sg.Button('OK', button_color=('black', '#f77c2f')), sg.Push()]]

    return sg.Window('Error', layout, size=(500,400), finalize=True)


def create_acc():
    """ A window for users to create new accounts """
    global username,password
    layout = [[sg.Push(), sg.Image('logo_small.png'), sg.Push()],
             [sg.Push(), sg.Text("Sign Up", font=('Avenir 20')), sg.Push()],
             [sg.Text("Full Name", size =(15, 1),font=('Avenir 16')), sg.InputText(key='-fname-', font=16)],
             [sg.Text("E-mail", size =(15, 1),font=('Avenir 16')), sg.InputText(key='-email-', font=16)],
             [sg.Text("Create Username", size =(15, 1), font=('Avenir 16')), sg.InputText(key='-username-', font=16)],
             [sg.Text("Create Password", size =(15, 1), font=('Avenir 16')), sg.InputText(key='-password-', font=16, password_char='*')],
             [sg.Push(), sg.Button('Submit', button_color=('black', '#f77c2f')), sg.Button('Cancel', button_color=('black', '#f77c2f')), sg.Push()]]

    return sg.Window('Sign up', layout, size=(900,1000), finalize=True)


def progress_bar():
    """ A progress bar to show progress in account creation """

    layout = [[sg.Push(), sg.Text('Creating your account...'), sg.Push()],
            [sg.ProgressBar(100, orientation='h', size=(40, 20), key='progbar')],
            [sg.Push(), sg.Cancel(), sg.Push()]]
    
    window = sg.Window('Working...', layout)
    for i in range(100):
        event, values = window.read(timeout=1)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        window['progbar'].update_bar(i + 1)
    window.close()
    sg.popup('Success! Your account has been created.')


def login():
    """ A login page for returning users """

    global username,password
    layout = [[sg.Push(), sg.Text('Login', font=('Avenir 16')), sg.Push()],
            [sg.Text("Username", font=('Avenir 16')),sg.InputText(key='-usrnm-', font=16)],
            [sg.Text("Password", font=('Avenir 16')),sg.InputText(key='-pwd-', password_char='*', font=16)],
            [sg.Push(), sg.Button('OK', button_color=('black', '#f77c2f')),sg.Button('Cancel', button_color=('black', '#f77c2f')), sg.Push()]]

    return sg.Window('Login', layout, size = (500, 400), finalize=True)

def make_win_geo():
    """ The geocoding results window """

    api = 'AIzaSyCziQ1u2q76jTMBnKPGZ1fMgYcYzNXdvs8'
    url = "https://maps.googleapis.com/maps/api/staticmap?"
    center = geo_add
    zoom = '10'
    markers_color = 'color:red|'
    markers_loc = center
    r = requests.get(url + 'sensor=false&v=3&visual;_refresh=true&'+ "center=" + center + "&zoom =" + zoom + "&size=800x600&" + "markers=" + markers_color + markers_loc + "&key=" + api)
    f = open('map.png', 'wb')
    f.write(r.content)
    f.close()

    block_1 = [[sg.Push(), sg.Image('logo_small.png'), sg.Push()], 
              [sg.Push(), sg.Text('Address to Geocoordinate Conversion', font=('Avenir 20')), sg.Push()]]
    block_2 = [[sg.Push(), sg.Image('map.png'), sg.Push()],
               [sg.Push(), sg.Text(geo_coord), sg.Push()]]
    block_3 = [[sg.Push(), sg.Button('OK', button_color=('black', '#f77c2f')), sg.Button('Back', button_color=('black', '#f77c2f')), sg.Push()]]

    layout = [[sg.Frame('', block_1, expand_x=True, expand_y=True)],
              [sg.Frame('', block_2, expand_x=True, expand_y=True)],
              [sg.Frame('', block_3, expand_x=True, expand_y=True)]]

    return sg.Window('Geocoodinates', layout, size=(900,1100), finalize=True)



######################################### Main Event Loop ###############################################

def main():

    """ Main window which holds the event loop """

    # Window declarations 
    win_home = make_win_home() 
    win_help = None 
    win_search = None
    win_contact = None 
    wind_err = None 
    win_create_acc = None 
    win_prog_bar = None
    win_login = None
    win_geo = None
    win_trail = None
    global geo_coord
    global geo_add
    global np_response
    global ytLink
    

    while True:

        window, event, values = sg.read_all_windows()

        # HomeScreen window
        if window == win_home:
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            elif event == 'Submit' and values['trail_search'].isnumeric():
                sg.popup('A valid non-numeric entry is required to search!', title='Error')
            elif event == 'Submit' and values['trail_search'] and not win_search:
                trail_search = str(values['trail_search'])
                y.start()
                ytLink = youtubeSearch(trail_search)
                np_response = np.trail_search(trail_search)
                win_search = make_win_search()
            elif event == 'Submit' and values['geo'] and not win_geo:
                geo_add = str(values['geo'])
                x.start()
                geo_coord = sc.socket_client(geo_add)
                geo_coord = geo_coord.decode('utf8')
                win_geo = make_win_geo()
            elif event == 'Help' and not win_help:
                win_help = make_win_help()
            elif event == 'Login' and not win_login:
                win_login = login()
            elif event == 'Sign up' and not win_create_acc:
                win_create_acc = create_acc()

        # Geocoordinate Results Window
        if window == win_geo:
            if event in(sg.WIN_CLOSED, 'OK', 'Back'):
                win_geo.close()
                win_geo = None

        # Create Account window 
        if window == win_create_acc:
            if event in (sg.WIN_CLOSED, 'Cancel'):
                win_create_acc.close()
                win_create_acc = None
            elif event == 'Submit':
                fullName = values['-fname-']
                username = values['-username-']
                password = values['-password-']
                email = values['-email-']
                progress_bar()
                win_create_acc.close()

        # Login Window
        if window == win_login:
            if event in (sg.WIN_CLOSED, 'Cancel'):
                win_login.close()
                win_login = None
            elif event == 'OK':
                if values['-usrnm-'] == username and values['-pwd-'] == password:
                    sg.popup("Welcome!")
                    win_login.close()
                elif values['-usrnm-'] != username or values['-pwd-'] != password:
                    sg.popup("Invalid login. Try again")

        # Help Window 
        if window == win_help:
            if event in (sg.WIN_CLOSED, 'OK'):
                win_help.close()
                win_help = None
            elif event == 'Contact Us':
                win_contact = make_win_contact()

        # Contact Us
        if window == win_contact:
            if event in (sg.WIN_CLOSED, 'Back'):
                win_contact.close()
                win_contact = None
            elif event == 'Send':
                contact_name = str(values['contact_name'])
                contact_email = str(values['contact_email'])
                contact_question = str(values['contact_question'])
                win_contact.close()
                win_contact = None 

        # Search Window 
        if window == win_search:
            if event in(sg.WIN_CLOSED, 'OK', 'Back'):
                win_search.close()
                win_search = None
            elif event == 'trail0':
                make_win_trail()
            elif event == 'trail1':
                make_win_trail()
            elif event == 'trail2':
                make_win_trail()
            elif event == 'trail3':
                make_win_trail()
            elif event == 'trail4':
                make_win_trail()
            elif event == 'trail5':
                make_win_trail()
            elif event == 'trail6':
                make_win_trail()
            elif event == 'trail7':
                make_win_trail()
            elif event == 'trail8':
                make_win_trail()
            elif event == 'trail9':
                make_win_trail()
            elif event == 'trail10':
                make_win_trail()
            elif event == 'trail11':
                make_win_trail()
            elif event == 'trail12':
                make_win_trail()
            elif event == 'trail13':
                make_win_trail()
            elif event == 'trail14':
                make_win_trail()           

if __name__ == '__main__':
    x = threading.Thread(target = ss.socket_server)
    y = threading.Thread(target = ytl.youtubeLinker)
    import NP_query as np
    main()
# a help page, contact page, as well as a main search page and a results page. 
# Future builds: Working to integrate the OSM maps to use for hiking waypoints, connecting DB to create user accounts, building an
# addiitonal window to view maps and download to device for offline use. 

from tkinter import Frame
import PySimpleGUI as sg
from OSMPythonTools.api import Api
from OSMPythonTools import overpass
from folium import Popup
from pymongo import MongoClient


sg.theme('DarkGrey13')
sg.set_options(font=("Avenir Next", 16))
username = ''
password = ''
client = MongoClient()
db = client.CS361 
# newUser = {
#     "username": "",
#     "password": "",
#     "Name": "",
#     "Email": ""
# }
# newUser = db.User_Authentication 

################################# Application Windows ###########################################

def make_win_home():
    """ Application Homescreen """

    block_1 = [[sg.Push(), sg.Text('Search Trails by State: '), sg.Push()], 
              [sg.Push(), sg.InputText('', size =(30,1), enable_events = True, key='search'), sg.Push()]]

    col_1 =[[sg.Push(), sg.Button('Submit', button_color=('black', '#f77c2f')), sg.Push(), sg.Button('Exit', button_color=('black', '#f77c2f')), sg.Push()],
            [sg.Push(), sg.Button('Help', button_color=('black', '#f77c2f')), sg.Push()]]

    col_2 = [[sg.Push(), sg.Button('Sign up', button_color=('black', '#f77c2f')), sg.Push(),sg.Button('Login', button_color=('black', '#f77c2f')), sg.Push()]]

    layout = [[sg.Push(), sg.Column(col_2)],
              [sg.Push(), sg.Image('logo.png'), sg.Push()],
              [sg.Push(), sg.Frame('', block_1, size=(900, 100), expand_x=True, expand_y=True, relief=sg.RELIEF_GROOVE, border_width=3), sg.Push()],
              [sg.Push(), sg.Column(col_1), sg.Push()]]

    return sg.Window('The Adventurer', layout, size=(900, 1000), finalize=True)

def make_win_help():
    """ Help Instructions Window """

    layout =[[sg.Push(), sg.Image('logo_small.png'), sg.Push()],
            [sg.Push (), sg.Text('To search for an adventure area, follow the below steps!'), sg.Push()],
            [sg.Push(), sg.Text('1. Enter a state in the search bar and hit submit'), sg.Push()],
            [sg.Push(), sg.Text('2. To find adventure areas by park name, city, or activity select \nthe Advanced Search options'), sg.Push()],
            [sg.Push(), sg.Text('3. Maps can be downloaded to your device for offline usage by selecting \nthe download icon and saving chosing a loction on your device to save it to'), sg.Push()],
            [sg.Push(), sg.Text('For more help, please contact us using the link below!'), sg.Push()],
            [sg.Push(), sg.Button('OK', button_color=('black', '#f77c2f')), sg.Button('Contact Us', button_color=('black', '#f77c2f')), sg.Push()]]     

    return sg.Window('Help', layout, size=(700, 800), finalize=True)

def make_win_search():
    """ Primary Search results window """

    block_1 = [[sg.Push(), sg.Image('logo_small.png'), sg.Push()], 
              [sg.Push(), sg.Text('Hiking Trails', font=('Avenir 20')), sg.Push()]]
    block_2 = [[sg.Push(), sg.Text('Under constructions, results coming soon!'), sg.Push()]]
    block_3 = [[sg.Push(), sg.Button('OK', button_color=('black', '#f77c2f')), sg.Button('Back', button_color=('black', '#f77c2f')), sg.Push()]]

    layout = [[sg.Frame('', block_1, expand_x=True, expand_y=True)],
              [sg.Frame('', block_2, expand_x=True, expand_y=True)],
              [sg.Frame('', block_3, expand_x=True, expand_y=True)]]
    
             

    return sg.Window('Search Results', layout, size=(900,1000), finalize=True)

def make_win_contact():
    """ A contact form for users to complete as needed """

    layout = [[sg.Push(), sg.Image('logo_small.png'), sg.Push()],
             [sg.Push(), sg.Text('Contact Us', font=('Avenir 20')), sg.Push()],
             [sg.Text('Name: ', size=(10,1)), sg.InputText('', key='contact_name')],
             [sg.Text('Email: ', size=(10,1)), sg.InputText('', key='contact_email')],
             [sg.Text('Question: ', size=(10,1)), sg.InputText('', key='contact_question')],
             [sg.Push(), sg.Button('Send', button_color=('black', '#f77c2f')), sg.Button('Back', button_color=('black', '#f77c2f')), sg.Push()]]

    return sg.Window('Contact Us', layout, size=(900, 1000), finalize=True)

def error_popup():
    """ Error message when invalid input is entered in """
    layout = [[sg.Push(), sg.Image('logo_smallest.png'), sg.Push()],
             [sg.Push(), sg.Text('A valid search entry is required', font=('Avenir 20')), sg.Push()],
             [sg.Push(), sg.Text('Please enter a city or state', font=('Avenir 20')), sg.Push()],
             [sg.Push(), sg.Button('OK', button_color=('black', '#f77c2f')), sg.Push()]]

    return sg.Window('Error', layout, size=(500,400), finalize=True)

def create_acc():
    """ A window for users to create new accounts """
    global username,password
    layout = [[sg.Push(), sg.Image('logo_small.png'), sg.Push()],
             [sg.Push(), sg.Text("Sign Up", font=('Avenir 20')), sg.Push()],
             [sg.Text("Full Name", size =(15, 1),font=('Avenir 16')), sg.InputText(key='-fname-', font=16)],
             [sg.Text("E-mail", size =(15, 1),font=('Avenir 16')), sg.InputText(key='-email-', font=16)],
             [sg.Text("Create Username", size =(15, 1), font=('Avenir 16')), sg.InputText(key='-username-', font=16)],
             [sg.Text("Create Password", size =(15, 1), font=('Avenir 16')), sg.InputText(key='-password-', font=16, password_char='*')],
             [sg.Push(), sg.Button('Submit', button_color=('black', '#f77c2f')), sg.Button('Cancel', button_color=('black', '#f77c2f')), sg.Push()]]

    return sg.Window('Sign up', layout, size=(900,1000), finalize=True)

def progress_bar():
    """ A progress bar to show progress in account creation """

    layout = [[sg.Push(), sg.Text('Creating your account...'), sg.Push()],
            [sg.ProgressBar(100, orientation='h', size=(40, 20), key='progbar')],
            [sg.Push(), sg.Cancel(), sg.Push()]]
    
    window = sg.Window('Working...', layout)
    for i in range(100):
        event, values = window.read(timeout=1)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        window['progbar'].update_bar(i + 1)
    window.close()
    sg.popup('Success! Your account has been created.')
    


def login():
    """ A login page for returning users """

    global username,password
    layout = [[sg.Push(), sg.Text('Login', font=('Avenir 16')), sg.Push()],
            [sg.Text("Username", font=('Avenir 16')),sg.InputText(key='-usrnm-', font=16)],
            [sg.Text("Password", font=('Avenir 16')),sg.InputText(key='-pwd-', password_char='*', font=16)],
            [sg.Push(), sg.Button('OK', button_color=('black', '#f77c2f')),sg.Button('Cancel', button_color=('black', '#f77c2f')), sg.Push()]]

    return sg.Window('Login', layout, size = (500, 400), finalize=True)


######################################### Main Event Loop ###############################################

def main():

    """ Main window which holds the event loop """

    # Window declarations 
    win_home = make_win_home() 
    win_help = None 
    win_search = None
    win_contact = None 
    wind_err = None 
    win_create_acc = None 
    win_prog_bar = None
    win_login = None
    
    while True:

        window, event, values = sg.read_all_windows()

        # HomeScreen window
        if window == win_home:
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            elif event == 'Submit' and values['search'] == "":
                sg.popup('A valid location entry is required to search!', title='Error')
            elif event == 'Submit' and values['search'].isnumeric():
                sg.popup('A valid non-numeric entry is required to search!', title='Error')
            elif event == 'Submit' and not win_search:
                user_search = str(values['search'])
                win_search = make_win_search()
            elif event == 'Help' and not win_help:
                win_help = make_win_help()
            elif event == 'Login' and not win_login:
                win_login = login()
            elif event == 'Sign up' and not win_create_acc:
                win_create_acc = create_acc()

        # Create Account window 
        if window == win_create_acc:
            if event in (sg.WIN_CLOSED, 'Cancel'):
                win_create_acc.close()
                win_create_acc = None
            elif event == 'Submit':
                fullName = values['-fname-']
                username = values['-username-']
                password = values['-password-']
                email = values['-email-']
                progress_bar()
                win_create_acc.close()

        # Login Window
        if window == win_login:
            if event in (sg.WIN_CLOSED, 'Cancel'):
                win_login.close()
                win_login = None
            elif event == 'OK':
                if values['-usrnm-'] == username and values['-pwd-'] == password:
                    sg.popup("Welcome!")
                    win_login.close()
                elif values['-usrnm-'] != username or values['-pwd-'] != password:
                    sg.popup("Invalid login. Try again")

        # Help Window 
        if window == win_help:
            if event in (sg.WIN_CLOSED, 'OK'):
                win_help.close()
                win_help = None
            elif event == 'Contact Us':
                win_contact = make_win_contact()

        # Contact Us
        if window == win_contact:
            if event in (sg.WIN_CLOSED, 'Back'):
                win_contact.close()
                win_contact = None
            elif event == 'Send':
                contact_name = str(values['contact_name'])
                contact_email = str(values['contact_email'])
                contact_question = str(values['contact_question'])
                win_contact.close()
                win_contact = None 

        # Search Window 
        if window == win_search:
            if event in(sg.WIN_CLOSED, 'OK', 'Back'):
                win_search.close()
                win_search = None
            #elif event == ...      > To be completed when search function is linked with maps

if __name__ == '__main__':
    main()
#     "username": "",
#     "password": "",
#     "Name": "",
#     "Email": ""
# }
# newUser = db.User_Authentication 

################################# Application Windows ###########################################

def make_win_home():
    """ Application Homescreen """

    block_1 = [[sg.Push(), sg.Text('Search Trails by State: '), sg.Push()], 
                [sg.Push(), sg.InputText('', size =(30,1), enable_events = True, key='search'), sg.Push()],
                [sg.Push(), sg.Button('Submit'), sg.Button('Exit'), sg.Push()],
                [sg.Push(), sg.Button('Help'), sg.Push()],
                [sg.Push(), sg.Button('Sign up'), sg.Button('Login'), sg.Push()]]

    layout = [[sg.Push(), sg.Image('logo.png'), sg.Push()],
              [sg.Frame('', block_1, pad=(0,0), expand_x=True, expand_y=True, relief=sg.RELIEF_GROOVE, border_width=3)]]

    return sg.Window('The Adventurer', layout, size=(900, 1000), finalize=True)

def make_win_help():
    """ Help Instructions Window """

    layout =[[sg.Push(), sg.Image('logo_small.png'), sg.Push()],
            [sg.Push (), sg.Text('To search for an adventure area, follow the below steps!'), sg.Push()],
            [sg.Push(), sg.Text('1. Enter a state in the search bar and hit submit'), sg.Push()],
            [sg.Push(), sg.Text('2. To find adventure areas by park name, city, or activity select \nthe Advanced Search options'), sg.Push()],
            [sg.Push(), sg.Text('3. Maps can be downloaded to your device for offline usage by selecting \nthe download icon and saving chosing a loction on your device to save it to'), sg.Push()],
            [sg.Push(), sg.Text('For more help, please contact us using the link below!'), sg.Push()],
            [sg.Push(), sg.Button('OK'), sg.Button('Contact Us'), sg.Push()]]     

    return sg.Window('Help', layout, size=(700, 800), finalize=True)

def make_win_search():
    """ Primary Search results window """

    block_1 = [[sg.Push(), sg.Image('logo_small.png'), sg.Push()], 
              [sg.Push(), sg.Text('Hiking Trails', font=('Avenir 20')), sg.Push()]]
    block_2 = [[sg.Push(), sg.Text('Under constructions, results coming soon!'), sg.Push()]]
    block_3 = [[sg.Push(), sg.Button('OK'), sg.Button('Back'), sg.Push()]]

    layout = [[sg.Frame('', block_1, expand_x=True, expand_y=True)],
              [sg.Frame('', block_2, expand_x=True, expand_y=True)],
              [sg.Frame('', block_3, expand_x=True, expand_y=True)]]
    
             

    return sg.Window('Search Results', layout, size=(900,1000), finalize=True)

def make_win_contact():
    """ A contact form for users to complete as needed """

    layout = [[sg.Push(), sg.Image('logo_small.png'), sg.Push()],
             [sg.Push(), sg.Text('Contact Us', font=('Avenir 20')), sg.Push()],
             [sg.Text('Name: ', size=(10,1)), sg.InputText('', key='contact_name')],
             [sg.Text('Email: ', size=(10,1)), sg.InputText('', key='contact_email')],
             [sg.Text('Question: ', size=(10,1)), sg.InputText('', key='contact_question')],
             [sg.Push(), sg.Button('Send'), sg.Button('Back'), sg.Push()]]

    return sg.Window('Contact Us', layout, size=(900, 1000), finalize=True)

def error_popup():
    """ Error message when invalid input is entered in """
    layout = [[sg.Push(), sg.Image('logo_smallest.png'), sg.Push()],
             [sg.Push(), sg.Text('A valid search entry is required', font=('Avenir 20')), sg.Push()],
             [sg.Push(), sg.Text('Please enter a city or state', font=('Avenir 20')), sg.Push()],
             [sg.Push(), sg.Button('OK'), sg.Push()]]

    return sg.Window('Error', layout, size=(500,400), finalize=True)

def create_acc():
    """ A window for users to create new accounts """
    global username,password
    layout = [[sg.Push(), sg.Image('logo_small.png'), sg.Push()],
             [sg.Push(), sg.Text("Sign Up", font=('Avenir 20')), sg.Push()],
             [sg.Text("Full Name", size =(15, 1),font=('Avenir 16')), sg.InputText(key='-fname-', font=16)],
             [sg.Text("E-mail", size =(15, 1),font=('Avenir 16')), sg.InputText(key='-email-', font=16)],
             [sg.Text("Create Username", size =(15, 1), font=('Avenir 16')), sg.InputText(key='-username-', font=16)],
             [sg.Text("Create Password", size =(15, 1), font=('Avenir 16')), sg.InputText(key='-password-', font=16, password_char='*')],
             [sg.Push(), sg.Button('Submit'), sg.Button('Cancel'), sg.Push()]]

    return sg.Window('Sign up', layout, size=(900,1000), finalize=True)

def progress_bar():
    """ A progress bar to show progress in account creation """

    layout = [[sg.Push(), sg.Text('Creating your account...'), sg.Push()],
            [sg.ProgressBar(100, orientation='h', size=(40, 20), key='progbar')],
            [sg.Push(), sg.Cancel(), sg.Push()]]
    
    window = sg.Window('Working...', layout)
    for i in range(100):
        event, values = window.read(timeout=1)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
        window['progbar'].update_bar(i + 1)
    window.close()
    sg.popup('Success! Your account has been created.')
    


def login():
    """ A login page for returning users """

    global username,password
    layout = [[sg.Push(), sg.Text('Login', font=('Avenir 16')), sg.Push()],
            [sg.Text("Username", font=('Avenir 16')),sg.InputText(key='-usrnm-', font=16)],
            [sg.Text("Password", font=('Avenir 16')),sg.InputText(key='-pwd-', password_char='*', font=16)],
            [sg.Push(), sg.Button('OK'),sg.Button('Cancel'), sg.Push()]]

    return sg.Window('Login', layout, size = (500, 400), finalize=True)


######################################### Main Event Loop ###############################################

def main():

    """ Main window which holds the event loop """

    # Window declarations 
    win_home = make_win_home() 
    win_help = None 
    win_search = None
    win_contact = None 
    wind_err = None 
    win_create_acc = None 
    win_prog_bar = None
    win_login = None
    
    while True:

        window, event, values = sg.read_all_windows()

        # HomeScreen window
        if window == win_home:
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            elif event == 'Submit' and values['search'] == "":
                sg.popup('A valid location entry is required to search!', title='Error')
            elif event == 'Submit' and values['search'].isnumeric():
                sg.popup('A valid non-numeric entry is required to search!', title='Error')
            elif event == 'Submit' and not win_search:
                user_search = str(values['search'])
                win_search = make_win_search()
            elif event == 'Help' and not win_help:
                win_help = make_win_help()
            elif event == 'Login' and not win_login:
                win_login = login()
            elif event == 'Sign up' and not win_create_acc:
                win_create_acc = create_acc()

        # Create Account window 
        if window == win_create_acc:
            if event in (sg.WIN_CLOSED, 'Cancel'):
                win_create_acc.close()
                win_create_acc = None
            elif event == 'Submit':
                fullName = values['-fname-']
                username = values['-username-']
                password = values['-password-']
                email = values['-email-']
                progress_bar()
                win_create_acc.close()

        # Login Window
        if window == win_login:
            if event in (sg.WIN_CLOSED, 'Cancel'):
                win_login.close()
                win_login = None
            elif event == 'OK':
                if values['-usrnm-'] == username and values['-pwd-'] == password:
                    sg.popup("Welcome!")
                    win_login.close()
                elif values['-usrnm-'] != username or values['-pwd-'] != password:
                    sg.popup("Invalid login. Try again")

        # Help Window 
        if window == win_help:
            if event in (sg.WIN_CLOSED, 'OK'):
                win_help.close()
                win_help = None
            elif event == 'Contact Us':
                win_contact = make_win_contact()

        # Contact Us
        if window == win_contact:
            if event in (sg.WIN_CLOSED, 'Back'):
                win_contact.close()
                win_contact = None
            elif event == 'Send':
                contact_name = str(values['contact_name'])
                contact_email = str(values['contact_email'])
                contact_question = str(values['contact_question'])
                win_contact.close()
                win_contact = None 

        # Search Window 
        if window == win_search:
            if event in(sg.WIN_CLOSED, 'OK', 'Back'):
                win_search.close()
                win_search = None
            #elif event == ...      > To be completed when search function is linked with maps

if __name__ == '__main__':
    main()