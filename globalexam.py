import tkinter as tk
from time import sleep
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


# Initiliaze the driver and global exam login
def init_globalexam(driver, delay):

    driver.get("https://auth.global-exam.com/login")

    driver.maximize_window()

    sleep(delay)


# Login to the global exam website with the user and password
def login_globalexam(driver, delay, username, password):
    usernameField = driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(username)
    passwordField = driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
    
    loginButton = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div/div/div/div/form/div[3]/button').click()
    
    sleep(delay)

# Function to loop for solving exercie
# it can be in the exam or general subdomain
def solve_next_exercice(driver, delay, subdomain, stepExercice, delayExercice):

    # Go to exercices page
    driver.get("https://"+subdomain+".global-exam.com/library/study-sheets/categories/grammar")
    
    sleep(delay)
    
    # Find all the button that has "Me tester" inside and click on the first one
    buttonsExercices = driver.find_elements(By.XPATH, "//button[contains(.,'Me tester')]")
    clickOnFirstButton = buttonsExercices[0].click()
    
    sleep(delay)
    
    # Select the first input of the exercice and fill it with the letter "h"
    if subdomain == "exam":
        inputField = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/input').click()
        inputField = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/input').send_keys('h')
    else:
        inputField = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div/input').click()
        inputField = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div/input').send_keys('h')
    
    # Create an action chain to fill the rest of the inputs with the letter "h"
    actions = ActionChains(driver)
    
    for input in range(1, 10):
        actions = actions.send_keys(Keys.TAB)
        actions = actions.send_keys('h')
    actions.perform()
    
    # click on the submit button
    if subdomain == "exam":
        submit_exercie = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/button').click()
    else:
        submit_exercie = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/button').click()
    
    sleep(delay)

    # Create a list of all correct answers
    correct_answers = list()

    # Find all the buttons for the correction of the exercice
    buttonsAnswers = driver.find_elements(By.XPATH, "//button[contains(@class,'lg:w-10')]")
    
    # For each button, click on it and get the correction
    for element in range(0, 10):
        buttonsAnswers[element].click()
        correction = driver.find_element(By.XPATH, "//span[contains(@class,'text-success-80')]")
        correct_answers.append(correction.text)
    
    # Go back to the exercice page
    driver.get("https://"+subdomain+".global-exam.com/library/study-sheets/categories/grammar")
    
    sleep(3)
    
    # Find the last button that has "Relancer" inside and click on it.
    # This is for selecting the same exercice as before
    # The stepExercice is for skipping multiple "Relancer" button that may appear if the user
    # had already done some exercice in between "Me tester" button
    buttonsExercices = driver.find_elements(By.XPATH, "//button[contains(.,'Relancer')]")
    clickOnLastButton = buttonsExercices[-1+stepExercice].click()
    
    sleep(delay)

    # Select the first input, click on it and fill the first correct answer
    if subdomain == "exam":
        inputField = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/input').click()
        inputField = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/input').send_keys(correct_answers[0])
    else:
        inputField = driver.find_element(By.XPATH, 'html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div/input').click()
        inputField = driver.find_element(By.XPATH, 'html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div/input').send_keys(correct_answers[0])

    # Create an action chain to fill the rest of the inputs with the correct answers
    actions = ActionChains(driver)
    for input in range(1, 10):
        actions = actions.send_keys(Keys.TAB)
        actions = actions.send_keys(correct_answers[input])
    actions.perform()
    
    # Add a delay to resolve the exercice
    sleep(delayExercice)
    
    # click on the submit button
    if subdomain == "exam":
        submit_exercie = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/button').click()
    else:
        submit_exercie = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/button').click()
    
    sleep(delay)

