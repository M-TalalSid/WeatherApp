import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import folium_static
import plotly.express as px
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="WeatherWise 🌦️",
    page_icon="🌦️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# OpenWeatherMap API key
API_KEY = "e2d212042e435a5989262759580b7171"  # Replace with your API key

# Function to fetch current weather
def get_current_weather(city, units="metric"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}"
    response = requests.get(url)
    return response.json()

# Function to fetch 5-day forecast
def get_forecast(city, units="metric"):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={units}"
    response = requests.get(url)
    return response.json()

# Function to fetch historical weather
def get_historical_weather(lat, lon, date, units="metric"):
    url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={date}&appid={API_KEY}&units={units}"
    response = requests.get(url)
    return response.json()

# Function to fetch air quality
def get_air_quality(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    return response.json()

# Function to fetch UV index
def get_uv_index(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,daily,alerts&appid={API_KEY}"
    response = requests.get(url)
    return response.json()

# Function to display weather icon
def display_weather_icon(icon_code):
    st.image(f"http://openweathermap.org/img/wn/{icon_code}@2x.png", width=100)

# Function to display sunrise and sunset times
def display_sunrise_sunset(sunrise, sunset):
    sunrise_time = datetime.fromtimestamp(sunrise).strftime("%H:%M")
    sunset_time = datetime.fromtimestamp(sunset).strftime("%H:%M")
    st.write(f"**Sunrise:** 🌅 {sunrise_time}")
    st.write(f"**Sunset:** 🌇 {sunset_time}")

# Function to create a weather widget
def create_weather_widget(title, value, unit, icon):
    st.markdown(
        f"""
        <div style="
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: #f9f9f9;
            margin: 10px 0;
        ">
            <h3>{title}</h3>
            <h2>{value} {unit}</h2>
            <p>{icon}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# App title and description
st.title("WeatherWise 🌦️")
st.write("Your ultimate weather companion. Stay informed, stay prepared.")

# Sidebar for user input and settings
with st.sidebar:
    st.header("Settings ⚙️")
    
    # Theme customization
    st.subheader("Theme 🎨")
    theme = st.selectbox("Choose Theme", ["Light", "Dark"])
    if theme == "Dark":
        st.markdown("<style>body {color: white; background-color: #0E1117;}</style>", unsafe_allow_html=True)
    
    # Language selection
    st.subheader("Language 🌐")
    language = st.selectbox("Choose Language", ["English", "Spanish", "French"])
    
    # Favorite locations
    st.subheader("Favorite Locations ❤️")
    favorite_locations = st.multiselect("Add or select favorite locations:", ["Karachi", "Mekkah", "Italy", "London", "Paris", "Chicago"])
    
    # Notification preferences
    st.subheader("Notifications 🔔")
    rain_alert = st.checkbox("Notify me when it rains")
    snow_alert = st.checkbox("Notify me when it snows")
    high_wind_alert = st.checkbox("Notify me of high winds")
    
    # Unit preferences
    st.subheader("Units 📏")
    units = st.selectbox("Select units:", ["metric", "imperial"])
    
    # About section
    st.markdown("---")
    st.subheader("About ℹ️")
    st.write("WeatherWise is a Smart Weather App built with ❤️")
    st.write("Developed by [Talal Shoaib].")
    
    # Feedback form
    st.markdown("---")
    st.subheader("Feedback 📝")
    feedback = st.text_area("Share your feedback or report issues:")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")

# Fetch and display current weather
st.header("Current Weather ⛅")
city = st.text_input("Enter city name:", "Karachi")
current_weather = get_current_weather(city, units)
if current_weather.get("cod") != 200:
    st.error("City not found. Please try again.")
else:
    col1, col2 = st.columns(2)
    with col1:
        display_weather_icon(current_weather["weather"][0]["icon"])
    with col2:
        st.write(f"**Temperature:** {current_weather['main']['temp']}°{'C' if units == 'metric' else 'F'}")
        st.write(f"**Humidity:** {current_weather['main']['humidity']}%")
        st.write(f"**Wind Speed:** {current_weather['wind']['speed']} {'m/s' if units == 'metric' else 'mph'}")
        st.write(f"**Conditions:** {current_weather['weather'][0]['description'].capitalize()}")

    # Display sunrise and sunset times
    st.subheader("Sunrise and Sunset Times 🌅🌇")
    display_sunrise_sunset(current_weather["sys"]["sunrise"], current_weather["sys"]["sunset"])

# Weather widgets
st.header("Weather Widgets 📊")
col1, col2, col3 = st.columns(3)
with col1:
    create_weather_widget("Temperature", current_weather["main"]["temp"], "°C" if units == "metric" else "°F", "🌡️")
with col2:
    create_weather_widget("Humidity", current_weather["main"]["humidity"], "%", "💧")
with col3:
    create_weather_widget("Wind Speed", current_weather["wind"]["speed"], "m/s" if units == "metric" else "mph", "🌬️")

# Fetch and display 5-day forecast
st.header("5-Day Forecast 📅")
forecast = get_forecast(city, units)
if forecast.get("cod") != "200":
    st.error("Forecast data unavailable.")
else:
    forecast_data = []
    for entry in forecast["list"]:
        date = entry["dt_txt"]
        temp = entry["main"]["temp"]
        humidity = entry["main"]["humidity"]
        wind_speed = entry["wind"]["speed"]
        conditions = entry["weather"][0]["description"]
        forecast_data.append([date, temp, humidity, wind_speed, conditions])
    forecast_df = pd.DataFrame(forecast_data, columns=["Date", "Temperature", "Humidity", "Wind Speed", "Conditions"])
    st.dataframe(forecast_df)

# Display interactive map
st.header("Interactive Map 🗺️")
lat = current_weather["coord"]["lat"]
lon = current_weather["coord"]["lon"]
m = folium.Map(location=[lat, lon], zoom_start=10)
folium.Marker([lat, lon], tooltip=city).add_to(m)
folium_static(m)

# Fetch and display air quality
st.header("Air Quality Index (AQI) 🌫️")
air_quality = get_air_quality(lat, lon)
if air_quality.get("cod"):
    st.error("Air quality data unavailable.")
else:
    aqi = air_quality["list"][0]["main"]["aqi"]
    st.write(f"**AQI:** {aqi} (1 = Good, 5 = Poor)")

# Fetch and display UV index
st.header("UV Index ☀️")
uv_index = get_uv_index(lat, lon)
if uv_index.get("cod"):
    st.error("UV index data unavailable.")
else:
    uv = uv_index["current"]["uvi"]
    st.write(f"**UV Index:** {uv}")
    if uv >= 8:
        st.warning("Very high UV index. Wear sunscreen and avoid prolonged sun exposure.")
    elif uv >= 6:
        st.warning("High UV index. Wear sunscreen.")
    else:
        st.success("UV index is moderate. Enjoy the sun safely!")

# Fetch and display historical weather
st.header("Historical Weather 📜")
historical_date = st.date_input("Select a date:", datetime.now() - timedelta(days=1))
if st.button("Get Historical Weather"):
    historical_weather = get_historical_weather(lat, lon, int(historical_date.timestamp()), units)
    if historical_weather.get("cod") != "200":
        st.error("Historical data unavailable.")
    else:
        st.write(f"**Temperature:** {historical_weather['current']['temp']}°{'C' if units == 'metric' else 'F'}")
        st.write(f"**Conditions:** {historical_weather['current']['weather'][0]['description'].capitalize()}")

# Footer
st.markdown("---")
st.markdown("©2025 Streamlit Weather App. All Rights Reserved.")