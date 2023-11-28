import requests,time,customtkinter,base64,hashlib,webbrowser,random,os,tkinter.messagebox,pyperclip
from threading import Thread
from itertools import cycle
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")
def commentCHK(*,username,comment,levelid,percentage,type):
        part1 = username + comment + levelid + str(percentage) + type + "xPT6iUrtws0J"
        return base64.b64encode(xor(hashlib.sha1(part1.encode()).hexdigest(),"29481").encode()).decode()
def xor(data, key):
        return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
def gjpEncrypt(data):
        return base64.b64encode(xor(data,"37526").encode()).decode()
def gjpDecrypt(data):
        return xor(base64.b64decode(data.encode()).decode(),"37526")
def getGJUsers(target):
    data={
        "secret":"Wmfd2893gb7",
        "str":target
    }
    request = requests.post("http://www.boomlings.com/database/getGJUsers20.php",data=data,headers={"User-Agent": ""}).text.split(":")[1::2]
    username = request[0]
    uuid = request[2]
    accountid = request[10]
    return (username,accountid,uuid)
def parseNONG(level,prefix):
    data = {
        "levelID": level,
        "secret": "Wmfd2893gb7"
    }
    req=requests.post("http://www.boomlings.com/database/downloadGJLevel22.php", data=data,headers={"User-Agent":""}).text.split(":")
    name=req[3]
    desc=base64.b64decode(req[5]).decode()
    link=desc.replace(prefix,"",1)
    return name,link
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        def startDownloader():
            Thread(target=dw).start()
        def dw():
          try:
            self.startButton.configure(state="disabled")
            self.progresslabel.configure(text="Loading link...")
            level=self.entry.get()
            info=parseNONG(level,self.entry2.get())
            self.progresslabel.configure(text="Downloading NONG...")
            self.ld1.configure(text=info[0])
            self.ld2.configure(text=info[1])
            link=info[1]
            splitted=link.split("/")
            fn=self.entry1.get()+"\\"+splitted[len(splitted)-1]
            with open(fn,"wb") as f:
                response = requests.get(link,stream=True)
                totalLength = response.headers.get("content-length")
                if totalLength is None:
                    f.write(response.content)
                else:
                    dl = 0
                    totalLength = int(totalLength)
                    for data in response.iter_content(chunk_size=4096):
                        dl += len(data)
                        f.write(data)
                        done = int(100*dl/totalLength)
                        self.progresslabel.configure(text="Downloading NONG... "+str(done)+"%")
                        self.progressbar.set(done/100)
            self.progresslabel.configure(text="Download successful!")
            time.sleep(2)
            self.progresslabel.configure(text="Nothing is downloading")
            self.startButton.configure(state="normal")
            self.progressbar.set(0)
            self.ld1.configure(text="Level Name")
            self.ld2.configure(text="NONG URL")
          except Exception as e:
            tkinter.messagebox.showerror(title="NumbersTada's NONG Downloader",message="NONG Downloader has crashed. Error: "+str(e))
            print(e)
            exit()
        self.title("NumbersTada's NONG Downloader")
        self.geometry(f"{900}x{450}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebarFrame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebarFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebarFrame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebarFrame, text="NumbersTada's\nNONG Downloader", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebarFrame, command=self.openWebsite, text="GitHub")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebarFrame, text="Theme:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appereanceMenu = customtkinter.CTkOptionMenu(self.sidebarFrame, values=["Light", "Dark", "System"],command=self.changeTheme)
        self.appereanceMenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scalingLabel = customtkinter.CTkLabel(self.sidebarFrame, text="Size:", anchor="w")
        self.scalingLabel.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scalingMenu = customtkinter.CTkOptionMenu(self.sidebarFrame, values=["80%", "90%", "100%", "110%", "120%"],command=self.changeScaling)
        self.scalingMenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Level ID")
        self.entry.grid(row=3, column=1, columnspan=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.startButton = customtkinter.CTkButton(master=self, text="Download", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=startDownloader)
        self.startButton.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Level Info")
        self.tabview.add("Settings")
        self.tabview.tab("Level Info").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Settings").grid_columnconfigure(0, weight=1)
        self.ld1 = customtkinter.CTkButton(self.tabview.tab("Level Info"), text="Level Name", state="disabled", fg_color="#303030", width=350)
        self.ld1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.ld2 = customtkinter.CTkButton(self.tabview.tab("Level Info"), text="NONG URL", state="disabled", fg_color="#303030", width=350)
        self.ld2.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.accidButton = customtkinter.CTkButton(self.tabview.tab("Level Info"), command=self.copy, text="Copy to clipboard")
        self.accidButton.grid(row=4, column=0, padx=20, pady=10)
        self.labelTab2 = customtkinter.CTkLabel(self.tabview.tab("Settings"), text="Specify the path to your Geometry Dash folder.")
        self.labelTab2.grid(row=0, column=0, padx=20, pady=20)
        self.entry1 = customtkinter.CTkEntry(self.tabview.tab("Settings"), placeholder_text="GD Folder Path",width=400)
        self.entry1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.entry1.insert(0,"C:\\Program Files (x86)\\Steam\\steamapps\\common\\Geometry Dash\\Resources\\")
        self.entry2 = customtkinter.CTkEntry(self.tabview.tab("Settings"), placeholder_text="NONG Prefix")
        self.entry2.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.entry2.insert(0,"NTNONG:")
        self.progressbarFrame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.progressbarFrame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.progressbarFrame.grid_columnconfigure(0, weight=1)
        self.progressbarFrame.grid_rowconfigure(4, weight=1)
        self.progresslabel = customtkinter.CTkLabel(self.progressbarFrame, font=customtkinter.CTkFont(size=12), text="Nothing is downloading")
        self.progresslabel.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.progressbar = customtkinter.CTkProgressBar(self.progressbarFrame)
        self.progressbar.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.checkboxFrame = customtkinter.CTkFrame(self)
        self.checkboxFrame.grid(row=0, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.autoFolder = customtkinter.CTkCheckBox(master=self.checkboxFrame, text="AutoFolder (WIP)", state="disabled")
        self.autoFolder.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.autoID = customtkinter.CTkCheckBox(master=self.checkboxFrame, text="AutoID (WIP)", state="disabled")
        self.autoID.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")

        self.appereanceMenu.set("Dark")
        self.scalingMenu.set("100%")
        self.progressbar.set(0)
    def copy(self):
        pyperclip.copy(self.ld2.cget("text"))
    def changeTheme(self, newMode: str):
        if newMode == "Light":
            customtkinter.set_appearance_mode("light")
        if newMode == "Dark":
            customtkinter.set_appearance_mode("dark")
        if newMode == "System":
            customtkinter.set_appearance_mode("system")
    def changeScaling(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    def openWebsite(self):
        webbrowser.open("https://github.com/NumbersTada/NONG")
if __name__ == "__main__":
    app = App()
    app.mainloop()
