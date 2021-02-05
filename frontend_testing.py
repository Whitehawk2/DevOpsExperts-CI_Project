"""
this module is made to test the frontend part - web_app.py

if called by main(), uses hardcoded selenium driver (expects Chrome)
and USER_ID (random 1-3).
"""

from selenium import webdriver
from selenium.common.exceptions import WebDriverException as WdE
from selenium.webdriver.chrome.options import Options as ch_Options
from selenium.webdriver.firefox.options import Options as frfx_Options
from random import randint as rr

PATH = r'/snap/bin/chromium.chromedriver'
APP_PATH = r'http://127.0.0.1:5001/users/get_user_data/'
USER = str(rr(1, 3))


def frontend_query(exec_path, id_num):
    """
    Queries the web app fronend by using headless chrome selenium session
    to browse to the web app address with specified user id,
    then uses selenium selector to check username was returned,
    and prints it.
    
    since it supports both Firefox and Chrome,
    has a nested function for shared logic.
    
    if the locator does not have 'user', fails the test.
    :param exec_path: str, chrome webdriver exec path
    :param id_num: int, the user_id to request user name by
    :return: response user name if id exists, else raises Exception
    """
    def shared_logic():
        """
        shared logic part of both firefox and chrome selenium webdrivers
        """
        driver.implicitly_wait(5)
        driver.get(f'{APP_PATH}{id_num}')
        q_element = driver.find_elements_by_id("user")
        if len(q_element) > 0:
            result = q_element[0].text
            print(f'->\tResponse: got {result} from web app interface.')
            return result
        else:
            raise Exception("test failed")
        
    if 'gecko' in exec_path:
        try:
            print('<Using Firefox>')
            options = frfx_Options()
            options.add_argument('-headless')
            with webdriver.Firefox(executable_path=exec_path,
                                   options=options) as driver:
                return shared_logic()
            
        except WdE as err:
            print(err)
    else:
        try:
            print('<Using Chrome>')
            options = ch_Options()
            options.headless = True
            with webdriver.Chrome(executable_path=exec_path,
                                  options=options) as driver:
    
                return shared_logic()
        
        except WdE as err:
            print(err)
    

def main():
    """
    Main driver for the test.
    Calls the testing function with arbitrary test args
    (Chrome)
    """
    frontend_query(PATH, USER)
    
    
if __name__ == '__main__':
    main()
