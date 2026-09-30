"""
Garun AI Assistant - Weather Service
======================================
Provides weather information using wttr.in (free, no API key needed)
"""

import requests
from config import DEFAULT_CITY


class WeatherService:
    """Provides weather information"""
    
    def __init__(self):
        self.base_url = "https://wttr.in"
        self.default_city = DEFAULT_CITY
    
    def get_weather(self, city=None):
        """
        Get current weather for a city.
        
        Args:
            city: City name (uses default if not specified)
            
        Returns:
            Weather description string
        """
        city = city or self.default_city
        
        try:
            # wttr.in format options
            # ?format=j1 gives JSON
            url = f"{self.base_url}/{city}?format=j1"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract current conditions
            current = data.get('current_condition', [{}])[0]
            
            temp_c = current.get('temp_C', 'N/A')
            temp_f = current.get('temp_F', 'N/A')
            feels_like = current.get('FeelsLikeC', temp_c)
            humidity = current.get('humidity', 'N/A')
            description = current.get('weatherDesc', [{}])[0].get('value', 'Unknown')
            wind_speed = current.get('windspeedKmph', 'N/A')
            wind_dir = current.get('winddir16Point', '')
            
            # Get location info
            location = data.get('nearest_area', [{}])[0]
            area_name = location.get('areaName', [{}])[0].get('value', city)
            country = location.get('country', [{}])[0].get('value', '')
            
            # Format response
            response_text = (
                f"The weather in {area_name}, {country}:\n"
                f"• Condition: {description}\n"
                f"• Temperature: {temp_c}°C ({temp_f}°F)\n"
                f"• Feels like: {feels_like}°C\n"
                f"• Humidity: {humidity}%\n"
                f"• Wind: {wind_speed} km/h {wind_dir}"
            )
            
            return response_text
            
        except requests.exceptions.Timeout:
            return "I couldn't fetch the weather - the request timed out. Please try again."
        except requests.exceptions.RequestException as e:
            return f"I couldn't fetch the weather: {str(e)}"
        except Exception as e:
            return f"There was an error getting the weather: {str(e)}"
    
    def get_forecast(self, city=None, days=3):
        """
        Get weather forecast for upcoming days.
        
        Args:
            city: City name
            days: Number of days (1-3)
            
        Returns:
            Forecast description string
        """
        city = city or self.default_city
        days = min(max(1, days), 3)  # Limit to 1-3 days
        
        try:
            url = f"{self.base_url}/{city}?format=j1"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            weather_data = data.get('weather', [])
            
            if not weather_data:
                return "I couldn't get the forecast data."
            
            forecast_text = f"Weather forecast for {city}:\n\n"
            
            for i, day in enumerate(weather_data[:days]):
                date = day.get('date', 'Unknown')
                max_temp = day.get('maxtempC', 'N/A')
                min_temp = day.get('mintempC', 'N/A')
                
                # Get average conditions
                hourly = day.get('hourly', [{}])
                mid_day = hourly[len(hourly)//2] if hourly else {}
                description = mid_day.get('weatherDesc', [{}])[0].get('value', 'Unknown')
                
                forecast_text += (
                    f"📅 {date}\n"
                    f"   {description}\n"
                    f"   High: {max_temp}°C | Low: {min_temp}°C\n\n"
                )
            
            return forecast_text.strip()
            
        except Exception as e:
            return f"I couldn't get the forecast: {str(e)}"
    
    def get_simple_weather(self, city=None):
        """
        Get a simple one-line weather summary.
        
        Args:
            city: City name
            
        Returns:
            Simple weather string
        """
        city = city or self.default_city
        
        try:
            # Simple format
            url = f"{self.base_url}/{city}?format=%C+%t"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            return f"Weather in {city}: {response.text.strip()}"
            
        except Exception as e:
            return f"Couldn't get weather: {str(e)}"
