import tkinter as tk
import pyautogui
from math import cos, sin, radians, atan2, pi, dist
import threading
import time
import pyperclip
import clipboard
import os
import sys
import webbrowser
import requests
import json
import mouse


class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.version = "v1.0.0"
        self.title("휠메뉴 " + self.version)
        self.geometry("400x570")
        self.resizable(False, False)
        self.file = "C:\\ProDays\\PDRadialMenu.json"

        self.set_dir()
        self.draw_menu()

        thread_kb = threading.Thread(target=self.msinput)
        thread_kb.start()

    def set_dir(self):
        try:
            os.chdir(sys._MEIPASS)
        except:
            os.chdir(os.getcwd())
        self.iconbitmap(default="icon.ico")

    def version_check(self):
        try:
            response = requests.get(
                "https://api.github.com/repos/pro-days/radialmenu/releases/latest"
            )
            checked_version = response.json()["name"]
            if response.status_code == 200:
                if self.version == checked_version:
                    self.update_label.config(text="최신버전 O", fg="green")
                else:
                    update_url = response.json()["html_url"]
                    self.update_label.bind(
                        "<Button-1>", lambda event: webbrowser.open_new(update_url)
                    )
                    self.update_label.config(text="최신버전 X", fg="red")
            else:
                self.update_label.config(text="업데이트 확인 실패", fg="red")
        except:
            self.update_label.config(text="업데이트 확인 실패", fg="red")

    def draw_menu(self):
        frame_navigator = tk.Frame(self, width=400, height=45)
        frame_navigator.pack_propagate(False)
        frame_navigator.pack()

        # 업데이트 체크
        frame_update = tk.Frame(frame_navigator, width=200, height=45)
        frame_update.pack_propagate(False)
        frame_update.place(x=0, y=0)

        self.update_label = tk.Label(
            frame_update,
            text="업데이트 확인중",
            fg="gray",
            relief="solid",
            font=("맑은 고딕", 12, "bold"),
            width=30,
            height=20,
            borderwidth=1.5,
        )
        self.update_label.pack()

        thread_version = threading.Thread(target=self.version_check)
        thread_version.start()

        # 설명 링크
        frame_descr = tk.Frame(frame_navigator, width=200, height=45)
        frame_descr.pack_propagate(False)
        frame_descr.place(x=200, y=0)

        descr_label = tk.Label(
            frame_descr,
            text="설명 확인하기",
            fg="blue",
            borderwidth=1.5,
            relief="solid",
            font=("맑은 고딕", 12, "bold"),
            width=30,
            height=20,
        )
        descr_label.pack()
        descr_label.bind(
            "<Button-1>",
            lambda event: webbrowser.open_new(
                "https://github.com/Pro-Days/radialmenu#readme"
            ),
        )

        frame_opts = tk.Frame(self, width=400, height=390)
        frame_opts.pack_propagate(False)
        frame_opts.pack(pady=20)

        self.opts_var = [tk.StringVar() for i in range(8)]
        opts = self.dataload()
        opts_entry = [
            tk.Entry(
                frame_opts,
                textvariable=self.opts_var[i],
                fg="black",
                borderwidth=1,
                relief="solid",
                justify="center",
                font=("맑은 고딕", 10),
            )
            for i in range(8)
        ]

        for i, j in enumerate(opts_entry):
            j.place(x=25, y=i * 50, width=350, height=40)
            self.opts_var[i].set(opts[i])
            j.configure(bg="#ffffff")

        frame_save = tk.Frame(self, width=100, height=50)
        frame_save.pack_propagate(False)
        frame_save.pack(pady=0)

        save_bt = tk.Button(
            frame_save,
            text="저장",
            width=100,
            borderwidth=1,
            relief="solid",
            font=("맑은 고딕", 10),
            bg="white",
            anchor="center",
            command=self.datasave,
        )
        save_bt.pack()

        tk.Label(
            self,
            text="제작자: 데이즈 | 디스코드: pro_days",
            relief=tk.SUNKEN,
            font=("맑은 고딕", 10),
            anchor=tk.W,
            bd=1,
        ).pack(side=tk.BOTTOM, fill=tk.X)

    def dataload(self):
        if os.path.isfile(self.file):
            try:
                with open(self.file, "r") as f:
                    json_object = json.load(f)

                    opts = json_object["Opts"]
            except:
                opts = [
                    "Opt 1",
                    "Opt 2",
                    "Opt 3",
                    "Opt 4",
                    "Opt 5",
                    "Opt 6",
                    "Opt 7",
                    "Opt 8",
                ]
                self.datamake()
        else:
            opts = [
                "Opt 1",
                "Opt 2",
                "Opt 3",
                "Opt 4",
                "Opt 5",
                "Opt 6",
                "Opt 7",
                "Opt 8",
            ]
            self.datamake()
        return opts

    def datamake(self):
        json_object = {
            "Opts": [
                "Opt 1",
                "Opt 2",
                "Opt 3",
                "Opt 4",
                "Opt 5",
                "Opt 6",
                "Opt 7",
                "Opt 8",
            ]
        }

        if not os.path.isdir("C:\\ProDays"):
            os.mkdir("C:\\ProDays")
        with open(self.file, "w") as f:
            json.dump(json_object, f)

    def datasave(self):
        opts = [self.opts_var[i].get() for i in range(8)]
        with open(self.file, "r") as f:
            json_object = json.load(f)

        json_object["Opts"] = opts

        with open(self.file, "w") as f:
            json.dump(json_object, f)

    def msinput(self):
        while True:
            if mouse.is_pressed("middle"):
                self.activate()
            time.sleep(0.0166)

    def activate(self):
        opts = [self.opts_var[i].get() for i in range(8)]
        self.app = RadialMenu(opts)


