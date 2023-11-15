import datetime as dt
import requests
from datetime import datetime
file_path = "API_key.txt"  # Replace with the path to your file
try:
    with open(file_path, "r") as file:
        # Read the entire file content
        API_KEY = file.read()
        
except FileNotFoundError:
    print(f"The file '{file_path}' does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")


base_URL = "https://api.openweathermap.org/data/2.5/weather?"

City = input("What city?: ")
Units = input("Fahrenheit(Type F) or Celsius?(Type C): ")

if Units.upper() == "F":
    displayTemp = "&units=imperial"
elif Units.upper() == "C":
     displayTemp = "&units=metric"
else:
    displayTemp = "&units=imperial"
    Units = "F"


url= base_URL + "appid=" + API_KEY + displayTemp +"&q=" + City
response = requests.get(url).json()

# Longitude and Latitude
lon = response["coord"]["lon"]
lat = response["coord"]["lat"]

# Weather Rain, Snow, Clear, Cloud etc...
w = response["weather"][0]["main"]

#Temutures  
temp = response ["main"]["temp"]
feels = response ["main"]["feels_like"]
max =response ["main"]["temp_max"]
min =response ["main"]["temp_min"]
# City name 
place = response["name"]

# Country
c = response["sys"]["country"]


# Displays the waether conditons in the desired City 
print(f"Today in {place} {c} it is {w}")
# displays The tempaure
print(f"The tempauture is {temp} degrees {Units.upper()}")
print(f"It feels like {feels} degrees {Units.upper()}")
print(f"The maximum is {max} degrees {Units.upper()}")
print(f"The minimum {min} degrees {Units.upper()}")
# Earthquake 
# https://earthquake.usgs.gov/fdsnws/event/1/[METHOD[?PARAMETERS]]

# The folowing 3 functions will be used to get the a date from the user
def get_year():
    Valid = False 
    date = datetime.now()
    while Valid == False:
        try:
            num =int(input("Enter a Year: "))
            if num <= date.year and num >= 1000:
                Valid = True
        except:
           pass 
        if not Valid:
            print(f"Invalid number must be a 4 digit number not larger than {date.year}. Example")
         
    return num

def get_month():
    Valid = False 
    valid_options = ["01", "02","03", "04", "05","06","07","08","09","10","11","12"]
    while Valid == False:
        num = input("Enter a month: ")
        if num in valid_options:
            Valid = True
        else:
            print("Invalid number must be a 2 digit number not larger than 12.")
            print("Example: January = 01")    
        
    return num
def get_day():
    Valid = False 
    while Valid == False:
        try:
            num =int(input("enter a day: "))
            if num <= 31 and num >= 1:
                Valid = True
        except:
           pass 
        if not Valid:
            print("Invalid number must be a 2 digit number not larger than 31.")
            print("example: 2nd day of the month = 02")         
    return num



print("How far back should I look for earthquake data?")
#User input 
Year = str(get_year())
month= str(get_month())
day = str(get_day())

startTime = f"{Year}-{month}-{day}"
endTime = datetime.now().strftime('%Y-%m-%d')
current_date = datetime.now().date()
earthquake_base_URL = "https://earthquake.usgs.gov/fdsnws/event/1/"
query = f"query?format=geojson&latitude={lat}&longitude={lon}"
StartEndTime =f"&maxradius=10&starttime={startTime}&{endTime}&minmagnitude=5"
url = earthquake_base_URL + query + StartEndTime 


response = requests.get(url).json()
warning =response["metadata"]["count"]

if warning != 0:#Meaning there have been least one magnitude 5 or greater EarthQuake within a 10 degree raduius  
    print(f"\n Here are the earthqukes within a 10 degree radius of {place}")
    print(f"That occured {startTime} to {datetime.now().strftime('%Y-%m-%d')}  (Year-Month-Day)")
    for feature in response['features']:
        place = feature['properties']['place']
        magnitude = feature['properties']['mag']
        print(f"Location: {place}")
        print(f"Magnitude: {magnitude}")
        print("-" * 20)
else: #warning = 0 means no earthqukes  
    print(f"No earthquke data within a 10 degree radius of {place}")





