import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import time

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
        options = Options()
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
        
    driver = get_driver()
    driver.get("https://www.example.com")
    st.write(driver.page_source)

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
