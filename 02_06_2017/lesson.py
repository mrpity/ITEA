
import tkinter as tk
from tkinter import messagebox
import time
import urllib.request
import threading



# def button_pressed():
#     #time.sleep(5)
#     l.config(text='Button pressed')
#
# def change_label():
#     l.config(text='Label')
#     l.after(3000, change_label)

# x = y = None


# def draw(event):
#     # print(event.x, event.y)
#     global x, y
#     if x is not None:
#         c.create_line(x, y, event.x + 1, event.y + 1, width=20)
#     x,y = event.x, event.y
#
# def pen_up(event):
#     global x,y
#     x = y = None


# def calc():
#     # try:
#     #     xv = int(x.get())
#     #     yv = int(y.get())
#     # except ValueError:
#     #     messagebox.showerror('Error', 'Invalid number')
#     #     return
#     try:
#         resv.set(xv.get() + yv.get())
#     except Exception:
#         messagebox.showerror('Error', 'Invalid number')
#
#     # res.config(text=str(resv))

is_interrupted = False
PG_LENGTH = 50
REQUESTS_COUNT = 20
comleted = 0

def run():
    b.config(text='Stop', command=stop)
    t = threading.Thread(target=get)
    t.start()


def stop():
    global is_interrupted
    is_interrupted = True

def get():
    global is_interrupted, comleted
    for i in range(REQUESTS_COUNT):
        if is_interrupted:
            break
        r = urllib.request.urlopen('http://itea.ua')
        print(len(r.read()))
        comleted = i
    is_interrupted = False
    b.config(text='Run', command=run)


def pg_update():
    spaces = int(PG_LENGTH/REQUESTS_COUNT * comleted)
    l.config(text=spaces*' ')
    l.after(1000, pg_update)


if __name__ == '__main__':
    root = tk.Tk()

    # xv = tk.IntVar()
    # yv = tk.IntVar()
    # resv = tk.IntVar()

    # root.geometry('200x300')
    # b = tk.Button(root, text="OK")
    # b.pack()

    # l1 = tk.Label(root, text='Label1', bg='blue', fg='yellow')
    # l1.pack(fill=tk.BOTH, expand=1)
    # l2 = tk.Label(root, text='Label1', bg='yellow', fg='blue')
    # l2.pack(fill=tk.BOTH, expand=1)

    root.geometry('600x500')
    # l = tk.Label(root, text='Label')
    # l.pack()
    # l.after(3000, change_label)
    # b = tk.Button(root, text='Ok', command=button_pressed)
    # b.pack()

    # c = tk.Canvas(root)
    # c.pack(fill=tk.BOTH, expand=1)
    # c.bind('<B1-Motion>', draw)
    # c.bind('<ButtonRelease-1>', pen_up)

    # l1 = tk.Label(root, text='X:')
    # l1.grid(row=0, column=0)
    # x = tk.Entry(root, textvariable=xv)
    # x.grid(row=0, column=1)
    #
    # l2 = tk.Label(root, text='Y:')
    # l2.grid(row=1, column=0)
    # y = tk.Entry(root, textvariable=yv)
    # y.grid(row=1, column=1)
    #
    # b = tk.Button(root, text='Calculate', command=calc)
    # b.grid(row=2, column=2)
    # res = tk.Label(root, text='Result', textvariable=resv)
    # res.grid(row=2, column=1)


    b = tk.Button(root, text='Run', command=run)
    b.pack()

    l = tk.Label(root, text='', bg='red')
    l.pack()

    l.after(1000, pg_update)

    root.mainloop()
