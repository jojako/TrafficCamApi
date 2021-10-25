import json
import tkinter as tk
from io import BytesIO
import requests
from PIL import Image, ImageTk


class ApiCon:
    def __init__(self, api_url):
        self.api_url = api_url
        self.camera_dict = {}

    def load_cameras(self):
        r = requests.get(self.api_url)
        if r.status_code == requests.codes.ok:
            r_parsed = json.loads(r.text)
            for i in r_parsed:
                self.camera_dict[i['Name']] = i['CameraImageUrl']
        else:
            print("Error")

    def get_camera_image(self, camera_name):
        if camera_name in self.camera_dict:
            r = requests.get(self.camera_dict.get(camera_name))
            return r
        else:
            return None


class ApiWindow:
    def __init__(self, is_main_opened):
        self.main_opened = is_main_opened

        self.api_window = tk.Tk()
        self.api_window.title("Set API-Key")

        api_window_width = 266
        api_window_height = 160
        ws = self.api_window.winfo_screenwidth()
        hs = self.api_window.winfo_screenheight()
        x = (ws/2) - (api_window_width/2)
        y = (hs/2) - (api_window_height/2)

        self.api_window.geometry('%dx%d+%d+%d' % (api_window_width, api_window_height, x, y))

        self.api_textbox = tk.Text(self.api_window, height=6, width=30)

        try:
            self.api_textbox.insert(1.0, api_con.api_url)
        except:
            pass

        self.api_textbox.place(x=10, y=10)

        self.close_button = tk.Button(self.api_window, text="Close", height=1, width=8, command=self.close_button)
        self.close_button.place(x=100, y=122)

        self.api_window.mainloop()

    def close_button(self):
        entered_api_url = self.api_textbox.get("1.0", "end-1c")

        if entered_api_url:
            with open('api.txt', 'w') as f:
                f.write(entered_api_url)

            global api_con
            api_con = ApiCon(entered_api_url)
            api_con.load_cameras()
            self.api_window.destroy()
            if not self.main_opened:
                self.main_opened = True
                main = MainWindow()


class MainWindow:
    def __init__(self):

        self.window = tk.Tk()
        self.window.title("Gothenburg Traffic Cameras")

        main_window_width = 800
        main_window_height = 660
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        x = (ws/2) - (main_window_width/2)
        y = (hs/2) - (main_window_height/2)

        self.window.geometry('%dx%d+%d+%d' % (main_window_width, main_window_height, x, y))

        self.image_placeholder = tk.Label(text="Image goes here", background="black", width=680, height=550)
        self.image_placeholder.pack_forget()

        self.clicked = tk.StringVar()
        self.clicked.set("Select a camera")
        self.dropdown = tk.OptionMenu(self.window, self.clicked, *api_con.camera_dict.keys(), command=self.show_camera)
        self.dropdown.place(x=54, y=600)

        self.api_button = tk.Button(self.window, text="Manage API-key", height=1, width=13, command=self.manage_api_button)
        self.api_button.place(x=560, y=600)

        self.countdown_text = tk.StringVar()
        self.countdown_label = tk.Label(text="")
        self.countdown_label.place(x=54, y=560)

        self.close_button = tk.Button(self.window, text="Close", height=1, width=8, command=self.window.destroy)
        self.close_button.place(x=680, y=600)

        self.window.mainloop()

    def show_camera(self, x):
        choice = self.clicked.get()
        self.returned_image = api_con.get_camera_image(choice)
        self.image_data = self.returned_image.content
        self.image_data_processed = ImageTk.PhotoImage(Image.open(BytesIO(self.image_data)))
        self.image_placeholder.configure(image=self.image_data_processed)
        self.image_placeholder.pack()

        self.countdown(60)
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
            self.show_camera(self)

    def manage_api_button(self):
        api_window = ApiWindow(True)


def start_up():
    try:
        with open('api.txt', 'r') as f:
            f_content = f.readline()
            global api_con
            api_con = ApiCon(f_content)
            api_con.load_cameras()
            main = MainWindow()
    except:
        api_window = ApiWindow(False)


start_up()
