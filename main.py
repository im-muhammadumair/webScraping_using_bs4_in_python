import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def scrape_weather_data():
    """
    Function to scrape weather data for cities in Pakistan from the Met Office website.
    It collects city names, temperatures, and predefined weather conditions.
    Returns:
        pd.DataFrame: DataFrame containing city names, temperatures, and conditions.
    """
    # Define the URL to scrape data from
    url = "https://www.metoffice.gov.uk/weather/world/pakistan"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Lists to store scraped data
    city_name = []
    temperature = []
    conditions = ["Sunny", "Cloudy", "Sunny", "Rain", "Sunny", "Cloudy", 
                  "Rain", "Sunny", "Cloudy", "Smoky"]  # Predefined conditions for simplicity

    # Scrape city names, ignoring non-city entries
    cities = soup.find_all('span', class_='link-text')
    for city in cities:
        city_text = city.text.strip()
        if city_text not in ["Home", "All countries"]:  # Filter out irrelevant entries
            city_name.append(city_text)

    # Scrape temperature data
    temp_text = soup.find_all('span', class_='temp')
    for temp in temp_text:
        each_temp = temp.text.strip()
        temperature.append(each_temp)
    
    # Create a DataFrame with the scraped data
    df = pd.DataFrame({
        'City': city_name,
        'Temperature': temperature,
        'Condition': conditions
    })

    return df

def display_weather_data():
    """
    Function to display the weather data using Streamlit.
    It allows the user to view, search, and sort the weather data.
    """
    # Fetch weather data
    df = scrape_weather_data()

    # Display the main weather data
    st.title('Weather Data for Pakistan')
    st.subheader('Weather Data')
    st.dataframe(df)

    # Search functionality for city-based filtering
    search_city = st.text_input("Search for a city:")
    if search_city:
        # Filter DataFrame for the searched city
        search_result = df[df['City'].str.contains(search_city, case=False, na=False)]
        if not search_result.empty:
            st.write(f"Results for '{search_city}':")
            st.dataframe(search_result)
        else:
            st.write("No results found for that city.")

    # Sorting functionality based on temperature
    sort_option = st.radio("Sort by temperature?", ('No', 'Yes'))
    if sort_option == 'Yes':
        # Convert temperature data to numeric for sorting
        df['Temperature'] = df['Temperature'].str.replace('°C', '').astype(str)
        df_sorted = df.sort_values(by='Temperature', ascending=True)
        
        # Display sorted data
        st.subheader('Sorted Weather Data (by Temperature)')
        st.dataframe(df_sorted)

# Run the application
if __name__ == '__main__':
    display_weather_data()