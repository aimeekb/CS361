# data_entry_app.py
"""The ABQ Data Entry application
"""
from cgitb import text
from distutils.command.install_egg_info import to_filename
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from pathlib import Path
import csv
from xmlrpc.server import resolve_dotted_attribute

################### Data Window Portion ##################################### 

variables = dict()
records_saved = 0

root = tk.Tk()
root.title('ABQ Data Entry Application')

# Configured the layout which will allow the first column to expand
# Even though this form will only have one column, by setting it we will
# allow our form to remain centered on the application if the window is expanded
root.columnconfigure(0, weight=1)

# Since we won't need to interact with the widget again, we can keep the code cleaner
# by calling .grid() at the same time and not assigning it to a variable
ttk.Label(
    root, 
    text='ABQ Data Entry Application',
    font= ('TkDefaultFont', 16)
).grid()

########################### Framing & Formating Portion #############################

# Creating the frame that will contain our label frames for greater organization
drf = ttk.Frame(root)
drf.grid(padx=10, sticky=(tk.E + tk.W))
drf.columnconfigure(0, weight=1)

# Creaing the label fram where we will enter our data entry fields 
r_info = ttk.LabelFrame(drf, text='Record Information')
r_info.grid(sticky=(tk.W + tk.E))
for i in range(3):
    r_info.columnconfigure(i, weight=1)
    
########################### Data Entry Fields ###########################

# For each item, we create a variable, Label, and input widget for each item
variables['Date'] = tk.StringVar()
ttk.Label(r_info, text='Date').grid(row=0, column=0)
ttk.Entry(
    r_info,
    textvariable = variables['Date']
    ).grid(row=1, column=0, sticky=(tk.W + tk.E))

# List for out Combobox
time_values= ['8:00', '12:00', '16:00', '20:00']
variables['Time'] = tk.StringVar()
tk.Label(r_info, text='Time').grid(row = 0, column = 1)

# Since Combobox takes a list of strings for its values argument, so we'll pass in out list above time_values
ttk.Combobox(
    r_info, textvariable= variables['Time'], values= time_values).grid(row = 1, column = 1, sticky= (tk.W + tk.E))

variables['Technician'] = tk.StringVar()
ttk.Label(r_info, textvariable= variables['Technician']).grid(row=1, column=2, sticky=(tk.W + tk.E))

variables['Labs'] = tk.StringVar()
ttk.Label(r_info, text='Lab').grid(row=2, column=0)

# Creating a frame that will hold our Labs Radiobuttons
labframe = ttk.Frame(r_info)

# A for loop for creating the Radiobuttons widgets, helps keep the code clean and concise
for lab in ('A', 'B', 'C'):
    ttk.Radiobutton(
        labframe, value=lab, text=lab, variable=variables['Labs']
    ).pack(side=tk.LEFT, expand=True) # We use pack here because it's simple to to tell it right or left without having to worry about columns
labframe.grid(row=3, column=0, sticky=(tk.W + tk.E))

variables['Plot'] = tk.IntVar()
ttk.Label(r_info,text='Plot').grid(row=2, column=1)
ttk.Combobox(
    r_info,
    textvariable = variables['Plot'],
    values=list(range(1, 21)) # Using range to generate a list to keep the code clean                   
).grid(row=3, column=1, sticky=(tk.W + tk.E))

variables['Seed Sample'] = tk.StringVar()
ttk.Label(r_info, text='Seed Sample').grid(row=2, column=2)
ttk.Entry(
    r_info,
    textvariable=variables['Seed Sample']
    ).grid(row=3, column=2, sticky=(tk.W + tk.E))

############################### Environment Data Section #########################################

# Creating the frame that will contain our label frames for greater organization, same as above
e_info = ttk.LabelFrame(drf, text='Environment Data')
e_info.grid(sticky=(tk.W + tk.E))
for i in range (3):
    e_info.columnconfigure(i, weight=1)

variables['Humidity'] = tk.DoubleVar()
ttk.Label(e_info, text='Humidity (g/m3)').grid(row=0, column=0)
ttk.Spinbox(
    e_info, textvariable=variables['Humidity'],
    from_=0.5, to=52.0, increment=0.01,
).grid(row=1, column=0, sticky=(tk.W + tk.E))