# Function to solve a selected exercice
# The exercice number is the number of the exercice in the list of exercice.
# To setup this exerciceNumber value, you must mannualy count the exercice taht you want the script to solve
def selected_re_solve_exercice(driver, delay, exerciceNumber, subdomain, delayExercice):

    # Go to exercices page
    driver.get("https://"+subdomain+".global-exam.com/library/study-sheets/categories/grammar")

    sleep(delay)

    # Find all the button that has "Me tester" inside and click on the first one
    buttonsExercices = driver.find_elements(By.XPATH, "//button[contains(.,'Relancer')]")
    clickOnFirstButton = buttonsExercices[exerciceNumber].click()

    sleep(delay)


    # Fill all the exercice inputs with the letter "h"
    if subdomain == "exam":

        inputField = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/input').click()
        inputField = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/input').send_keys('h')
    
    else:
        inputField = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div/input').click()
        inputField = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div/input').send_keys('h')

    # Fill all the input with the letter "h"
    actions = ActionChains(driver)

    for input in range(1, 10):
        actions = actions.send_keys(Keys.TAB)
        actions = actions.send_keys('h')

    actions.perform()

    # click on the submit button
    if subdomain == "exam":
        
        submit_exercie = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/button').click()
    
    else:
    
        submit_exercie = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/button').click()


    sleep(delay+1)

    correct_answers = list()

    # Get all the buttons for each response of the exercice
    buttonsAnswers = driver.find_elements(By.XPATH, "//button[contains(@class,'lg:w-10')]")

    # For each button, click on it and get the correction
    for element in range(0, 10):
        # click on the button
        buttonsAnswers[element].click()

        # Get the correct answer
        correction = driver.find_element(By.XPATH, "//span[contains(@class,'text-success-80')]")

        # Append this answers to a list
        correct_answers.append(correction.text)

    # Go back to the exercice page
    driver.get("https://"+subdomain+".global-exam.com/library/study-sheets/categories/grammar")

    sleep(delay)

    # Go back to the selected exercice
    buttonsExercices = driver.find_elements(By.XPATH, "//button[contains(.,'Relancer')]")
    clickOnLastButton = buttonsExercices[exerciceNumber].click()

    sleep(delay)

    # Click on the first input and put the correct answer in it
    if subdomain == "exam":

        inputField = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/input').click()
        inputField = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/input').send_keys(correct_answers[0])
    
    else:

        inputField = driver.find_element(By.XPATH, 'html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div/input').click()
        inputField = driver.find_element(By.XPATH, 'html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div/input').send_keys(correct_answers[0])


    # Fill all the input with the correct answers
    actions = ActionChains(driver)

    for input in range(1, 10):
        actions = actions.send_keys(Keys.TAB)
        actions = actions.send_keys(correct_answers[input])

    actions.perform()

    # Add a delay to resolve the exercice
    sleep(delayExercice)

    # click on the submit button
    if subdomain == "exam":

        submit_exercie = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/button').click()
    
    else:

        submit_exercie = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/button').click()

    sleep(delay)


# Function to invert a number
# This is used for the stepExercice input
def invert_number(a):
    return -a

# Create the main window
window = tk.Tk()
window.title("GlobalExam Solver")
window.geometry("950x800")

# ==== Add a solve for exercice tab ====

# Add title
title_label = tk.Label(window, text="Solve every exercice possible on GlobalExam !", font=("Arial", "12", "bold"))
title_label.pack()
title_label.place(x=100, y=20)

# Add prompt for the user and the password
username_label = tk.Label(window, text="Username:")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()
password_label = tk.Label(window, text="Password:")
password_label.pack()
password_entry = tk.Entry(window)
password_entry.pack()
username_label.place(x=100, y=50)
username_entry.place(x=100, y=80)
password_label.place(x=100, y=110)
password_entry.place(x=100, y=140)


# Add spacing
spacing_label = tk.Label(window, text="")
spacing_label.pack()
spacing_label.place(x=100, y=170)

# Add prompt for a delay with default value
delay_label = tk.Label(window, text="Add a general delay (default 2) \n For slow connection use 4 :")
delay_label.pack()
delay_entry = tk.Entry(window)
delay_entry.insert(0, "2")  # Set default value
delay_entry.pack()
delay_label.place(x=100, y=200)
delay_entry.place(x=100, y=230)

