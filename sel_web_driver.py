from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.service import Service
import requests

class voiceAssistantClass():

    def __init__(self):
        self.driver = webdriver.Chrome()
    def info(self, query):

        self.query = query
        self.driver.get(url="https://www.wikipedia.org")  # search net
        search = self.driver.find_element(By.XPATH, '//*[@id="searchInput"]')  # locate element in webpage by xpath
        search.click()  # click element
        search.send_keys(self.query)
        enter = self.driver.find_element(By.XPATH, '//*[@id="search-form"]/fieldset/button/i')
        enter.click()
        n = int(input("Press 0 to exit"))

        self.driver.quit()


    def video(self,query):

        self.query = query
        self.driver.get("https://www.youtube.com/results?search_query="+query)
        # search = self.driver.find_element(By.XPATH, '//*[@id="video-title"]')
        # search.click()
        input("Press enter to exit")
        self.driver.quit()

    def news(self):

        API_KEY= "c152cd342610465c94a1b0e54356f22c"
        api_address = "https://newsapi.org/v2/top-headlines?country=in&apiKey=" + API_KEY
        json_data = requests.get(api_address).json()
        arr = []
        #print(json_data)
        for i in range(3):
            arr.append("Number " + str(i + 1) + " " + json_data["articles"][i]["title"] + ".")
        return arr
    def jokes(self):

        url = "https://official-joke-api.appspot.com/random_joke"
        json_data = requests.get(url).json()
        arr = ["", ""]
        arr[0] = json_data["setup"]
        arr[1] = json_data["punchline"]
        return arr
        #  print(arr)

    def weather(self):

        api_key = "f6c2333b9450bb945905838bd7f1d175"
        url = f"https://api.openweathermap.org/data/2.5/weather?lat=8.4833&lon=76.9167&appid={api_key}"
        json_data = requests.get(url).json()
        print(json_data)
        arr = [" ", " "]
        temperature = str(round(json_data["main"]["temp"]-273))
        desc = json_data["weather"][0]["description"]
        arr[0] = str(temperature)
        arr[1] = desc
        #  print(arr)
        return arr




# def main():
#     assist = voiceAssistantClass()
#     assist.video("Hello world")
#
# if __name__ =="__main__":
#     main()