variables['Light'] = tk.DoubleVar()
ttk.Label(e_info, text='Light (klx)').grid(row=0, column=1)
ttk.Spinbox(
    e_info,
    textvariable = variables['Light'],
    from_= 0, to=100, increment= 0.01
).grid(row=1, column=1, sticky=(tk.W + tk.E))

variables['Temperature'] = tk.DoubleVar()
ttk.Label(e_info, text='Temperature (C)').grid(row=0, column=2)
ttk.Spinbox(
    e_info,
    textvariable = variables['Temperature'],
    from_= 0, to=40, increment= 0.01
).grid(row=1, column=2, sticky=(tk.W + tk.E))

variables['Equipment Fault'] = tk.BooleanVar()
ttk.Checkbutton(
    e_info, variable=variables['Equipment Fault'],
    text='Equipment Fault'
).grid(row=2, column=0, sticky=(tk.W + tk.E))

############################# Plant Data Section ############################################## 

p_info = ttk.LabelFrame(drf, text='Plant Data')
p_info.grid(sticky=(tk.W + tk.E))
for i in range(3):
    p_info.columnconfigure(i, weight=1)
    
variables['Plants'] = tk.IntVar()
ttk.Label(p_info, text='Plants').grid(row=0, column=0)
ttk.Spinbox(
    p_info, textvariable=variables['Plants'],
    from_=0, to=20, increment=1
).grid(row=1, column=0, sticky=(tk.W + tk.E))

variables['Blossoms'] = tk.IntVar()
ttk.Label(p_info, text='Blossoms').grid(row=0, column=1)
ttk.Spinbox(
    p_info, textvariable=variables['Blossoms'],
    from_=0, to=1000, increment=1
).grid(row=1, column=1, sticky=(tk.W + tk.E))

variables['Fruit'] = tk.IntVar()
ttk.Label(p_info, text='Fruit').grid(row=0, column=2)
ttk.Spinbox(
    p_info, textvariable=variables['Fruit'],
    from_=0, to=1000, increment=1
).grid(row=1, column=2, sticky=(tk.W + tk.E))

variables['Min Height'] = tk.DoubleVar()
ttk.Label(p_info, text='Min Height (cm)').grid(row=2, column=0)
ttk.Spinbox(
    p_info, textvariable=variables['Min Height'],
    from_=0, to=1000, increment=0.01
).grid(row=3, column=0, sticky=(tk.W + tk.E))

variables['Max Height'] = tk.DoubleVar()
ttk.Label(p_info, text='Max Height (cm)').grid(row=2, column=1)
ttk.Spinbox(
    p_info, textvariable=variables['Max Height'],
    from_=0, to=1000, increment=0.01
).grid(row=3, column=1, sticky=(tk.W + tk.E))

variables['Med Height'] = tk.DoubleVar()
ttk.Label(p_info, text='Med Height (cm)').grid(row=3, column=0)
ttk.Spinbox(
    p_info, textvariable=variables['Med Height'],
    from_=0, to=1000, increment=0.01
).grid(row=3, column=2, sticky=(tk.W + tk.E))

########################## Notes section #################################

# We add this dierctly to the drf frame, no need to create another frame for it
ttk.Label(drf, text='Notes').grid()

# Since we cannot create a control variable for the text widget, we have to create a variable that can reference it
notes_inp = tk.Text(drf, width=75, height=10)
notes_inp.grid(sticky=(tk.W + tk.E))

########################## Submission Buttons ############################# 

# To keep formatting simple, we have packed the save and reset buttons into a subframe so we can use the 
# geometrey handler pack instead of grid
buttons = tk.Frame(drf)
buttons.grid(sticky=(tk.W + tk.E))
save_button = ttk.Button(buttons, text='Save')
save_button.pack(side=tk.RIGHT)

reset_button = ttk.Button(buttons, text='Reset')
reset_button.pack(side=tk.RIGHT)

############################ Status Bar ################################## 

status_variable = tk.StringVar()
ttk.Label(
    root, textvariable = status_variable
).grid(sticky=(tk.W + tk.E), row=99, padx=10)
