# Pujan Gautam - C0842623


from tkinter import *
import tkinter.messagebox
import tkinter
import requests
import json
import urllib
from PIL import ImageTk, Image
from io import BytesIO
from time import strftime
from datetime import datetime,timedelta


class OpenWeatherWindow:
    # initializing the window of the weather app
    current_time = datetime.now()
    time_to_update = 2
    future_time = current_time + timedelta(minutes=time_to_update)

    def __init__(self, window) -> None:
        self.title_lbl = Label(
            window, text="Welcome to Open Weather Application", fg='blue', font=("Helvetica", 16))
        self.title_lbl.pack()
        self.search_lbl = Label(
            window, text="Enter City Name: ", font=("Helvetica", 12))
        self.city_field = Entry(window, bd=2)

        self.btn_search = Button(window, text='Search', background="gray",
                                 width=15, padx=3, pady=3, command=self.get_weather)
        self.search_lbl.place(x=30, y=37)
        self.city_field.place(x=155, y=38, height=28)
        self.btn_search.place(x=300, y=35)
        self.clock_lbl = Label(window, font=("Helvetica", 30, 'bold'), bg="gray", fg="white", bd =20)
        self.clock_lbl.place(x=200,y=200)
        self.get_weather()
        self.time()


# function that get called when search button is clicked
# it fetch the data from the api and display it to user in user friendly way
    def get_weather(self):
        degree_sign = u"\N{DEGREE SIGN}"

        # getting the city name from the textbox
        city_name = self.city_field.get()

        # if textbox is empty then assigning a default value to the variable city_name
        if not city_name:
            city_name = 'Sarnia'

        # api key
        api_key = "a9fab8817de1e42dccbc4d342b3eac71"

        # url to call the api
        url = "http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s&units=metric" % (
            city_name, api_key)

        # exception handling while calling the api
        try:
            # calling the api and saving it to the response variable
            response = requests.get(url)
             # loading the response text into json format
            data = json.loads(response.text)

            # fetching required data such as temperature , wind speed
            # humidity, icon from the url as required
            temperature_celcius = data['main']['temp']
            country = data['sys']['country']
            feels_like = data['main']['feels_like']
            description = data['weather'][0]['description']
            wind_speed = data['wind']['speed'] 
            wind_deg = data['wind']['deg']
            humidity = data['main']['humidity']

            # making full url path to fetch the image from the cloud
            icon_url = "http://openweathermap.org/img/w/" + \
                data['weather'][0]['icon']+".png"
            
            # opening the url
            raw_data = urllib.request.urlopen(icon_url).read()
            # fetching image raw data 
            im = Image.open(BytesIO(raw_data))
            photo = ImageTk.PhotoImage(im)

            # calling celcius_to_fahrenheit function and assigning to temperature_fahrenheit variable
            temperature_fahrenheit = self.celcius_to_fahrenheit(
                temperature_celcius)
            # displaying the data fetched from api to the users 
            # in a Window Label
            self.city_name_lbl = Label(
                window, font=("Helvetica", 12))
            self.city_name_lbl.configure(text = city_name.capitalize() + ", "+country)
            self.city_name_lbl.place(x=30, y=80)
            self.current_time_lbl = Label(window,text="Updated At: "+str(self.current_time.strftime('%Y-%m-%d :: %I:%M:%S %p')),font=("Helvetica", 8))
            self.current_time_lbl.place(x=30,y=100)
            self.temp_label = Label(window, text=str(temperature_celcius)+degree_sign+"C / " + str(
                format(temperature_fahrenheit, '.2f'))+degree_sign+"F", font=("Helvetica", 12))
            self.temp_label.place(x=30, y=120)
            self.description = Label(window,text= description, font=("Helvetica", 8))
            self.description.place(x=30,y=150)
           
            self.feels_like_lbl = Label(
                window, font=("Helvetica", 12))
            self.feels_like_lbl.configure(text = 'Feels Like')
            self.feels_like_lbl.place(x=260, y=80)
            self.temp = Label(window, text= str(feels_like) + degree_sign+"C", font=("Helvetica", 12))
            self.temp.place(x=270, y=100)

            self.lbl_icon = Label(window, image=photo, width=50, height=30)
            self.lbl_icon.image = photo
            self.lbl_icon.place(x=350, y=80)

            self.humidity_lbl = Label (window,font=("Helvetica", 12),text= "Humidity")
            self.humidity_data_lbl = Label(window,text= humidity,font=("Helvetica", 12))
            self.humidity_lbl.place(x=30,y=150)
            self.humidity_data_lbl.place(x=30,y=170)

            self.wind_lbl = Label(window,text='Wind',font=("Helvetica", 12))
            self.wind_data = Label(window,text= str(wind_speed) +' mph / '+ str(wind_deg)+degree_sign,font=("Helvetica", 12))
            self.wind_lbl.place(x=230,y=150)
            self.wind_data.place(x=220,y=170)
        except:
            # showing messagebox if any exception arises while calling api
            tkinter.messagebox.showinfo("Error Message","Invalid City Name.")
            
    # method to convert celcius temperature to fahrenheit
    def celcius_to_fahrenheit(self, celcius):
        fahrenheit = 1.8 * celcius + 32
        return fahrenheit


# displaying clock time in the window
    def time(self):
        string = strftime('%I:%M:%S %p')
        self.clock_lbl.config(text = string)
        self.clock_lbl.after(1000, self.time)
        if(self.current_time == self.future_time):
            self.get_weather()
        


# main program
window = Tk()
open_weather = OpenWeatherWindow(window)
window.title("Open Weather")
window.geometry('500x300')
window.mainloop()
