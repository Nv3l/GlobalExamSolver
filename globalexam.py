import tkinter as tk
from time import sleep
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
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
def solve_next_exercice(driver, delay, subdomain, delayExercice):

    # Go to exercices page
    driver.get("https://"+subdomain+".global-exam.com/library/study-sheets/categories/grammar")
    
    sleep(delay)

    # Find all the exercice button
    allButtonsExercice = driver.find_elements(By.XPATH, "//button[contains(@class,'button-solid-default-small')]")

    # Get the content of all the buttons
    allButtonsExerciceContent = [button.text for button in allButtonsExercice]

    # Count the number of "Relancer" between two or more "Me tester"
    # stepExercice = sum(1 for i, item in enumerate(allButtonsExerciceContent) if (item == "Relancer" and allButtonsExerciceContent[i - 1] == "Me tester" if i > 0 else False))

    first_me_tester_index = None
    last_me_tester_index = None

    for i, item in enumerate(allButtonsExerciceContent):
        if item == "Me tester":
            if first_me_tester_index is None:
                first_me_tester_index = i
            last_me_tester_index = i

    # Count "Relancer" between the first and last "Me tester"
    stepExercice = 0
    if first_me_tester_index is not None and last_me_tester_index is not None:
        for i in range(first_me_tester_index, last_me_tester_index + 1):
            if allButtonsExerciceContent[i] == "Relancer":
                stepExercice += 1

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
    clickOnLastButton = buttonsExercices[-1+invert_number(stepExercice)].click()
    
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
window.geometry("1200x620")

# ==== Add a solve for exercice tab ====

# Add title
title_label = tk.Label(window, text="Solve every exercice possible on GlobalExam !", font=("Arial", "12", "bold"))
title_label.pack()
title_label.place(x=350, y=20)

# Add prompt for the user and the password
username_label = tk.Label(window, text="Username:")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()
password_label = tk.Label(window, text="Password:")
password_label.pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()
username_label.place(x=100, y=50)
username_entry.place(x=100, y=80)
password_label.place(x=100, y=110)
password_entry.place(x=100, y=140)


# Add choice for web breowser
browser_label = tk.Label(window, text="Web Browser (default Firefox) :")
browser_label.pack()
browser_list = tk.Listbox(window, height=1)

# Add element for the list
browser_list.insert(0, "Firefox")
# browser_list.insert(1, "Chrome")

# Select default web browser
browser_list.selection_set(0,0)

browser_list.pack()
browser_label.place(x=100, y=200)
browser_list.place(x=100, y=230)


# Add prompt for a delay with default value
delay_label = tk.Label(window, text="Add a general delay (default 3) \n For slow connection use 5 :")
delay_label.pack()
delay_entry = tk.Entry(window)
delay_entry.insert(0, "3")  # Set default value
delay_entry.pack()
delay_label.place(x=350, y=50)
delay_entry.place(x=350, y=80)

# Create the subdomain label and entry
subdomain_label = tk.Label(window, text="Solve exercice for the selected subdomain (exam, general):")
subdomain_label.pack()
subdomain_entry = tk.Entry(window)
subdomain_entry.insert(0, "exam")  # Set default value
subdomain_entry.pack()
subdomain_label.place(x=350, y=140)
subdomain_entry.place(x=350, y=170)

# # Create a input for the step of the exercice
# stepExercice_label = tk.Label(window, text="If you already solve some exercice at the bottom of the page \n You must add a step to skip this exercice (default 0) :")
# stepExercice_label.pack()
# stepExercice_entry = tk.Entry(window)
# stepExercice_entry.insert(0, "0")  # Set default value
# stepExercice_entry.pack()
# stepExercice_label.place(x=350, y=230)
# stepExercice_entry.place(x=350, y=260)

# Add delay to resolve the exercice
delayExercice_label = tk.Label(window, text="Add a delay in seconde to resolve exercice (default 0) :")
delayExercice_label.pack()
delayExercice_entry = tk.Entry(window)
delayExercice_entry.insert(0, "0")  # Set default value
delayExercice_entry.pack()
delayExercice_label.place(x=350, y=320)
delayExercice_entry.place(x=350, y=350)

def on_solve_next_exercice():
    subdomain = subdomain_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    delay = int(delay_entry.get())
    # stepExercice = invert_number(int(stepExercice_entry.get()))
    delayExercice = int(delayExercice_entry.get())

    # See wich browser the user choose
    browser = browser_list.curselection()

    if browser == ():
        # Show a alert box to the user to select a browser
        # Show this alert with red border
        Errorwindow = tk.Tk()
        Errorwindow.geometry("250x100")
        Errorwindow.title("Error - GlobalExam Solver")
        Errorwindow.configure(bg="red")


        Errorwindows = tk.Label(Errorwindow, text="Please select a browser", font=("Arial", "12", "bold"), fg="white", bg="red")
        Errorwindows.pack()
        Errorwindows.place(x=20, y=40)

        ready = False

    # Chrome browser
    elif browser == "(1,)":
        # Download Chrome driver
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument(argument='log-level=3')

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(latest_release_url="https://chromedriver.storage.googleapis.com/765286099.0.4844.51/").install()), options=chromeOptions)

        ready = True

    # Firefox browser
    else:
        # Download Firefox driver
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        ready = True

    # Print a message to the user to not close the window
    print("/!\ Do not close this window ! /!\\ \n\n")

    if ready == True:
        # Initiliaze the driver and login to the global exam website
        init_globalexam(driver, delay)
        login_globalexam(driver, delay, username, password)

        # Loop to solve every exercice
        while True:
            solve_next_exercice(driver, delay, subdomain, delayExercice)

