import time, calendar
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


#Gets girls name
def get_girl_name(month, day, count, driver):

    g_name_count_no = 0
    month_str = calendar.month_name[month]

    print(f'////{count} results for: {day} {month_str} (female name)////\n')

    while g_name_count_no < count:
    
        g_name_count_no += 1
        select_month = Select(driver.find_element(By.ID, 'month')) #Finds month input
        select_day = Select(driver.find_element(By.ID,'day')) #Finds day input

        select_month.select_by_value(str(month)) #Select DOB month
        select_day.select_by_value(str(day)) #Select DOB day

        girl_name_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form"]/input[4]'))) #Waits for browser until the button to be loaded
        girl_name_input.click() #Click the button

        # Gets names in Korean
        # ------------------------------------------------------
        p_g_first_name_kr = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]').text.strip()
        c_g_first_name_kr = driver.find_element(By.CLASS_NAME, 'gf').text.strip()
        f_g_first_name_kr = p_g_first_name_kr.replace(c_g_first_name_kr, '')

        p_g_last_name_kr = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]').text.strip()
        c_g_last_name_kr = driver.find_element(By.CLASS_NAME, 'fm').text.strip()
        f_g_last_name_kr = p_g_last_name_kr.replace(c_g_last_name_kr, '')
        # ------------------------------------------------------

        # Gets names in Japanese
        p_g_first_name_jp = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[2]/div[2]/div[2]').text.strip()
        c_g_first_name_jp = driver.find_element(By.CLASS_NAME, 'gf').text.strip()
        f_g_first_name_jp = p_g_first_name_jp.replace(c_g_first_name_jp, '')

        p_g_last_name_jp = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[2]/div[2]/div[1]').text.strip()
        c_g_last_name_jp = driver.find_element(By.CLASS_NAME, 'fm').text.strip()
        f_g_last_name_jp = p_g_last_name_jp.replace(c_g_last_name_jp, '')        
        # ------------------------------------------------------

        # Gets names in English
        p_g_first_name_en = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[4]/div[2]/div[2]').text.strip()
        c_g_first_name_en = driver.find_element(By.CLASS_NAME, 'gf').text.strip()
        f_g_first_name_en = p_g_first_name_en.replace(c_g_first_name_en, '')

        p_g_last_name_en = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[4]/div[2]/div[1]').text.strip()
        c_g_last_name_en = driver.find_element(By.CLASS_NAME, 'fm').text.strip()
        f_g_last_name_en = p_g_last_name_en.replace(c_g_last_name_en, '')     
        # ------------------------------------------------------

        #Prints results 

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

#Gets boys name
def get_boy_name(month, day, count, driver):

    b_name_count_no = 0
    month_str = calendar.month_name[month]

    print(f'////{count} results for: {day} {month_str} (male name)////\n')

    while b_name_count_no < count:
    
        b_name_count_no += 1
        select_month = Select(driver.find_element(By.ID, 'month')) #Finds month input
        select_day = Select(driver.find_element(By.ID,'day')) #Finds day input

        select_month.select_by_value(str(month)) #Select DOB month
        select_day.select_by_value(str(day)) #Select DOB day

        boy_name_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form"]/input[3]'))) #Waits for browser until the button to be loaded
        boy_name_input.click()

        # Gets names in Korean
        # ------------------------------------------------------
        p_b_first_name_kr = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]').text 
        c_b_first_name_kr = driver.find_element(By.CLASS_NAME, 'gm').text
        f_b_first_name_kr = p_b_first_name_kr.replace(c_b_first_name_kr, '')

        p_b_last_name_kr = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]').text
        c_b_last_name_kr = driver.find_element(By.CLASS_NAME, 'fm').text
        f_b_last_name_kr = p_b_last_name_kr.replace(c_b_last_name_kr, '')
        # ------------------------------------------------------

        # Gets names in Japanese
        p_b_first_name_jp = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[2]/div[2]/div[2]').text
        c_b_first_name_jp = driver.find_element(By.CLASS_NAME, 'gm').text
        f_b_first_name_jp = p_b_first_name_jp.replace(c_b_first_name_jp, '')

        p_b_last_name_jp = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[2]/div[2]/div[1]').text
        c_b_last_name_jp = driver.find_element(By.CLASS_NAME, 'fm').text
        f_b_last_name_jp = p_b_last_name_jp.replace(c_b_last_name_jp, '')        
        # ------------------------------------------------------

        # Gets names in English
        p_b_first_name_en = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[4]/div[2]/div[2]').text
        c_b_first_name_en = driver.find_element(By.CLASS_NAME, 'gm').text
        f_b_first_name_en = p_b_first_name_en.replace(c_b_first_name_en, '')

        p_b_last_name_en = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[4]/div[2]/div[1]').text
        c_b_last_name_en = driver.find_element(By.CLASS_NAME, 'fm').text
        f_b_last_name_en = p_b_last_name_en.replace(c_b_last_name_en, '')     
        # ------------------------------------------------------
        #Prints results 

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


# Define a headless Chrome browser and run functions
def main(month, day, count):

    opt = webdriver.ChromeOptions()
    opt.add_argument('headless') #Suppress the browser with headless

    driver = webdriver.Chrome('/Users/sean/Documents/DEV/chromedriver', options = opt) #Chrome driver location
    driver.implicitly_wait(3) #Waits 3 secs for loading web resources
    url = 'https://ko.enjoyjapan.co.kr/japanese_names_maker.php' #URL defined
    driver.get(url) #Gets the defined URL
    driver.maximize_window() #Maximize the window when open

    response = requests.get(url)
    status = response.status_code

    if status == 200:

        # Print success message if access is granted
        print('Access to the url is successful\n\n')

        # Get time of starting point
        t_start = time.time()

        # Call functions   
        get_girl_name(month, day, count, driver)
        get_boy_name(month, day, count, driver)
    
        # Get time of ending point
        t_end = time.time()

        # Get time taken
        t_taken = t_end - t_start
        elapsed_time = time.strftime('%H:%M:%S', time.gmtime(t_taken))

        # Print time taken for getting data
        print(f'Time taken to print results: {elapsed_time}')

    else:
        print('No connection')

main(4, 25, 10)