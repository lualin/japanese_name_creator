import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

opt = webdriver.ChromeOptions()
opt.add_argument('headless') #Suppress the browser with headless

driver = webdriver.Chrome('/Users/sean/Documents/DEV/chromedriver', options = opt) #Chrome driver location
driver.implicitly_wait(3) #Waits 3 secs for loading web resources
url = 'https://ko.enjoyjapan.co.kr/japanese_names_maker.php' #URL defined
driver.get(url) #Gets the defined URL
driver.maximize_window() #Maximize the window when open

#Gets girls name

def get_girl_name(month, day):

    g_name_count_no = 0

    print('Results for: {m}/{d}'.format(m=month, d=day))

    while g_name_count_no < 20:
    
        g_name_count_no += 1
        select_month = Select(driver.find_element(By.ID, 'month')) #Finds month input
        select_day = Select(driver.find_element(By.ID,'day')) #Finds day input

        select_month.select_by_value(str(month)) #Select DOB month
        select_day.select_by_value(str(day)) #Select DOB day

        girl_name_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form"]/input[4]'))) #Waits for browser until the button to be loaded
        girl_name_input.click() #Click the button

        # Gets names in Korean
        # ------------------------------------------------------
        p_g_first_name_kr = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]').text 
        c_g_first_name_kr = driver.find_element(By.CLASS_NAME, 'gf').text
        f_g_first_name_kr = p_g_first_name_kr.replace(c_g_first_name_kr, '')

        p_g_last_name_kr = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[1]/div[2]/div[1]').text
        c_g_last_name_kr = driver.find_element(By.CLASS_NAME, 'fm').text
        f_g_last_name_kr = p_g_last_name_kr.replace(c_g_last_name_kr, '')
        # ------------------------------------------------------

        # Gets names in Japanese
        p_g_first_name_jp = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[2]/div[2]/div[2]').text 
        c_g_first_name_jp = driver.find_element(By.CLASS_NAME, 'gf').text
        f_g_first_name_jp = p_g_first_name_jp.replace(c_g_first_name_jp, '')

        p_g_last_name_jp = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[2]/div[2]/div[1]').text
        c_g_last_name_jp = driver.find_element(By.CLASS_NAME, 'fm').text
        f_g_last_name_jp = p_g_last_name_jp.replace(c_g_last_name_jp, '')        
        # ------------------------------------------------------

        # Gets names in English
        p_g_first_name_en = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[4]/div[2]/div[2]').text 
        c_g_first_name_en = driver.find_element(By.CLASS_NAME, 'gf').text
        f_g_first_name_en = p_g_first_name_en.replace(c_g_first_name_en, '')

        p_g_last_name_en = driver.find_element(By.XPATH, '//*[@id="contents"]/div/div[1]/div[2]/div/div[4]/div[2]/div[1]').text
        c_g_last_name_en = driver.find_element(By.CLASS_NAME, 'fm').text
        f_g_last_name_en = p_g_last_name_en.replace(c_g_last_name_en, '')     
        # ------------------------------------------------------

        #Prints results 

        #print('Recommended name is:')
        print(g_name_count_no, '------------------')
        print('First Name: ', f_g_first_name_kr, f_g_first_name_jp, f_g_first_name_en ,end='')    
        print('Last Name: ', f_g_last_name_kr, f_g_last_name_jp, f_g_last_name_en)

#Gets boys name

def get_boy_name(month,day):

    b_name_count_no = 0

    print('Results for: {m}/{d}'.format(m=month, d=day))

    while b_name_count_no < 20:
    
        b_name_count_no += 1
        select_month = Select(driver.find_element(By.ID, 'month')) #Finds month input
        select_day = Select(driver.find_element(By.ID,'day')) #Finds day input

        select_month.select_by_value(str(month)) #Select DOB month
        select_day.select_by_value(str(day)) #Select DOB day

        boy_name_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form"]/input[3]'))) #Waits for browser until the button to be loaded
        boy_name_input.click() #Click the button

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
        print(b_name_count_no, '------------------')
        print('First Name: ', f_b_first_name_kr, f_b_first_name_jp, f_b_first_name_en, end='')    
        print('Last Name: ', f_b_last_name_kr, f_b_last_name_jp, f_b_last_name_en)

get_boy_name(4, 27)