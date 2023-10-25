import tkinter as tk
from tkinter import ttk


TEST_DB = ['sp1', 'sp2', 'sp3', 'sp4', 'sp5', 'sp6', 'sp7']


class windows(tk.Tk):
    """
    основное окно.
    пояснение за дальнейщие формулировки: контейнер - фрейм хранящий фреймы,
    фрейм - фрейм хранящий другие объекты (кнопки, списки...)
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # название приложения
        self.wm_title("Введите название")

        # создание главного контейнера окна
        main_container = tk.Frame(self, height=400, width=800)
        main_container.pack()

        # контейнер для левых фреймов
        left_container = tk.Frame(main_container, height=400, width=600)
        left_container.pack(side="left", fill="both", expand=True)

        # контейнер для правых фреймов
        right_container = tk.Frame(main_container, height=400, width=600)
        right_container.pack(side="right", fill="both", expand=True)

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
            frame.grid(row=0, column=0, sticky="nsew")  # нужен ли мне он?

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
        lbox = tk.Listbox(self, width=15, height=8)
        lbox.pack()

        # ввод данных из базы данных в список приложения
        for i in TEST_DB:
            lbox.insert(0, i)

        # тут реализовывается переключение между "окнами"
        switch_window_button = tk.Button(
            self,
            text="Go to the Side Page",
            command=lambda: controller.show_frame(cont=SatelliteCardFrame,
                                                  direction_frame=controller.left_frames),
        )
        switch_window_button.pack(side="bottom", fill=tk.X)


class SatelliteCardFrame(tk.Frame):
    """
    фрейм выводящий данные выбранного спутника
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="карточка выбранного спутника")
        label.pack(padx=10, pady=10)

        # временная кнопка для переключения между фреймами.
        # позже видоизменю переход через как-нибудь по-другому
        switch_window_button = tk.Button(
            self,
            text="Go to the Completion Screen",
            command=lambda: controller.show_frame(cont=ListInfoFrame,
                                                  direction_frame=controller.left_frames),
        )
        switch_window_button.pack(side="bottom", fill=tk.X)


class CoordInputFrame(tk.Frame):
    """
    фрейм с полем ввода координат и интерактивной картой
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="блок из поля ввода и карты")
        label.pack(padx=10, pady=10)

        # тут реализовывается переключение между "окнами"
        switch_window_button = tk.Button(
            self,
            text="Go to the Side Page",
            command=lambda: controller.show_frame(cont=SatelliteInputFrame,
                                                  direction_frame=controller.right_frames),
        )
        switch_window_button.pack(side="bottom", fill=tk.X)


class SatelliteInputFrame(tk.Frame):
    """фрейм для добавления нового спутника в базу данных по введенным данным"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="ввод данных нового спутника")
        label.pack(padx=10, pady=10)

        switch_window_button = tk.Button(
            self,
            text="Go to the Completion Screen",
            command=lambda: controller.show_frame(cont=CoordInputFrame,
                                                  direction_frame=controller.right_frames),
        )
        switch_window_button.pack(side="bottom", fill=tk.X)


if __name__ == "__main__":
    testObj = windows()
    testObj.mainloop()
