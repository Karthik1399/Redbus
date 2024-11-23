#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install selenium


# In[2]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import execjs



driver_sel = webdriver.Chrome() 
driver_sel.get("https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile");

driver_sel.maximize_window()
time.sleep(2)

pagination_table = driver_sel.find_element(By.CLASS_NAME, 'DC_117_paginationTable')
def is_in_view(driver_sel, element):
    element_location = element.location
    window_height = driver_sel.execute_script("return window.innerHeight")
    scroll_y = driver_sel.execute_script("return window.scrollY")
    
    if scroll_y <= element_location['y'] <= (scroll_y + window_height):
        return True
    else:
        return False
    
while True:
    if is_in_view(driver_sel, pagination_table):
        break
    else:
        driver_sel.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)

bus_routes = driver_sel.find_elements(By.CLASS_NAME, "route")

bus_route_link = driver_sel.find_elements(By.CLASS_NAME, "route_link")

bus_routes_data = [route.text for route in bus_routes]
bus_route_links = [route_link.text for route_link in bus_route_link]

driver_sel.get("https://www.redbus.in/bus-tickets/vijayawada-to-hyderabad?fromCityId=134&toCityId=124&fromCityName=Vijayawada&toCityName=Hyderabad&busType=Any&srcCountry=IND&destCountry=IND&onward=27-Jul-2024");

check_box = driver_sel.find_element(By.CLASS_NAME,'custom-checkbox').click()

Govt_bus = driver_sel.find_element(By.CLASS_NAME,'button').click()


x = 0


while True:
    x=x+1
    driver_sel.execute_script('window.scrollBy(0,100)')
    if(x>1000):
        break

df_bus_routes = pd.DataFrame(bus_routes_data, columns=['Bus Route'])
df_bus_link = pd.DataFrame(bus_route_links, columns=['Links'])
    
 
bus_name = driver_sel.find_elements(By.CSS_SELECTOR,"div[class='travels lh-24 f-bold d-color']")
bus_type = driver_sel.find_elements(By.CSS_SELECTOR,"div[class='bus-type f-12 m-top-16 l-color evBus']")
Departing_time = driver_sel.find_elements(By.CSS_SELECTOR,"div[class='dp-time f-19 d-color f-bold']")
Duration = driver_sel.find_elements(By.CSS_SELECTOR,"div[class='column-four p-right-10 w-10 fl']")
Reach_time = driver_sel.find_elements(By.CSS_SELECTOR,"div[class='column-five p-right-10 w-10 fl']")
Star_rating = driver_sel.find_elements(By.CSS_SELECTOR,"div[class='column-six p-right-10 w-10 fl']")
price = driver_sel.find_elements(By.CSS_SELECTOR,"div[class='fare d-block']")
seat_availabilty = driver_sel.find_elements(By.CSS_SELECTOR,"div[class = 'seat-left m-top-30']")


print(f"bus_name: {len(bus_name)}")
print(f"bus_type: {len(bus_type)}")
print(f"Departing_time: {len(Departing_time)}")
print(f"Duration: {len(Duration)}")
print(f"Reach_time: {len(Reach_time)}")
print(f"Star_rating: {len(Star_rating)}")
print(f"price: {len(price)}")
print(f"seat_availabilty: {len(seat_availabilty)}")

min_length = min(len(bus_name), len(bus_type), len(Departing_time), len(Duration), len(Reach_time), len(Star_rating), len(price), len(seat_availabilty))
gov_bus_data = []
for i in range(min_length):
    bus_details = {
        'Bus Name': bus_name[i].text,
        'Bus Type': bus_type[i].text,
        'Departing Time': Departing_time[i].text,
        'Duration': Duration[i].text,
        'Reach Time': Reach_time[i].text,
        'Star Rating': Star_rating[i].text,
        'Price': price[i].text,
        'Seat Availability': seat_availabilty[i].text
    }
    gov_bus_data.append(bus_details)

print(gov_bus_data)

# Create DataFrames
df_bus_routes = pd.DataFrame(bus_routes_data, columns=['Bus Route'])
df_bus_link = pd.DataFrame(bus_route_links, columns=['Links'])
df_gov_bus = pd.DataFrame(gov_bus_data)

# Print DataFrames
print(df_bus_routes)
print(df_bus_link)
print(df_gov_bus)


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


pip install mysql.connector


# In[6]:


import mysql.connecctor


# In[7]:


import mysql.connector


# In[8]:


con= mysql.connector.connect(
    host="Redbus",
    user="root",
    password="K@rt1312",
    autocommit=True
    )
print(con)


# In[9]:


import mysql.connector
mydb = mysql.connector.connect(
  host="Redbus",
  user="root",
  password= "K@rt1312"
)

print(mydb)


# In[23]:


import mysql.connector

db=mysql.connector.connect(
   host="127.0.0.1",
   port="3306",
   user="root",
   passwd="1234",
   database="Redbus"
)


# In[10]:



pip install pymysql


# In[11]:


