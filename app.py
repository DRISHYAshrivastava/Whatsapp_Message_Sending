import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from webdriver_manager.core.os_manager import ChromeType


# Streamlit UI
st.title("WhatsApp Bulk Message Sender")
numbers_input = st.text_area("Enter phone numbers (separated by spaces):")
message_input = st.text_area("Enter your message:")
st.warning("Please ensure you are using the Chrome browser.")
st.warning("Please keep your phone with you and ensure it's connected to the internet.")
send_button = st.button("Send")

# Configurations
login_time = 30
new_msg_time = 5
send_msg_time = 5
country_code = 91
action_time = 2

if send_button:
    if numbers_input and message_input:
        numbers_list = numbers_input.split()
        @st.cache_resource
        def get_driver():
            return webdriver.Chrome(
                service=Service(
                    ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
                ),
                options=options,
            )
        option=options()
        options.add_argument("--headless=new")
        options.add_argument('--disable-gpu')
        
        driver=get_driver()
        #Open WhatsApp Web
        link = 'https://web.whatsapp.com'
        driver.get(link)
        st.write("Please scan the QR code through your WhatsApp app to log in to WhatsApp Web. You will get 30 seconds to login.")
        time.sleep(login_time)

        for num in numbers_list:
            num = num.strip()
            phone_link = f'https://web.whatsapp.com/send/?phone={country_code}{num}'
            driver.get(phone_link)
            time.sleep(new_msg_time)

            # Prepare the message
            actions = ActionChains(driver)
            for line in message_input.split('\n'):
                actions.send_keys(line)
                actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            time.sleep(send_msg_time)

        driver.quit()
        st.success("Messages sent successfully!")
    else:
        st.error("Please enter both phone numbers and a message.")
