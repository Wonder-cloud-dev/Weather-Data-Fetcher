import requests
import tkinter as tk
from tkinter import messagebox

# Function to fetch weather data by city name
def get_weather_by_city(city):
    api_key = "f7967f47aed181cab741043dc7eaf71e"  # Replace with your actual API key
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,           # The city name (e.g., London)
        "appid": api_key,    # Your actual API key
        "units": "metric"    # Optional: to get the temperature in Celsius
    }
    try:
        # Make the API call
        response = requests.get(base_url, params=params)
        
        # Debugging: Print the request URL to verify correctness
        print(f"Request URL: {response.url}")
        
        # Raise error for bad responses
        response.raise_for_status()
        
        # Parse the response JSON
        data = response.json()
        
        # Check if 'cod' is 200, meaning the request was successful
        if data["cod"] != 200:
            raise ValueError(f"Error: {data.get('message', 'Unknown error')}")
        
        # Extract weather data
        weather = {
            "Location": data["name"],
            "Temperature": f"{data['main']['temp']} °C",
            "Weather": data["weather"][0]["description"].capitalize(),
            "Humidity": f"{data['main']['humidity']}%",
            "Wind Speed": f"{data['wind']['speed']} m/s"
        }
        return weather
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return {"Error": str(e)}

# Function to display weather information
def display_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return

    weather = get_weather_by_city(city)
    if "Error" in weather:
        messagebox.showerror("Error", f"Could not fetch weather data: {weather['Error']}")
    else:
        result_label.config(text=f"Location: {weather['Location']}\n"
                                 f"Temperature: {weather['Temperature']}\n"
                                 f"Weather: {weather['Weather']}\n"
                                 f"Humidity: {weather['Humidity']}\n"
                                 f"Wind Speed: {weather['Wind Speed']}")

# Function to clear input and output fields
def clear_fields():
    city_entry.delete(0, tk.END)
    result_label.config(text="")

# Create the UI
root = tk.Tk()
root.title("Weather Data Fetcher")
root.geometry("800x600")  # Increase the size of the window
root.resizable(False, False)

# Set background color with a gradient
root.configure(bg="#f5f5f5")

# Title Label with a modern font
title_label = tk.Label(root, text="Weather Data Fetcher", font=("Helvetica", 20, "bold"), fg="#ffffff", bg="#4CAF50", padx=10, pady=10)
title_label.pack(pady=20)

# City Input Label and Entry with improved styles
city_label = tk.Label(root, text="Enter City Name:", font=("Helvetica", 14), fg="#333", bg="#f5f5f5")
city_label.pack()
city_entry = tk.Entry(root, width=30, font=("Helvetica", 14), relief="flat", bd=2, fg="#333", bg="#e0e0e0", justify="center", borderwidth=3)
city_entry.pack(pady=10)

# Fetch Weather Button with rounded corners
fetch_button = tk.Button(root, text="Fetch Weather", command=display_weather, font=("Helvetica", 14), bg="#4CAF50", fg="white", relief="flat", height=2, width=20, bd=2, activebackground="#45a049")
fetch_button.pack(pady=10)

# Clear Button with rounded corners
clear_button = tk.Button(root, text="Clear", command=clear_fields, font=("Helvetica", 14), bg="#FF5733", fg="white", relief="flat", height=2, width=20, bd=2, activebackground="#ff451c")
clear_button.pack(pady=10)

# Result Label to display weather info
result_label = tk.Label(root, text="", font=("Helvetica", 14), fg="#333", bg="#f5f5f5", justify="left", padx=20)
result_label.pack(pady=20)

# Run the application
root.mainloop()
