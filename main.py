# Term is live currency exchange. Site = https://www.smartcurrencyexchange.com/live-exchange-rates/
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, math
from datetime import datetime as dt
import matplotlib.pyplot as plt
import smtplib
import json
from email import message
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage

service = Service('/Users/dominicpakenham/Downloads/chromedriver 2')

def get_driver():
# We create an empty variable and then populate it with various specifications before getting browser information.
    options = webdriver.ChromeOptions()
    options.add_argument('disable-infobars')
    options.add_argument('start-maximized')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('no-sandbox')
    options.add_argument('headless')
    # The experimental options below help avoid detection from the web browser.
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('disable_blink_features=AutomationControlled')
# options is a positional argument, so we have to assign it below.
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://www.smartcurrencyexchange.com/live-exchange-rates/')
    return driver


def send_email(user_email):

    from_email = <EMAIL>
    from_password = <PASSWORD>
    to_email = user_email
    subject = 'Hong Kong Dollar versus Pound Sterling: live rates'
    content = 'Please see attachments for the relevant data.'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    body = MIMEText(content, 'plain')
    msg.attach(body)

    filename = 'final_data.txt'
    with open(filename, 'r') as f:
        attachment = MIMEApplication(f.read(), Name=basename(filename))
        attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))

    filename_two = 'exchange_plotchart.png'
    with open(filename_two, 'rb') as fp:
        img = MIMEImage(fp.read())
        fp.close()

    msg.attach(attachment)
    msg.attach(img)

    server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(from_email, from_password)
    server.send_message(msg, from_addr=from_email, to_addrs=[to_email])
    return True


def main():
    print('''
    The following program will scrape the live exchange rate for Hong Kong dollars against British Pounds at roughly eight-second intervals
    over a period of your choosing. It will then send an email to your desired address with two attachments - a text file detailing the exchange rate
    over the relevant period and a plot-line graph representing the same information visually.''')
    time.sleep(5)
    user_email = input('Please enter an email address to receive the pertinent data.')
    time_period = input('''Enter a number to specify how many real-time data points you would like the program to obtain.
                                Make sure it is a valid number.''')

    while not time_period.isnumeric():
        time_period = input('''Enter a number to specify for how many real-time data points you would like the program to obtain.
                                        Make sure it is a valid number.''')
    time_period = (int(time_period))



    data_list = []
    time_list = []
    #format_data = '%Y-%m-%d %H:%M:%S'
    list_data = []
    driver = get_driver()
    time.sleep(4)

# I make the below dynamic by asking the user to specify a value.
    while len(list_data) < time_period:

    # The xpath finds the relevant html element exactly within the pertinent webpage.
        data_point = driver.find_element(By.XPATH, value="/html/body/div[1]/div/div/article/div/div[2]/div/div/div/div/div[1]/div/div/div/div/table/tbody[8]/tr/td[2]/span[1]")
        time.sleep(4)
        current_time = dt.now()

    # I want to convert the time nodes into date time objects, which I can then send to the relevant email address.
    # I save the string date to feed into my json dump later in the script.
        string_date = dt.strftime(current_time, '%Y-%m-%d')
        string_time = dt.strftime(current_time, '%Y-%m-%d %H:%M:%S')
        dt_object = dt.strptime(string_time, '%Y-%m-%d %H:%M:%S')


        data_list.append(float(data_point.text))
        time_list.append(dt_object)


        time.sleep(2)
    # Below I combine my time values with the corresponding data-values for the exchange rate.
        list_data = list(zip(time_list, data_list))
        time.sleep(2)

# We want to add the values to two lists, then convert into a dictionary using a dict comprehension. Then we can
# transfer to a new .txt file each time, so that each .txt file contains only the newest values.


    with open('final_data.txt', 'w') as final_data:
        final_data.write(json.dumps(list_data, default = str, sort_keys=True, indent=4))


# Below I capture the relevant information in a plot graph to be sent to the user along with our list of lists
# containing the exact time against currency values for each point on the graph.
    plt.style.use('seaborn')
    plt.plot_date(time_list, data_list, linestyle = 'solid')
    plt.title(f"HKD against Pound Sterling for {string_date}")
    plt.xlabel('Time in seconds')
    # The datetime object is being perceived as four items hence issue with shape in plot.
    plt.ylabel('Exchange Rate')
    plt.tight_layout
    plt.savefig('exchange_plotchart.png')

    #plt.show(block=True)

    email_action = send_email(user_email)




if __name__ == '__main__':
    main()