import pymysql

con= pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="K@rt1312",
    autocommit=True
    )
print(con)


# In[14]:


# mysql.connector   - caching sha2 password error-  innodb
# pymysql
# psycopg2 - postgresql
# pyodbc- microsoft sql server
# sqlalchemy  engine


# In[12]:


mycursor = con.cursor()
mycursor.execute('CREATE DATABASE Redbus_data')


# In[13]:


mycursor.execute("SHOW DATABASES")


# In[14]:


for x in mycursor:
    print(x)


# In[15]:


mycursor.execute("USE redbus_data")


# In[16]:


mycursor.execute("""CREATE table bus_routes(id int auto_increment primary key, route_name varchar(50), route_link varchar(1000), busname varchar(100), bustype varchar(100), departing_time TIME , duration varchar(100), reaching_time TIME, star_rating FLOAT, price decimal(10,2),seats_available int);""")


# In[40]:


from decimal import Decimal

# Function to clean and convert 'price' column
def clean_price(value):
    try:
        # Remove 'INR ' prefix and commas, then convert to Decimal
        cleaned_value = str(value).replace('INR ', '').replace(',', '')
        return Decimal(cleaned_value)
    except (ValueError, InvalidOperation):
        return None  # Handle or log cases where conversion fails

# Clean the 'price' column
df['Price'] = df['Price'].apply(clean_price)

# Function to clean and convert 'seats_available' column
def clean_seats(value):
    try:
        # Convert to string, strip whitespace, then convert to int
        return int(str(value).strip())
    except ValueError:
        return None 

# Clean the 'seats_available' column
df['Seat Availability'] = df['Seat Availability'].apply(clean_seats)

# Remove rows where 'seats_available' is None (optional)
df = df.dropna(subset=['Seat Availability'])


# Define the insert query
insert_query = """
INSERT INTO bus_routes (route_name,route_link ,busname,bustype,departing_time,duration,reaching_time,star_rating,price,seats_available) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)
"""

# Iterate over the DataFrame and insert each row
for index, row in df.iterrows():
    mycursor.execute(insert_query, (row['Route Name'], row['Route Link'], row['Bus Name'], row['Bus Type'] , row['Departing Time'], row['Duration'], row['Reach Time'], row['Star Rating'], row['Price'], row['Seat Availability']))

# Commit the transaction
con.commit()


# In[41]:


df.columns


# In[42]:


# Define the insert query
insert_query = """
INSERT INTO bus_routes (route_name,route_link ,busname,bustype,departing_time,duration,reaching_time,star_rating,price,seats_available) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)
"""

# Iterate over the DataFrame and insert each row
for index, row in df.iterrows():
    Seat_availability = int(row['Seat Availability'].split()[0])
    mycursor.execute(insert_query, (row['Route Name'], row['Route Link'], row['Bus Name'], row['Bus Type'] , row['Departing Time'], row['Duration'], row['Reach Time'], row['Star Rating'], row['Price'], row['Seat Availability']))

# Commit the transaction
conn.commit()


# In[43]:


print(insert_query)


# In[44]:


print(df)


# In[45]:


from decimal import Decimal

# Function to clean and convert 'price' column
def clean_price(value):
    try:
        # Remove 'INR ' prefix and commas, then convert to Decimal
        cleaned_value = str(value).replace('INR ', '').replace(',', '')
        return Decimal(cleaned_value)
    except (ValueError, InvalidOperation):
        return None  # Handle or log cases where conversion fails

# Clean the 'price' column
df['Price'] = df['Price'].apply(clean_price)

# Function to clean and convert 'seats_available' column
def clean_seats(value):
    try:
        # Convert to string, strip whitespace, then convert to int
        return int(str(value).strip())
    except ValueError:
        return None 

# Clean the 'seats_available' column
df['Seat Availability'] = df['Seat Availability'].apply(clean_seats)

# Remove rows where 'seats_available' is None (optional)
df = df.dropna(subset=['Seat Availability'])


# Define the insert query
insert_query = """
INSERT INTO bus_routes (route_name,route_link ,busname,bustype,departing_time,duration,reaching_time,star_rating,price,seats_available) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)
"""

# Iterate over the DataFrame and insert each row
for index, row in df.iterrows():
    mycursor.execute(insert_query, (row['Route Name'], row['Route Link'], row['Bus Name'], row['Bus Type'] , row['Departing Time'], row['Duration'], row['Reach Time'], row['Star Rating'], row['Price'], row['Seat Availability']))

# Commit the transaction
con.commit()


# In[46]:


mycursor = con.cursor()
fetch_query = "SELECT * FROM bus_routes"
mycursor.execute(fetch_query)
rows = mycursor.fetchall()
for row in rows:
    print(row)
    
mycursor.close()


# In[47]:


df


# In[88]:


df


# In[97]:


import pandas as pd
from decimal import Decimal

