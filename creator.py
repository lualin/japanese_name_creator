# Author: Lualin
# imports
import datetime
import time
import calendar
import requests
import inquirer
import re

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# Database import
import mariadb
from db import db

# ------------------------------------------------------ #

# Gets girls name
def get_girl_name(month, day, count, gender, driver, conn):

    g_name_count_no = 0
    month_str = calendar.month_name[month]

    print(f'////{count} results for: {day} {month_str} (female name)////\n')

    while g_name_count_no < count:

        g_name_count_no += 1
        select_month = Select(driver.find_element(
            By.ID, 'month'))  # Finds month input
        select_day = Select(driver.find_element(
            By.ID, 'day'))  # Finds day input

        select_month.select_by_value(str(month))  # Select DOB month
        select_day.select_by_value(str(day))  # Select DOB day

        girl_name_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="form"]/input[4]')))  # Waits for browser until the button to be loaded
        girl_name_input.click()  # Click the button

        # Gets names in Korean
        # ------------------------------------------------------
        p_g_first_name_kr = driver.find_element(
            By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]').text.strip()
        c_g_first_name_kr = driver.find_element(
            By.CLASS_NAME, 'gf').text.strip()
        f_g_first_name_kr = p_g_first_name_kr.replace(c_g_first_name_kr, '')

        p_g_last_name_kr = driver.find_element(
            By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]').text.strip()
        c_g_last_name_kr = driver.find_element(
            By.CLASS_NAME, 'fm').text.strip()
        f_g_last_name_kr = p_g_last_name_kr.replace(c_g_last_name_kr, '')
        # ------------------------------------------------------

        # Gets names in Japanese
        p_g_first_name_jp = driver.find_element(
            By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[2]/div[2]/div[2]').text.strip()
        c_g_first_name_jp = driver.find_element(
            By.CLASS_NAME, 'gf').text.strip()
        f_g_first_name_jp = p_g_first_name_jp.replace(c_g_first_name_jp, '')

        p_g_last_name_jp = driver.find_element(
            By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[2]/div[2]/div[1]').text.strip()
        c_g_last_name_jp = driver.find_element(
            By.CLASS_NAME, 'fm').text.strip()
        f_g_last_name_jp = p_g_last_name_jp.replace(c_g_last_name_jp, '')
        # ------------------------------------------------------

        # Gets names in English
        p_g_first_name_en = driver.find_element(
            By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[4]/div[2]/div[2]').text.strip()
        c_g_first_name_en = driver.find_element(
            By.CLASS_NAME, 'gf').text.strip()
        f_g_first_name_en = p_g_first_name_en.replace(c_g_first_name_en, '')

        p_g_last_name_en = driver.find_element(
            By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[4]/div[2]/div[1]').text.strip()
        c_g_last_name_en = driver.find_element(
            By.CLASS_NAME, 'fm').text.strip()
        f_g_last_name_en = p_g_last_name_en.replace(c_g_last_name_en, '')
        # ------------------------------------------------------

        # Prints results

        #print('Recommended name is:')
        print(f'---<<{g_name_count_no}>>---\n')
        #print(f'JP: \n{f_g_first_name_jp}{f_g_last_name_jp}\nKR: {f_g_first_name_kr}{f_g_last_name_kr}\nEN: {f_g_first_name_en}{f_g_last_name_en}')
        print(
            f' -Japanese-',
            f'\n名前: {f_g_first_name_jp}名字: {f_g_last_name_jp}\n',
            f'-Korean-',
            f'\n이름: {f_g_first_name_kr}성: {f_g_last_name_kr}\n',
            f'-English-'
            f'\nFirst Name: {f_g_first_name_en}Last Name: {f_g_last_name_en}'
        )

        # Database functions call
        try:
            # Get cursor
            cur = conn.cursor()

            # Get the latest transaction number
            # If there are no transactions yet, start with 1
            # Otherwise, generate a new transaction number
            cur.execute(
                "SELECT TRANS_NO FROM transaction ORDER BY TRANS_NO DESC LIMIT 1")
            latest_transaction = cur.fetchone()  # Retrieve the latest transaction number
            if latest_transaction is None:
                transaction_no = 10000  # If there are no transactions yet, start with 1
            else:
                transaction_no = latest_transaction[0] + 1  # Generate a new transaction number

            # Insert transaction into DB
            cur.execute(
                "INSERT INTO transaction (TRANS_NO, DATE_CREATED, TIME_CREATED, GENDER, MONTH, DAY) VALUES (?, ?, ?, ?, ?, ?)",
                (transaction_no, datetime.datetime.now().date(), datetime.datetime.now().time(), gender, month, day))

            # get the generated transaction_id
            transaction_id = cur.lastrowid

            # Use the transaction_id as a foreign key in en_names table
            cur.execute("INSERT INTO en_names (transaction_id, first_name, last_name) VALUES (?, ?, ?)",
                        (transaction_id, f_g_first_name_en, f_g_last_name_en))

            # Use the transaction_id as a foreign key in jp_names table
            cur.execute("INSERT INTO jp_names (transaction_id, first_name, last_name) VALUES (?, ?, ?)",
                        (transaction_id, f_g_first_name_jp, f_g_last_name_jp))

            # Use the transaction_id as a foreign key in kr_names table
            cur.execute("INSERT INTO kr_names (transaction_id, first_name, last_name) VALUES (?, ?, ?)",
                        (transaction_id, f_g_first_name_kr, f_g_last_name_kr))

            # Print success message
            print('Data successfully inserted')

            # commit the changes to the database
            conn.commit()

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        except Exception as ex:
            print(f'Error incurring while executing SQL statement: ({ex})')


# Gets boys name
def get_boy_name(month, day, count, gender, driver):

    b_name_count_no = 0
    month_str = calendar.month_name[month]

    print(f'////{count} results for: {day} {month_str} (male name)////\n')

    while b_name_count_no < count:

        b_name_count_no += 1
        select_month = Select(driver.find_element(
            By.ID, 'month'))  # Finds month input
        select_day = Select(driver.find_element(
            By.ID, 'day'))  # Finds day input

        select_month.select_by_value(str(month))  # Select DOB month
        select_day.select_by_value(str(day))  # Select DOB day

        boy_name_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="form"]/input[3]')))  # Waits for browser until the button to be loaded
        boy_name_input.click()

        # Gets names in Korean
        # ------------------------------------------------------
        p_b_first_name_kr = driver.find_element(
            By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]').text
        c_b_first_name_kr = driver.find_element(By.CLASS_NAME, 'gm').text
        f_b_first_name_kr = p_b_first_name_kr.replace(c_b_first_name_kr, '')

        p_b_last_name_kr = driver.find_element(
            By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]').text
        c_b_last_name_kr = driver.find_element(By.CLASS_NAME, 'fm').text
        f_b_last_name_kr = p_b_last_name_kr.replace(c_b_last_name_kr, '')
        # ------------------------------------------------------

        # Gets names in Japanese
        p_b_first_name_jp = driver.find_element(
            By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[2]/div[2]/div[2]').text
        c_b_first_name_jp = driver.find_element(By.CLASS_NAME, 'gm').text
        f_b_first_name_jp = p_b_first_name_jp.replace(c_b_first_name_jp, '')

        p_b_last_name_jp = driver.find_element(
            By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[2]/div[2]/div[1]').text
        c_b_last_name_jp = driver.find_element(By.CLASS_NAME, 'fm').text
        f_b_last_name_jp = p_b_last_name_jp.replace(c_b_last_name_jp, '')
        # ------------------------------------------------------

        # Gets names in English
        p_b_first_name_en = driver.find_element(
            By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[4]/div[2]/div[2]').text
        c_b_first_name_en = driver.find_element(By.CLASS_NAME, 'gm').text
        f_b_first_name_en = p_b_first_name_en.replace(c_b_first_name_en, '')

        p_b_last_name_en = driver.find_element(
            By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[4]/div[2]/div[1]').text
        c_b_last_name_en = driver.find_element(By.CLASS_NAME, 'fm').text
        f_b_last_name_en = p_b_last_name_en.replace(c_b_last_name_en, '')
        # ------------------------------------------------------
        # Prints results

        #print('Recommended name is:')
        print(f'---<<{b_name_count_no}>>---\n')
        print(
            f' -Japanese-',
            f'\n名前: {f_b_first_name_jp}名字: {f_b_last_name_jp}\n',
            f'-Korean-',
            f'\n이름: {f_b_first_name_kr}성: {f_b_last_name_kr}\n',
            f'-English-'
            f'\nFirst Name: {f_b_first_name_en}Last Name: {f_b_last_name_en}'
        )

        # Database functions call
        try:
            # Get cursor
            cur = conn.cursor()

            # Get the latest transaction number
            # If there are no transactions yet, start with 1
            # Otherwise, generate a new transaction number
            cur.execute(
                "SELECT TRANS_NO FROM transaction ORDER BY TRANS_NO DESC LIMIT 1")
            latest_transaction = cur.fetchone()  # Retrieve the latest transaction number
            if latest_transaction is None:
                transaction_no = 10000  # If there are no transactions yet, start with 1
            else:
                transaction_no = latest_transaction[0] + 1  # Generate a new transaction number

            # Insert transaction into DB
            cur.execute(
                "INSERT INTO transaction (TRANS_NO, DATE_CREATED, TIME_CREATED, GENDER, MONTH, DAY) VALUES (?, ?, ?, ?, ?, ?)",
                (transaction_no, datetime.datetime.now().date(), datetime.datetime.now().time(), gender, month, day))

            # get the generated transaction_id
            transaction_id = cur.lastrowid

            # Use the transaction_id as a foreign key in en_names table
            cur.execute("INSERT INTO en_names (transaction_id, first_name, last_name) VALUES (?, ?, ?)",
                        (transaction_id, f_b_first_name_en, f_b_last_name_en))

            # Use the transaction_id as a foreign key in jp_names table
            cur.execute("INSERT INTO jp_names (transaction_id, first_name, last_name) VALUES (?, ?, ?)",
                        (transaction_id, f_b_first_name_jp, f_b_last_name_jp))

            # Use the transaction_id as a foreign key in kr_names table
            cur.execute("INSERT INTO kr_names (transaction_id, first_name, last_name) VALUES (?, ?, ?)",
                        (transaction_id, f_b_first_name_kr, f_b_last_name_kr))

            # Print success message
            print('Data successfully inserted')

            # commit the changes to the database
            conn.commit()

        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        except Exception as ex:
            print(f'Error incurring while executing SQL statement: ({ex})')


# Define a headless Chrome browser and run functions

def main(month, day, count, gender):

    # Chrome options setup
    opt = webdriver.ChromeOptions()
    opt.add_argument('headless')  # Suppress the browser with headless

    # Chrome driver setup
    driver = webdriver.Chrome(
        '/Users/sean/Documents/DEV/chromedriver', options=opt)
    driver.implicitly_wait(3)  # Waits 3 secs for loading web resources
    url = 'https://ko.enjoyjapan.co.kr/japanese_names_maker.php'  # URL defined
    driver.get(url)  # Gets the defined URL
    driver.maximize_window()  # Maximize the window when open

    # Check connection
    response = requests.get(url)
    status = response.status_code

    # Get user input and convert to int
    month_int = month['month']
    day_int = day['day']
    gender_str = gender['gender']

    # Check connection status code and proceed if 200
    if status == 200:

        # Print success message if access is granted
        print('------------------------------------\n')
        print(f'Access status code: {status}\n')
        print(f'Access to the {url} is successful\n')

        # Get time of starting point
        t_start = time.time()

        # Check month range
        if month_int < 1 or month_int > 12:
            print('Month is out of range')
            return
        
        # Connect to database
        conn = db.connect()
        print('Connected to database')

        # Check gender and run corresponding functions
        if gender_str == 'M':
            try:
                get_boy_name(month_int, day_int, count, gender_str, driver, conn)

            # If there is an error, print error message
            except:
                print('Error: Please try again')
        else:
            try:           
                get_girl_name(month_int, day_int, count, gender_str, driver, conn)

            # If there is an error, print error message
            except:
                print('Error: Please try again')
            

        # Get time of ending point
        t_end = time.time()

        # Get time taken
        t_taken = t_end - t_start
        elapsed_time = time.strftime('%H:%M:%S', time.gmtime(t_taken))

        # Print time taken for getting data
        print(f'Time taken to print results: {elapsed_time}')

        # Close database connection
        conn.close()
        print('Database connection closed')

    # Print error message if access is denied
    else:
        print('No connection')

# Main function call

if __name__ == '__main__':

    # Input and questions config
    count = int(input('Enter the number of results: '))
    month_questions = [
        inquirer.List('month',
                      message="Select the month of birth: ",
                      choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                      ),
    ]
    day_questions = [
        inquirer.List('day',
                      message="Select the day of birth: ",
                      choices=[i for i in range(1, 32)],
                      ),
    ]
    gender_questions = [
        inquirer.List('gender',
                      message="Select your gender: ",
                      choices=['M', 'F'],
                      ),
    ]

    # Get user input
    month = inquirer.prompt(month_questions)
    day = inquirer.prompt(day_questions)
    gender = inquirer.prompt(gender_questions)

    # Try to connect to database and run main function
    try:
        # Call main function
        main(month, day, count, gender)

    except TypeError as type_err: # Catch type error
        print(f'Invalid type {type_err=}, {type(type_err)=}')
    except ValueError: # Catch value error
        print("Could not convert data to an integer.")
    except Exception as err: # Catch other errors
        print(f"Unexpected {err=}, {type(err)=}")
        raise