# Create the solve next exercice button
solve_next_exercice_button = tk.Button(window, text="Solve exercice", command=on_solve_next_exercice)
solve_next_exercice_button.pack()
solve_next_exercice_button.place(x=350, y=410)


## ==== Add a selected re-solve exercice button ====

# Add title
title_label = tk.Label(window, text="Solve a selected exercice \n (you must count the line of the exercice)", font=("Arial", "12", "bold"))
title_label.pack()
title_label.place(x=750, y=10)

# Add prompt for a delay with default value
selected_delay_label = tk.Label(window, text="Add a general delay (default 3) \n For slow connection use 5 :")
selected_delay_label.pack()
selected_delay_entry = tk.Entry(window)
selected_delay_entry.insert(0, "3")  # Set default value
selected_delay_entry.pack()
selected_delay_label.place(x=750, y=50)
selected_delay_entry.place(x=750, y=80)

# Create the subdomain label and entry
selected_subdomain_label = tk.Label(window, text="Solve exercice for the selected subdomain (exam, general):")
selected_subdomain_label.pack()
selected_subdomain_entry = tk.Entry(window)
selected_subdomain_entry.insert(0, "exam")  # Set default value
selected_subdomain_entry.pack()
selected_subdomain_label.place(x=750, y=140)
selected_subdomain_entry.place(x=750, y=170)

# Create a input for the number of the exercice
selected_number_exercice_label = tk.Label(window, text="Enter the selected number of the exercice to solve :")
selected_number_exercice_label.pack()
selected_exercice_number_entry = tk.Entry(window)
selected_exercice_number_entry.insert(0, "0")  # Set default value
selected_exercice_number_entry.pack()
selected_number_exercice_label.place(x=750, y=230)
selected_exercice_number_entry.place(x=750, y=260)

# Add delay to resolve the exercice
selected_delayExercice_label = tk.Label(window, text="Add a delay in seconde to resolve selected exercice (default 0) :")
selected_delayExercice_label.pack()
selected_delayExercice_entry = tk.Entry(window)
selected_delayExercice_entry.insert(0, "0")  # Set default value
selected_delayExercice_entry.pack()
selected_delayExercice_label.place(x=750, y=320)
selected_delayExercice_entry.place(x=750, y=350)


def on_selected_re_solve_exercice():
    subdomain = selected_subdomain_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    delay = int(selected_delay_entry.get())
    exerciceNumber = int(selected_exercice_number_entry.get())
    delayExercice = int(selected_delayExercice_entry.get())

    # See wich browser the user choose
    browser = browser_list.curselection()

    if browser == ():
        # Show a alert box to the user to select a browser
        # Show this alert with red border
        Errorwindow = tk.Tk()
        Errorwindow.geometry("250x100")
        Errorwindow.title("Error - GlobalExam Solver")
        Errorwindow.configure(bg="red")


        Errorwindows = tk.Label(Errorwindow, text="Please select a browser", font=("Arial", "12", "bold"), fg="white", bg="red")
        Errorwindows.pack()
        Errorwindows.place(x=20, y=40)

        ready = False

    # Chrome browser
    elif browser == tuple((1,)):
        # Download Chrome driver
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument(argument='log-level=3')
        # from webdriver_manager.core.utils import ChromeType

        # driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM, version="114.0.5735.90").install(), options=chromeOptions)

        ready = True

    # Firefox browser
    else:
        # Download Firefox driver
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        ready = True

    # Print a message to the user to not close the window
    print("/!\ Do not close this window ! /!\\ \n\n")

    if ready == True:
        # Initiliaze the driver and login to the global exam website
        init_globalexam(driver, delay)
        login_globalexam(driver, delay, username, password)

        # Solve the selected exercice
        selected_re_solve_exercice(driver, delay, exerciceNumber, subdomain, delayExercice)

        driver.quit()

# Create the solve next exercice button
solve_next_exercice_button = tk.Button(window, text="Solve selected exercice", command=on_selected_re_solve_exercice)
solve_next_exercice_button.pack()
solve_next_exercice_button.place(x=750, y=410)


# add a quit button
quit_button = tk.Button(window, text="Exit", command=window.quit)
quit_button.pack()
quit_button.place(x=600, y=500)

# Place credit for the developer
credit_label = tk.Label(window, text="Developed by Nv3l", font=("Arial", "8", "bold"), fg="grey")
credit_label.pack()
credit_label.place(x=550, y=540)
contact_label = tk.Label(window, text="Discord : Chicoch#7678", font=("Arial", "8", "bold"), fg="grey")
contact_label.pack()
contact_label.place(x=550, y=560)
github_label = tk.Label(window, text="https://github.com/Nv3l", font=("Arial", "8", "bold"), fg="grey")
github_label.pack()
github_label.place(x=550, y=580)


# Print a message to the user to not close the window
print("/!\ Do not close this window ! /!\\ \n\n")

# Start the main loop
window.mainloop()



