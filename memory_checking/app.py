import tkinter
import subprocess, os
import time

def get_mem():
    first = ["free", "-h", "-t"]
    second = ["grep", "Total"]
    third = ["awk", "{print $3}"]
    fourth = ["awk", "-FG", "{print $1}"]
    p1 = subprocess.Popen(first, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(second, stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(third, stdin=p2.stdout, stdout=subprocess.PIPE)
    p4 = subprocess.Popen(fourth, stdin=p3.stdout, stdout=subprocess.PIPE)
    return float(p4.stdout.read())

def check_mem(memory):
    if memory >= 2.6:
        return True
    else:
        return False

def prepare_root():

    try:
        current_mem = get_mem()
    except Exception as e:
        print("Cann't get float value from subprocess PIPE. ERROR: {}".format(e))

    if check_mem(current_mem):
        root = tkinter.Tk()
        lab = tkinter.Label(root, text="WARNING!\nMemory limit: {}GB".format(current_mem), font="Arial 18")
        lab.pack()
    else:
        root = tkinter.Tk()
        lab = tkinter.Label(root, text="OK!\nMemory limit: {}GB".format(current_mem), font="Arial 18")
        lab.pack()
    return root

def main_loop():
    while True:
        prepare_root().mainloop()
        time.sleep(5)

if __name__ == '__main__':
    main_loop()
    