# Add spacing
spacing_label = tk.Label(window, text="")
spacing_label.pack()
spacing_label.place(x=100, y=260)

# Create the subdomain label and entry
subdomain_label = tk.Label(window, text="Solve exercice for the selected subdomain (exam, general):")
subdomain_label.pack()
subdomain_entry = tk.Entry(window)
subdomain_entry.insert(0, "exam")  # Set default value
subdomain_entry.pack()
subdomain_label.place(x=100, y=290)
subdomain_entry.place(x=100, y=320)

# Add spacing
spacing_label = tk.Label(window, text="")
spacing_label.pack()
spacing_label.place(x=100, y=350)

# Create a input for the step of the exercice
stepExercice_label = tk.Label(window, text="If you already solve some exercice at the bottom of the page \n You must add a step to skip this exercice (default 0) :")
stepExercice_label.pack()
stepExercice_entry = tk.Entry(window)
stepExercice_entry.insert(0, "0")  # Set default value
stepExercice_entry.pack()
stepExercice_label.place(x=100, y=380)
stepExercice_entry.place(x=100, y=410)

# Add spacing
spacing_label = tk.Label(window, text="")
spacing_label.pack()
spacing_label.place(x=100, y=440)

# Add delay to resolve the exercice
delayExercice_label = tk.Label(window, text="Add a delay in seconde to resolve exercice (default 0) :")
delayExercice_label.pack()
delayExercice_entry = tk.Entry(window)
delayExercice_entry.insert(0, "0")  # Set default value
delayExercice_entry.pack()
delayExercice_label.place(x=100, y=470)
delayExercice_entry.place(x=100, y=500)


# Add spacing
spacing_label = tk.Label(window, text="")
spacing_label.pack()
spacing_label.place(x=100, y=530)

# Add spacing
spacing_label = tk.Label(window, text="")
spacing_label.pack()
spacing_label.place(x=100, y=560)

def on_solve_next_exercice():
    subdomain = subdomain_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    delay = int(delay_entry.get())
    stepExercice = invert_number(int(stepExercice_entry.get()))
    delayExercice = int(delayExercice_entry.get())
    
    # Downlaod and start the driver
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    # Print a message to the user to not close the window
    print("/!\ Do not close this window ! /!\\ \n\n")

    # Initiliaze the driver and login to the global exam website
    init_globalexam(driver, delay)
    login_globalexam(driver, delay, username, password)

    # Loop to solve every exercice
    while True:
        solve_next_exercice(driver, delay, subdomain, stepExercice, delayExercice)

# Create the solve next exercice button
solve_next_exercice_button = tk.Button(window, text="Solve exercice", command=on_solve_next_exercice)
solve_next_exercice_button.pack()
solve_next_exercice_button.place(x=100, y=590)


## ==== Add a selected re-solve exercice button ====

# Add title
title_label = tk.Label(window, text="Solve a selected exercice \n (you must count the line of the exercice)", font=("Arial", "12", "bold"))
title_label.pack()
title_label.place(x=550, y=10)

# Add prompt for the user and the password
selected_username_label = tk.Label(window, text="Username:")
selected_username_label.pack()
selected_username_entry = tk.Entry(window)
selected_username_entry.pack()
selected_password_label = tk.Label(window, text="Password:")
selected_password_label.pack()
selected_password_entry = tk.Entry(window)
selected_password_entry.pack()
selected_username_label.place(x=550, y=50)
selected_username_entry.place(x=550, y=80)
selected_password_label.place(x=550, y=110)
selected_password_entry.place(x=550, y=140)

# Add spacing
spacing_label = tk.Label(window, text="")
spacing_label.pack()
spacing_label.place(x=550, y=170)

# Add prompt for a delay with default value
selected_delay_label = tk.Label(window, text="Add a general delay (default 2) \n For slow connection use 4 :")
selected_delay_label.pack()
selected_delay_entry = tk.Entry(window)
selected_delay_entry.insert(0, "2")  # Set default value
selected_delay_entry.pack()
selected_delay_label.place(x=550, y=200)
selected_delay_entry.place(x=550, y=230)

