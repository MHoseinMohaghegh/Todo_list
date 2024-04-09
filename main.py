# Import necessary libraries
import tkinter as tk
import tkinter
from tkinter import ttk
from tkinter import *
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("data_base.db")

# Create a cursor object to execute SQL commands
cur = conn.cursor()

# Create tables for each day of the week to store task descriptions
for day in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']:
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {day.lower()} (
        task_description varchar(2000)
    )""")

# Define a function to display tasks for the selected day


def show():
    try:
        # Get the selected day from the combobox
        day = day_combobox.get()
    except:
        # Print an error message if the day cannot be retrieved
        print("Error getting day from combobox")
        return

    try:
        # Connect to the database
        conn = sqlite3.connect('data_base.db')
        cur = conn.cursor()

        # Retrieve tasks for the selected day from the database
        cur.execute(f'SELECT task_description FROM {day.lower()}')
        tasks = cur.fetchone()

        # If tasks are found, display them in the text widget
        if tasks:
            data.delete('1.0', tkinter.END)
            data.insert(tkinter.END, tasks[0])
        else:
            # If no tasks are found, display a message
            print(f"No tasks found for {day}.")
            data.delete("1.0", "end")
            data.insert(tkinter.END, f"No tasks found for {day}.")
    except Exception as e:
        # Print an error message if an exception occurs during execution of SQL query
        print("An error occurred while executing SQL query:", e)
    finally:
        # Close the database connection
        conn.close()

# Define a function to save tasks for the selected day


def save():
    try:
        # Get the selected day from the combobox
        day = day_combobox.get()
    except:
        # Print an error message if the day cannot be retrieved
        print("Error getting day from combobox")
        return

    # Get the tasks entered by the user from the text widget
    tasks = str(data.get("1.0", "end-1c"))

    try:
        # Connect to the database
        conn = sqlite3.connect('data_base.db')
        cur = conn.cursor()

        # Delete existing tasks for the selected day
        cur.execute(f"DELETE FROM {day.lower()}")

        # Insert new tasks for the selected day into the database
        cur.execute(f"INSERT INTO {day.lower()
                                   } (task_description) VALUES (?)", (tasks,))
        conn.commit()

        # Clear the text widget after saving tasks
        data.delete("1.0", "end")
    except Exception as e:
        # Print an error message if an exception occurs during saving tasks
        print("An error occurred while saving tasks:", e)
    finally:
        # Close the database connection
        conn.close()

# Define a function to clear tasks for the selected day


def clear():
    try:
        # Get the selected day from the combobox
        day = day_combobox.get()
    except:
        # Print an error message if the day cannot be retrieved
        print("Error getting day from combobox")
        return
    try:
        # Connect to the database
        conn = sqlite3.connect('data_base.db')
        cur = conn.cursor()

        # Delete all tasks for the selected day from the database
        cur.execute(f"DELETE FROM {day.lower()}")
        conn.commit()

        # Clear the text widget after clearing tasks
        data.delete("1.0", "end")
    except Exception as e:
        # Print an error message if an exception occurs during clearing tasks
        print("An error occurred while clearing tasks:", e)
    finally:
        # Close the database connection
        conn.close()


# Create the main application window
window = tk.Tk()
window.title("Todo")
frame = tkinter.Frame(window)
frame.pack()

# Create a frame for buttons
buttons_frame = tkinter.Frame(frame)
buttons_frame.grid(row=0, column=0, sticky='N')

# Create a label for the combobox
combobox_label = tkinter.Label(buttons_frame, text='Choose Day:')
combobox_label.grid(row=0, column=0, padx=5, pady=2)

# Create a combobox to select the day
day_combobox = ttk.Combobox(buttons_frame, values=['Sunday', 'Monday', 'Tuesday',
                                                   'Wednesday', 'Thursday', 'Friday', 'Saturday'])
day_combobox.grid(row=1, column=0, padx=5, pady=2)

# Create a button to show tasks for the selected day
show_button = tkinter.Button(
    buttons_frame, text='Show', height=1, width=10, command=show)
show_button.grid(row=2, column=0, padx=5, pady=2)

# Create a button to clear tasks for the selected day
clear_button = tkinter.Button(
    buttons_frame, text='Clear', height=1, width=10, command=clear)
clear_button.grid(row=3, column=0, padx=5, pady=2)

# Create a button to save tasks for the selected day
save_button = tkinter.Button(
    buttons_frame, text='Save', height=1, width=10, command=save)
save_button.grid(row=4, column=0, padx=5, pady=2)

# Create a label frame to contain the text widget
description_label_frame = tkinter.LabelFrame(frame)
description_label_frame.grid(row=0, column=1)

# Create a text widget to display tasks
data = tkinter.Text(description_label_frame, height=10,
                    width=40, font=("Helvetica", 12))
data.grid(row=0, column=0)

# scrollbar for the text widget
scrollbar = tkinter.Scrollbar(
    description_label_frame, orient="vertical", command=data.yview)
scrollbar.grid(row=0,    column=1, sticky='ns')
data.config(yscrollcommand=scrollbar.set)

# Start the main event loop
window.mainloop()
