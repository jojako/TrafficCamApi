import json
import tkinter as tk
from io import BytesIO
import requests
from PIL import Image, ImageTk

timer_id = ''
camera_dict = {}
api_url = "https://data.goteborg.se/TrafficCamera/v1.0/TrafficCameras/2045abfc-4065-4741-a580-1755cbe3e245?format=json"

class Users:
    def __init__(self):
        pass


class ApiCon:
    def __init__(self):
        r = requests.get(api_url)
        if r.status_code == requests.codes.ok:
            r_parsed = json.loads(r.text)
            for i in r_parsed:
                camera_dict[i['Name']] = i['CameraImageUrl']
        else:
            print("Error")

    def get_camera(self, camera_name):
        if camera_name in camera_dict:
            r = requests.get(camera_dict.get(camera_name))
            return r
        else:
            return None


class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Gothenburg Traffic Cameras")
        self.window.geometry("800x660")
        self.window.eval('tk::PlaceWindow . center')

        self.image_placeholder = tk.Label(text="Image goes here", background="black", width=680, height=550)
        self.image_placeholder.pack_forget()

        self.clicked = tk.StringVar()
        self.clicked.set("Select a camera")
        self.dropdown = tk.OptionMenu(self.window, self.clicked, *camera_dict.keys(), command=self.show_camera)
        self.dropdown.place(x=54, y=600)

        self.countdown_text = tk.StringVar()
        self.countdown_label = tk.Label(text="")
        self.countdown_label.place(x=600, y=600)

        self.close_button = tk.Button(self.window, text="Close", height=1, width=8, command=self.window.destroy)
        self.close_button.place(x=680, y=600)

        self.window.mainloop()

    def show_camera(self, x):
        self.choice = self.clicked.get()
        self.returned_image = api_con.get_camera(self.choice)
        self.image_data = self.returned_image.content
        self.image_data_processed = ImageTk.PhotoImage(Image.open(BytesIO(self.image_data)))
        self.image_placeholder.configure(image=self.image_data_processed)
        self.image_placeholder.pack()

        self.countdown(10)
        self.window.mainloop()

    def countdown(self, count):
        global timer_id
        try:
            self.window.after_cancel(timer_id)
        except:
            pass

        self.countdown_label["text"] = f"Refresh in {count}s"
        if count > 0:
            timer_id = self.window.after(1000, self.countdown, count-1)
        elif count == 0:
            #Uppdatera bilden
            pass


api_con = ApiCon()
main = MainWindow()