# Define cleaning functions
def clean_price(value):
    try:
        cleaned_value = str(value).replace('INR ', '').replace(',', '')
        return Decimal(cleaned_value)
    except (ValueError, InvalidOperation):
        return None

def clean_seats(value):
    try:
        cleaned_value = str(value).strip()
        return int(cleaned_value) if cleaned_value.isdigit() else None
    except ValueError:
        return None

# Load and clean DataFrame
 # Replace with your actual data source

df['Price'] = df['Price'].apply(clean_price)
df['Seat Availability'] = df['Seat Availability'].apply(clean_seats)

# Print the DataFrame to check values before insertion
print("DataFrame before insertion:")
print(df)

# Check for any potential issues
print("\nChecking for rows with null values:")
print(df[df['Price'].isnull() | df['Seat Availability'].isnull()])



# Define the insert query
insert_query = """
INSERT INTO bus_routes (route_name, route_link, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Iterate over the DataFrame and insert each row
for index, row in df.iterrows():
    try:
        mycursor.execute(insert_query, ("""
            row['Route Name'], 
            row['Route Link'], 
            row['Bus Name'], 
            row['Bus Type'], 
            row['Departing Time'], 
            row['Duration'], 
            row['Reach Time'], 
            row['Star Rating'], 
            row['Price'], 
            row['Seat Availability']
        """))
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Commit the transaction
con.commit()

# Close the cursor and connection
mycursor.close()
con.close()


# In[100]:


import pymysql

con= pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="K@rt1312",
    autocommit=True
    )
print(con)


# In[101]:


mycursor = con.cursor()


# In[103]:


mycursor.execute("USE redbus_data")


# In[115]:


import pandas as pd
print(pd.__version__)


# In[49]:






# Define the insert query
insert_query = """
INSERT INTO bus_routes (route_name, route_link, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

# Iterate over the DataFrame and insert each row
for index, row in df.iterrows():
    try:
        # Clean the price by removing 'INR ' and converting to float
        price = row['Price'].replace('INR ', '').strip()
        
        # Clean seat availability by extracting the numeric part and converting to integer
        seats_available = int(row['Seat Availability'].split()[0].strip())
        star_rating_str = row['Star Rating'].strip()
        # Here, we assume star rating can be a float
        star_rating = float(''.join(filter(lambda x: x.isdigit() or x == '.', star_rating_str)))
        # Execute the insert query
        mycursor.execute(insert_query, (
            row['Route Name'], row['Route Link'], row['Bus Name'], row['Bus Type'], 
            row['Departing Time'], row['Duration'], row['Reach Time'], row['Star Rating'], 
            price, seats_available
        ))
    except (ValueError, IndexError) as e:
        print(f"Error processing row {index}: {row} - {e}")

# Commit the transaction
con.commit()


# In[126]:





# In[1]:


pip install streamlit


# In[17]:


import streamlit as st


conn = st.connection("Redbus_data")
df1 = conn.query("select * from bus_routes")
st.dataframe(df1)


# In[18]:


streamlit run C:\Users\Karthik\anaconda3\lib\site-packages\ipykernel_launcher.py


# In[19]:


import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Function to load data from your MySQL database
@st.cache_data
def load_data():
    # Update with your MySQL connection string
    engine = create_engine("mysql+pymysql://root:K@rt1312@127.0.0.1/Redbus_data")
    query = "SELECT * FROM bus_routes"
    df = pd.read_sql(query, engine)
    return df

# Load the scraped data
df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")

# Filter by bus type
bus_types = df['bustype'].unique()
selected_bus_type = st.sidebar.multiselect("Select Bus Type", bus_types, bus_types)

# Filter by route
routes = df['route_name'].unique()
selected_route = st.sidebar.multiselect("Select Route", routes, routes)

min_

# Filter by price range
min_price, max_price = st.sidebar.slider(
    "Select Price Range",
    int(df['price'].min()), int(df['price'].max()),
    (int(df['price'].min()), int(df['price'].max()))
)

# Filter by star rating
min_rating, max_rating = st.sidebar.slider(
    "Select Star Rating",
    float(df['rating'].min()), float(df['rating'].max()),
    (float(df['rating'].min()), float(df['rating'].max()))
)

# Filter by availability
min_seats, max_seats = st.sidebar.slider(
    "Select Seat Availability",
    int(df['availability'].min()), int(df['availability'].max()),
    (int(df['availability'].min()), int(df['availability'].max()))
)

# Apply filters
filtered_df = df[
    (df['bus_type'].isin(selected_bus_type)) &
    (df['route'].isin(selected_route)) &
    (df['price'] >= min_price) &
    (df['price'] <= max_price) &
    (df['rating'] >= min_rating) &
    (df['rating'] <= max_rating) &
    (df['availability'] >= min_seats) &
    (df['availability'] <= max_seats)
]

# Display filtered data
st.title("Bus Information")
st.dataframe(filtered_df)

# Optional: Add a summary or statistics
st.subheader("Summary")
st.write(f"Total buses found: {filtered_df.shape[0]}")


# In[ ]:




