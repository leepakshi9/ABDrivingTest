#https://scheduler.itialb4dmv.com/schAlberta
from selenium.common.exceptions import NoSuchElementException
import time
from argparse import ArgumentParser


def sendEmail(messg,args):
    import smtplib
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Next, log in to the server
    server.login(args.username, args.password)

    # Send the mail
    msg = messg+",check for spots!"
    server.sendmail(args.username, args.recipient, msg)

def real_task(args):
    from selenium import webdriver
    # Using Chrome to access web
    driver = webdriver.Chrome(executable_path=args.driverPath+'/chromedriver')
    # Open the website
    driver.get('https://scheduler.itialb4dmv.com/schAlberta')

    # Select the id box
    book_appt = driver.find_element_by_id('btnBookAppt')
    book_appt.click()

    buy_test = driver.find_element_by_id('invalidPermit')
    buy_test.click()

    fname = driver.find_element_by_id('FirstName')
    fname.send_keys(args.firstName)

    lname = driver.find_element_by_id('LastName')
    lname.send_keys(args.lastName)

    lname = driver.find_element_by_id('MVID')
    lname.send_keys(args.mvid)

    lname = driver.find_element_by_id('Birthdate')
    lname.send_keys(args.birthdate)

    lname = driver.find_element_by_id('Email')
    lname.send_keys(args.email)

    #checkbox
    for i in range(5):
        try:
            result = driver.find_element_by_id("isTermsAccepted").is_selected()
            if result:
                print('Checkbox already selected')
            else:
                element = driver.find_element_by_id('isTermsAccepted')
                driver.execute_script("arguments[0].click();", element)
                print('Checkbox selected')
                break

        except NoSuchElementException as e:
            print('retry in 1s.')
            time.sleep(1)
        else:
            raise e

    time.sleep(2)
    #formSubmit
    next1 = driver.find_element_by_id('formSubmit')
    # Click login
    next1.click()

    time.sleep(2)
    from selenium.webdriver.support.ui import Select

    select = Select(driver.find_element_by_id('serviceGroupList'))

    # Change type of test here
    select.select_by_visible_text('Class 5 Basic Road Test')

    time.sleep(2)
    #isTermsAccepted
    #checkbox
    for i in range(5):
        try:
            result = driver.find_element_by_id("isTermsAccepted").is_selected()
            if result:
                print('Checkbox already selected')
            else:
                element = driver.find_element_by_id('isTermsAccepted')
                driver.execute_script("arguments[0].click();", element)
                print('Checkbox selected')
                break
        except NoSuchElementException as e:
            print('retry in 1s.')
            time.sleep(1)
        else:
            raise e

    #acceptTerms
    driver.find_element_by_id('acceptTerms').click()

    #cityNameSearch
    city = driver.find_element_by_id('cityNameSearch')
    city.send_keys(args.city)

    #citySearchRadius
    select = Select(driver.find_element_by_id('citySearchRadius'))

    select.select_by_value('50')

    #searchSelectedLocation
    driver.find_element_by_id('searchSelectedLocation').click()

    time.sleep(6)
    try:
        message=driver.find_element_by_class_name('text-danger').text
        print(message)
        sendEmail("not found",args)
    except:
        print("found a spot")
        sendEmail("found",args)
def get_args():
    '''
    Parses input arguments and calls the appropriate function
    :return: None
    '''
    parser = ArgumentParser(prog='driving_test.py', add_help=False)

    parser.add_argument('-P', '--driverPath', dest='driverPath',
                        help='path of the chromedriver.exe file')
    parser.add_argument('-u', '--username', dest='username',
                        help='username for email client')
    parser.add_argument('-p', '--password', dest='password',
                        help='password for email client')
    parser.add_argument('-r', '--recipient', dest='recipient',
                        help='email recipient')
    parser.add_argument('-f', '--firstName', dest='firstName',
                        help='your firstName')
    parser.add_argument('-l', '--lastName', dest='lastName',
                        help='your lastName')
    parser.add_argument('-m', '--mvid', dest='mvid',
                        help='mvid of the user (string in yyyy/mm/dd format)')
    parser.add_argument('-b', '--birthdate', dest='birthdate',
                        help='birthdate as on application')
    parser.add_argument('-e', '--email', dest='email',
                        help='email as on application')
    parser.add_argument('-c', '--city', dest='city',
                        help='city for driving test')

    args = parser.parse_args()

    return args

def main():
    try:
        real_task(get_args())
        print("done task")
        exit(0)
    except Exception as e:
        print(e)
        exit(100)

main()