# coding=utf-8
import tkinter as tk
import main
from tkinter import ttk

from project_hackathon.satelliteLTE import satellites_name, start, show_satellite

TEST_DB = satellites_name()


class windows(tk.Tk):
    """
    основное окно.
    пояснение за дальнейщие формулировки: контейнер - фрейм хранящий фреймы,
    фрейм - фрейм хранящий другие объекты (кнопки, списки...)
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # название приложения
        self.wm_title("SatPhoto")
        self.iconbitmap(r'C:\Users\zharyj.d\projects\project_hackathon\Земля.ico')

        # создание главного контейнера окна
        main_container = tk.Frame(self, height=self.winfo_height(), width=self.winfo_width(), borderwidth=1, relief='solid')
        main_container.pack(anchor='n', fill='x', padx=5, pady=5)

        # контейнер для левых фреймов
        left_container = tk.Frame(main_container, height=self.winfo_height()//2, width=self.winfo_width()//2, borderwidth=1, relief='solid')
        left_container.grid(sticky='e', row=0, column=0, ipadx=6, ipady=6, padx=4, pady=4)

        # контейнер для правых фреймов
        right_container = tk.Frame(main_container, height=400, width=600, borderwidth=1, relief='solid')
        right_container.grid(sticky='w', row=0, column=1, ipadx=6, ipady=6, padx=4, pady=4)

        # добавление фреймов в левый и правый контейнеры
        self.left_frames = {}
        self.add_frames(container=left_container, frames=(SatelliteCardFrame, ListInfoFrame),
                        direction_frame=self.left_frames)
        self.right_frames = {}
        self.add_frames(container=right_container, frames=(SatelliteInputFrame, CoordInputFrame),
                        direction_frame=self.right_frames)

        self.show_container(main_container)

    def add_frames(self, container, frames, direction_frame):
        """
        объединяет контейнер с фреймами в виде словаря и
        размещает фреймы через grid <-- понять для чего это мне нужно!!!!
        """
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in frames:
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            direction_frame[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    # вывод главного контейнера
    def show_container(self, container):
        container.tkraise()

    # вывод левого или правого контейнера
    def show_frame(self, cont, direction_frame):
        """его нужно переработать, чтоб он был не здесь а в классах-фреймах"""
        frame = direction_frame[cont]
        # raises the current frame to the top
        frame.tkraise()


class ListInfoFrame(tk.Frame):
    """
    фрейм выводящий список спутников
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # создаем список для вывода спутников
        data_var = tk.Variable(value=TEST_DB)
        self.lbox = tk.Listbox(self, listvariable=data_var,
                          width=40, height=17)
        self.lbox.yview_scroll(number=1, what="units")
        self.lbox.grid(sticky='w', row=0, column=0)

        # тут реализовывается переключение между "окнами"
        switch_window_button = tk.Button(
            self,
            text="посмотреть данные спутника",
            command=self.open_info
        )

        switch_window_button.grid(sticky='w', row=1, column=0)

    def open_info(self):
        """
        берет имя спутника из списка приложения
        """
        choosed_satellite = self.lbox.curselection()
        return show_satellite(TEST_DB[choosed_satellite[0]])


class SatelliteCardFrame(tk.Frame):
    """
    фрейм выводящий данные выбранного спутника
    """
    def __init__(self, parent, controller):

        self.closest_id = None

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="карточка выбранного спутника")
        label.grid(row=0, column=0)

        # временная кнопка для переключения между фреймами.
        # позже видоизменю переход через как-нибудь по-другому
        switch_window_button = tk.Button(
            self,
            text="Go to the Completion Screen",
            command=lambda: controller.show_frame(cont=ListInfoFrame,
                                                  direction_frame=controller.left_frames),
        )
        switch_window_button.grid(row=1, column=0)


class CoordInputFrame(tk.Frame):
    """
    фрейм с полем ввода координат и интерактивной картой
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)

        self.coord_entry = tk.Entry(self, width=50)
        self.coord_entry.grid(sticky='n', row=0, column=0)

        self.satellite = tk.Label(self, height=1, width=30, text="")
        self.satellite.grid(row=1, column=0)

        map = tk.Label(self, height=17, width=30, text="")
        map.grid(row=2, column=0)

        # тут реализовывается переключение между "окнами"
        switch_window_button = tk.Button(
            self,
            text="отправить координаты",
            command=self.input_coord
        )
        switch_window_button.grid(row=3, column=0)

    def input_coord(self):
        """
        ввод данных
        """
        coord = self.coord_entry.get()
        main.input_coord(coord)
        self.closest_id = start()

        self.output_satellite()

    def output_satellite(self):
        """
        выводит спутник в зависимости от координат
        """
        self.satellite.config(text=self.closest_id)

class SatelliteInputFrame(tk.Frame):
    """фрейм для добавления нового спутника в базу данных по введенным данным"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="ввод данных нового спутника")
        label.grid(row=0, column=0)

        switch_window_button = tk.Button(
            self,
            text="вернуться обратно",
            command=lambda: controller.show_frame(cont=CoordInputFrame,
                                                  direction_frame=controller.right_frames),
        )
        switch_window_button.grid(row=1, column=0)


if __name__ == "__main__":
    testObj = windows()
    # testObj.iconbitmap(r'C:\Users\zharyj.d\projects\project_hackathon\Земля.ico')

    # настройка размера и начального положения приложения
    w = testObj.winfo_screenwidth()
    h = testObj.winfo_screenheight()
    w = w // 2  # середина экрана
    h = h // 2
    w = w - 200  # смещение от середины
    h = h - 200
    testObj.geometry(f'600x400+{w}+{h}')
    testObj.resizable(width=False, height=False)

    testObj.mainloop()