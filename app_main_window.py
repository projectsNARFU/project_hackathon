from tkinter import *
from tkinter import ttk

test_db = [1, 2, 3]

# начальная настройка приложения
root = Tk()
root.title("Введите название")
root.geometry("660x450")
style = ttk.Style()

#
frame = Frame(root, padx=10, pady=10)
frame.pack(expand=True)

root.mainloop()

if __name__ == "__main__":
    pass