# Add spacing
spacing_label = tk.Label(window, text="")
spacing_label.pack()
spacing_label.place(x=550, y=260)

# Create the subdomain label and entry
selected_subdomain_label = tk.Label(window, text="Solve exercice for the selected subdomain (exam, general):")
selected_subdomain_label.pack()
selected_subdomain_entry = tk.Entry(window)
selected_subdomain_entry.insert(0, "exam")  # Set default value
selected_subdomain_entry.pack()
selected_subdomain_label.place(x=550, y=290)
selected_subdomain_entry.place(x=550, y=320)

# Add spacing
spacing_label = tk.Label(window, text="")
spacing_label.pack()
spacing_label.place(x=550, y=350)

# Create a input for the number of the exercice
selected_number_exercice_label = tk.Label(window, text="Enter the selected number of the exercice to solve :")
selected_number_exercice_label.pack()
selected_exercice_number_entry = tk.Entry(window)
selected_exercice_number_entry.insert(0, "0")  # Set default value
selected_exercice_number_entry.pack()
selected_number_exercice_label.place(x=550, y=380)
selected_exercice_number_entry.place(x=550, y=410)

# Add spacing
spacing_label = tk.Label(window, text="")
spacing_label.pack()
spacing_label.place(x=550, y=440)

# Add delay to resolve the exercice
selected_delayExercice_label = tk.Label(window, text="Add a delay in seconde to resolve selected exercice (default 0) :")
selected_delayExercice_label.pack()
selected_delayExercice_entry = tk.Entry(window)
selected_delayExercice_entry.insert(0, "0")  # Set default value
selected_delayExercice_entry.pack()
selected_delayExercice_label.place(x=550, y=470)
selected_delayExercice_entry.place(x=550, y=500)


# Add spacing
spacing_label = tk.Label(window, text="")
spacing_label.pack()
spacing_label.place(x=550, y=530)

# Add spacing
spacing_label = tk.Label(window, text="")
spacing_label.pack()
spacing_label.place(x=550, y=560)


def on_selected_re_solve_exercice():
    subdomain = selected_subdomain_entry.get()
    username = selected_username_entry.get()
    password = selected_password_entry.get()
    delay = int(selected_delay_entry.get())
    exerciceNumber = int(selected_exercice_number_entry.get())
    delayExercice = int(selected_delayExercice_entry.get())

    # Downlaod and start the driver
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    # Print a message to the user to not close the window
    print("/!\ Do not close this window ! /!\\ \n\n")

    # Initiliaze the driver and login to the global exam website
    init_globalexam(driver, delay)
    login_globalexam(driver, delay, username, password)

    # Solve the selected exercice
    selected_re_solve_exercice(driver, delay, exerciceNumber, subdomain, delayExercice)

    driver.quit()

# Create the solve next exercice button
solve_next_exercice_button = tk.Button(window, text="Solve selected exercice", command=on_selected_re_solve_exercice)
solve_next_exercice_button.pack()
solve_next_exercice_button.place(x=550, y=590)

# Add spacing
spacing_label = tk.Label(window, text="")
spacing_label.pack()
spacing_label.place(x=100, y=620)

# add a quit button
quit_button = tk.Button(window, text="Exit", command=window.quit)
quit_button.pack()
quit_button.place(x=450, y=700)

# Place credit for the developer
credit_label = tk.Label(window, text="Developed by Nv3l", font=("Arial", "8", "bold"), fg="grey")
credit_label.pack()
credit_label.place(x=400, y=740)
contact_label = tk.Label(window, text="Discord : Chicoch#7678", font=("Arial", "8", "bold"), fg="grey")
contact_label.pack()
contact_label.place(x=400, y=760)
github_label = tk.Label(window, text="https://github.com/Nv3l", font=("Arial", "8", "bold"), fg="grey")
github_label.pack()
github_label.place(x=400, y=780)


# Print a message to the user to not close the window
print("/!\ Do not close this window ! /!\\ \n\n")

# Start the main loop
window.mainloop()
