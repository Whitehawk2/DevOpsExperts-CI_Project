"""
    this module combines both the frontend and backend testing
    into one.
    
    uses arbitrary selenium chrome driver path, address, uid and usernames.
"""
from random import randint as rr
import requests
import backend_testing as bt
import frontend_testing as ft

CH_PATH = r'/snap/bin/chromium.chromedriver'
FRFX_PATH = r'/home/whitehawk/PycharmProjects/scratch/geckodriver'
TEST_USER_ID = rr(31, 50)


def fail():
    """
    shorthand to raise exception
    """
    raise Exception("test failed")


def cleanup_api(path: str):
    """
    Cleans the db by deleting selected row via rest_app delete method
    :param path: str, full path including uid, to send for deletion
    :raises exception if can't delete
    """
    res = requests.delete(path)
    if res.ok:
        print('Done! \nTable clean!')
    else:
        fail()
    

def main():
    """
    procedurally calls testing functions from both frontend and backend
    testing modules for a complete suite of testing.
    
    calls on cleanup at the end regardless of success or failure.
    
    Gets current test configurations randomly from db.
    
    :raises exception if testing fails at any point.
    """
    # get test configurations via bt.get_test_configurations
    THIS_TEST = bt.get_test_configuration()
    APP_PATH, USER_NAME, BROWSER = (THIS_TEST['Gateway'],
                                    THIS_TEST['User'],
                                    THIS_TEST['Browser'])
    full_path = APP_PATH + str(TEST_USER_ID)
    
    try:
        print(f"Testing with UID {TEST_USER_ID} as "
              f"{USER_NAME}...\n\nProgress:")
        # backend:
        bt.post_2_db_api(full_path, USER_NAME)
        bt.get_from_db_api(full_path, USER_NAME)
        bt.get_from_mysql(TEST_USER_ID, USER_NAME)
        print("\nAll backend tests successful!\nStarting frontend...\n")
        # frontend:
        print(f'->\tExpecting {USER_NAME} from web app...')
        if BROWSER == 'Chrome':
            shown_username = ft.frontend_query(CH_PATH, str(TEST_USER_ID))
        else:
            shown_username = ft.frontend_query(FRFX_PATH, str(TEST_USER_ID))
        
        if shown_username == USER_NAME:
            print('Checks out!\n\nFrontend tests completed successfully!')
        else:
            fail()
    
    finally:
        # regardless of success or failure, clean the db
        print("Making sure table is clean for next testing: ", end='')
        try:
            cleanup_api(full_path)
        except Exception as e:
            print(f'FAILED!\n Given reason: {e}\n'
                  f'Check db.users @ uid {TEST_USER_ID} might not be purged.')


if __name__ == '__main__':
    main()
