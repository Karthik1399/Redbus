#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install selenium




# In[2]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def scrape_route(driver_sel, route_name, route_url):
    driver_sel.get(route_url)
    time.sleep(2)
    try:
        #WebDriverWait(driver_sel, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'custom-checkbox'))).click()
        WebDriverWait(driver_sel, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'button'))).click()
    except Exception as e:
        print(f"Exception occurred while clicking elements: {e}")
        return []

    # Scroll to ensure all elements are in view
    x = 0
    while True:
        x += 1
        driver_sel.execute_script('window.scrollBy(0, 100)')
        if x > 1000:
            break
    
    # Scrape the bus details
    bus_name = driver_sel.find_elements(By.CSS_SELECTOR, "div[class='travels lh-24 f-bold d-color']")
    bus_type = driver_sel.find_elements(By.CSS_SELECTOR, "div[class='bus-type f-12 m-top-16 l-color evBus']")
    departing_time = driver_sel.find_elements(By.CSS_SELECTOR, "div[class='dp-time f-19 d-color f-bold']")
    duration = driver_sel.find_elements(By.CSS_SELECTOR, "div[class='column-four p-right-10 w-10 fl']")
    reach_time = driver_sel.find_elements(By.CSS_SELECTOR, "div[class='column-five p-right-10 w-10 fl']")
    star_rating = driver_sel.find_elements(By.CSS_SELECTOR, "div[class='column-six p-right-10 w-10 fl']")
    price = driver_sel.find_elements(By.CSS_SELECTOR, "div[class='fare d-block']")
    seat_availability = driver_sel.find_elements(By.CSS_SELECTOR, "div[class='seat-left m-top-30']")

    def clean_text(element):
        return element.text.replace('\n', ' ').strip()
    # Determine the minimum length to ensure all lists are aligned
    min_length = min(len(bus_name), len(bus_type), len(departing_time), len(duration), len(reach_time), len(star_rating), len(price), len(seat_availability))
    
    gov_bus_data = []
    for i in range(min_length):
        bus_details = {
            'Route Name': route_name,
            'Route Link':route_url,
            'Bus Name': bus_name[i].text,
            'Bus Type': bus_type[i].text,
            'Departing Time': departing_time[i].text,
            'Duration': duration[i].text,
            'Reach Time': reach_time[i].text.split('\n')[0],
            'Star Rating': star_rating[i].text.split('\n')[0],
            'Price': price[i].text,
            'Seat Availability': seat_availability[i].text.split('\n')[0]
        }
        gov_bus_data.append(bus_details)

    return gov_bus_data

# Set up the WebDriver
driver_sel = webdriver.Chrome()
driver_sel.maximize_window()

# List of URLs for different routes
routes = [
    {"route_name": "Vijayawada to Hyderabad", "route_url": "https://www.redbus.in/bus-tickets/vijayawada-to-hyderabad?fromCityId=134&toCityId=124&fromCityName=Vijayawada&toCityName=Hyderabad&busType=Any&srcCountry=IND&destCountry=IND&onward=27-Jul-2024"},
    {"route_name": "Hyderabad to Vijayawada", "route_url": "https://www.redbus.in/bus-tickets/hyderabad-to-vijayawada?fromCityId=124&toCityId=134&fromCityName=Hyderabad&toCityName=Vijayawada&busType=Any&onward=29-Jul-2024"},
    {"route_name": "Kakinada to Visakhapatnam", "route_url":"https://www.redbus.in/bus-tickets/kakinada-to-visakhapatnam?fromCityId=316&toCityId=248&fromCityName=Kakinada&toCityName=Visakhapatnam&busType=Any&onward=16-Aug-2024"},
    {"route_name": "Visakhapatnam to Kakinada", "route_url":"https://www.redbus.in/bus-tickets/visakhapatnam-to-kakinada?fromCityId=248&toCityId=316&fromCityName=Visakhapatnam&toCityName=Kakinada&busType=Any&onward=16-Aug-2024"},
    {"route_name": "Chittoor (Andhra Pradesh) to Bangalore", "route_url":"https://www.redbus.in/bus-tickets/chittoor-andhra-pradesh-to-bangalore?fromCityId=653&toCityId=122&fromCityName=Chittoor%20(Andhra%20Pradesh)&toCityName=Bangalore&busType=Any&srcCountry=IND&destCountry=IND&onward=16-Aug-2024"},
    {"route_name": "Kadapa to Bangalore", "route_url":"https://www.redbus.in/bus-tickets/kadapa-to-bangalore?fromCityId=284&toCityId=122&fromCityName=Kadapa&toCityName=Bangalore&busType=Any&srcCountry=IND&destCountry=IND&onward=16-Aug-2024"},
    {"route_name": "Anantapur (andhra pradesh) to Bangalore", "route_url":"https://www.redbus.in/bus-tickets/ananthapur-to-bangalore?fromCityId=121&toCityId=122&fromCityName=Anantapur%20(andhra%20pradesh)&toCityName=Bangalore&busType=Any&srcCountry=IND&destCountry=IND&onward=16-Aug-2024"},
    {"route_name": "Tirupati to Bangalore", "route_url":"https://www.redbus.in/bus-tickets/tirupathi-to-bangalore?fromCityId=71756&toCityId=122&fromCityName=Tirupati&toCityName=Bangalore&busType=Any&srcCountry=IND&destCountry=IND&onward=16-Aug-2024"},
    {"route_name": "Visakhapatnam to Vijayawada", "route_url":"https://www.redbus.in/bus-tickets/visakhapatnam-to-vijayawada?fromCityId=248&toCityId=134&fromCityName=Visakhapatnam&toCityName=Vijayawada&busType=Any&srcCountry=IND&destCountry=IND&onward=16-Aug-2024"},
    {"route_name": "Ongole to Hyderabad", "route_url":"https://www.redbus.in/bus-tickets/ongole-to-hyderabad?fromCityId=135&toCityId=124&fromCityName=Ongole&toCityName=Hyderabad&busType=Any&srcCountry=IND&destCountry=IND&onward=16-Aug-2024"}
]

all_routes_data = []
for route in routes:
    route_name = route["route_name"]
    route_url = route["route_url"]

    # Scrape the data for this route
    route_data = scrape_route(driver_sel, route_name, route_url)
    all_routes_data.extend(route_data)

# Create a DataFrame with all the collected data
df_all_routes = pd.DataFrame(all_routes_data)

# Print the DataFrame
print(df_all_routes)



# Close the driver
driver_sel.quit()


# In[3]:


df = pd.DataFrame(df_all_routes)


# In[ ]:





# In[4]:


df


# In[5]:


