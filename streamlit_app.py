

import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇') 

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
# Display the table on the page
streamlit.dataframe(my_fruit_list)
#Lets put a picklist here so they can pick the fruit they want to include
fruits_selected=streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]
#display the table on the page
streamlit.dataframe(fruits_to_show)
#New Section to display FruityVice api respone


#create the repeatable code block (calleda function)
def get_fruityvice_data(this_fruit_choice):
     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
     fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
     return fruityvice_normalized
#New Section to display FruityVice API Resonse
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice: 
        streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function=get_fruityvice_data(fruit_choice)
         streamlit.dataframe(back_from_function)
except URLError as e:
        streamlit.error()
#streamlit.text(fruityvice_response.json())
# FruityVice data JSON value normalized 
# output table
#don't run anything while we troubleshoot
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit list contains:")
#streamlit.text("Hello from Snowflake:")
streamlit.dataframe(my_data_rows)
#Allow the end user to add fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values ('from streamlit')")
         return 'Thanks for adding'+new_fruit
add_my_fruit= streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
         my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
         back_from_function=insert_row_snowflake(add_my_fruit)
         streamlit.text(back_from_function)
#streamlit.write('The user entered ', add_my_fruit)
#my_cur.execute("insert into fruit_load_list values ('from streamlit')")
#fruityvice_response = requests.put("https://fruityvice.com/api/fruit/"+add_my_fruit)
#streamlit.write('Thanks for adding',add_my_fruit)
#Adding data from streamlit
#my_cur.execute("insert into fruit_load_list values ('from streamlit')")
