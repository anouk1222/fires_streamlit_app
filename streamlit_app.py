
import streamlit
import pandas 
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('My parents new healthy diner')

streamlit.header('Breakfast favorites')
streamlit.text('🥣 Omega 3 & Bluebery Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled free range egg')
streamlit.text('🥑🍞 Avocado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
# Let's put a pick list here so they can pick the fruit they want to include 
fruit_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruit_to_show = my_fruit_list.loc[fruit_selected]
# Display the table on the page.
streamlit.dataframe(fruit_to_show)
streamlit.header("Fruityvice Fruit Advice!")

def get_fruit(this_fruit):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruit advice")
try :
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice :
    streamlit.error('please select a fruit to get information')
  else : 
    A = get_fruit(fruit_choice)
    streamlit.dataframe(A)
except URLError as e :
  streamlit.error()



  
  
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load contains:")
streamlit.dataframe(my_data_rows)

fruit_choice1 = streamlit.text_input('What fruit would you like to add?')
streamlit.write('The user entered ', fruit_choice1)
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values (fruit_choice1)");








