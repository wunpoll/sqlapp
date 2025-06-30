import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def load_data():
    for i in tree.get_children():
        tree.delete(i)

    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="root", database="pet_shop")
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM petlust""")
        for i in cursor.fetchall():
            tree.insert("", tk.END, values=i)
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Ошибка", str(e))


def call_proc(win, lines):
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="root", database="pet_shop")
        cursor = conn.cursor()
        cursor.callproc("AddSell",(
            lines[0].get(),
            int(lines[1].get()),
            int(lines[2].get())
        ))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Процедура выполнена")
        win.destroy()
        load_data()
    except mysql.connector.Error as e:
        messagebox.showerror("Ошибка", str(e))


def open_proc():
    win = tk.Toplevel(root)
    labels = ["Введите дату продажи(YYYY-MM-DD HH:MM):", "Введите ID питомца:", "Введите ID клиента:"]
    lines = []
    for i, text in enumerate(labels):
        tk.Label(win, text=text).grid(row=i, column=0, sticky="e")
        e = tk.Entry(win)
        e.grid(row=i, column=1)
        lines.append(e)
    tk.Button(win, text="Выполнить", command= lambda: call_proc(win, lines)).grid(row=len(labels), column=0, columnspan=2)

root = tk.Tk()
root.title("Данные представление")

tree = ttk.Treeview(root, columns=("1", "2", "3", "4", "5", "6"), show="headings")

tree.heading("1", text="Кличка")
tree.heading("2", text="Цвет")
tree.heading("3", text="Возраст")
tree.heading("4", text="Цена")
tree.heading("5", text="Порода")
tree.heading("6", text="Категория")

tree.column("1", width=100)
tree.column("2", width=100)
tree.column("3", width=100)
tree.column("4", width=100)
tree.column("5", width=100)
tree.column("6", width=100)

tree.pack(expand=True, fill=tk.BOTH)
btn1 = tk.Button(root, text="Обновить", command=load_data)
btn2 = tk.Button(root, text="Выполнить", command=open_proc)

btn1.place(relx=0.4, rely=0.95, anchor=tk.CENTER)
btn2.place(relx=0.6, rely=0.95, anchor=tk.CENTER)

load_data()
root.mainloop()