class RadialMenu(tk.Tk):
    def __init__(self, data):
        self.x, self.y = pyautogui.position()
        tk.Tk.__init__(self)
        self.fore = pyautogui.getActiveWindow()
        size = round((self.winfo_screenwidth() + self.winfo_screenheight()) * 0.15)
        self.title("Radial Menu")
        self.geometry(
            f"{size}x{size}+{self.x-round(0.5*size)}+{self.y-round(0.5*size)}"
        )
        self.attributes("-alpha", 0.7)
        self.overrideredirect(True)
        self.wm_attributes("-transparentcolor", "#fffffe")
        self.configure(background="#fffffe")
        self.wm_attributes("-topmost", True)

        self.menu_items = data
        self.state = True

        self.canvas = tk.Canvas(
            self,
            width=size,
            height=size,
            bg="#fffffe",
            bd=0,
            highlightthickness=0,
        )
        self.canvas.pack()

        self.center = round(size * 0.5)
        self.radius = round(size * 0.5)

        self.draw_menu()
        thread_activate = threading.Thread(target=self.msinput, daemon=True)
        thread_activate.start()
        t = threading.Thread(target=self.drag, daemon=True)
        t.start()

        self.mainloop()

    def msinput(self):
        while mouse.is_pressed("middle"):
            time.sleep(0.0166)
        self.activate()

    def draw_menu(self):
        self.canvas.create_oval(
            self.center - self.radius,
            self.center - self.radius,
            self.center + self.radius,
            self.center + self.radius,
            outline="black",
            width=2,
            fill="#aaaaaa",
        )

        angle = 360 / len(self.menu_items)
        self.texts = []
        for i, item in enumerate(self.menu_items):
            theta = radians(i * angle)
            x = self.center + int(self.radius * cos(theta) * 0.7)
            y = self.center + int(self.radius * sin(theta) * 0.7)
            self.texts.append(
                self.canvas.create_text(
                    x, y, text=item[:10], font=("Arial", 10), tags=("menu_item",)
                )
            )
        angle = 360 / len(self.menu_items)
        for i in range(len(self.menu_items)):
            theta = radians(i * angle + 22.5)
            self.canvas.create_line(
                self.center,
                self.center,
                self.center + int(self.radius * cos(theta)),
                self.center + int(self.radius * sin(theta)),
            )

        self.canvas.create_oval(
            self.center - self.radius * 0.2,
            self.center - self.radius * 0.2,
            self.center + self.radius * 0.2,
            self.center + self.radius * 0.2,
            outline="black",
            width=2,
            fill="#aaaaaa",
        )

    def drag(self):
        while self.state:
            try:
                mx, my = pyautogui.position()
                mx -= self.x
                my -= self.y

                distance = dist([0, 0], [mx, my])
                rad = atan2(my, mx)
                if distance <= self.radius * 0.2:
                    self.pos = 0
                elif rad == 0:
                    self.pos = 0
                elif 0 < rad <= pi * 0.125:
                    self.pos = 1
                elif pi * 0.125 <= rad <= pi * 0.375:
                    self.pos = 2
                elif pi * 0.375 <= rad <= pi * 0.625:
                    self.pos = 3
                elif pi * 0.625 <= rad <= pi * 0.875:
                    self.pos = 4
                elif pi * 0.875 <= rad:
                    self.pos = 5
                elif rad <= pi * -0.875:
                    self.pos = 5
                elif pi * -0.875 <= rad <= pi * -0.625:
                    self.pos = 6
                elif pi * -0.625 <= rad <= pi * -0.375:
                    self.pos = 7
                elif pi * -0.375 <= rad <= pi * -0.125:
                    self.pos = 8
                elif pi * -0.125 <= rad <= 0:
                    self.pos = 1

                item = self.texts[self.pos - 1]
                for i in self.texts:
                    if i != item:
                        self.canvas.itemconfig(i, fill="black")
                        self.canvas.itemconfig(i, font=("Arial", 10))
                if self.pos != 0:
                    # print(self.canvas.itemcget(item, "text"))
                    self.canvas.itemconfig(item, fill="red")
                    self.canvas.itemconfig(item, font=("Arial", 15, "bold"))
            except:
                break

            time.sleep(0.05)
            if not self.state:
                break

    def activate(self):
        if self.pos != 0:
            self.fore.activate()
            pre = clipboard.paste()
            pyperclip.copy(self.menu_items[self.pos - 1])
            pyautogui.hotkey("ctrl", "v")
            pyperclip.copy(pre)
            self.state = False
        self.destroy()


if __name__ == "__main__":
    app = Window()
    app.mainloop()
