from re import I
import tkinter as tk

class BasePopOut(tk.Toplevel):
    def __init__(self, mainapp: tk.Tk, title:str="pop_out", geometry:str="300x100"):
        super().__init__(mainapp)
        self.title(title)
        self.geometry(geometry)
        self.update()
    
class PopOutInfo(BasePopOut):
    def __init__(self, mainapp: tk.Tk, title: str = "info", geometry: str = "200x100"):
        super().__init__(mainapp, title, geometry)
        self.info_var = tk.StringVar(value='info...')
        self.info_label= tk.Label(self, textvariable=self.info_var)
        self.looping = False
        self.mainapp = mainapp
        self._Layout()
        self.update()
        # self.withdraw()

    def _Layout(self):
        return self.info_label.place(relx=0.4, rely=0.4)

    def pop(self):
        # self.deiconify()
        self.looping = True
        self.pop_loop()
        return self

    def pop_loop(self, basetxt:str="連線中", sep:str='.', cnt:int=0):
        if self.looping is False:
            return
        cnt = 0 if cnt > 5 else cnt+1
        print(f"\r{basetxt+(sep*cnt)}", cnt, end='')
        self.info_var.set(f"{basetxt+(sep*cnt)}")
        self.update()
        self.mainapp.after(100, lambda: self.pop_loop(basetxt, sep, cnt))

    def update_info(self, txt:str):
        self.looping = False
        self.info_var.set(txt)
        return self.update()

    def destroy(self) -> None:
        self.looping = False
        return super().destroy()