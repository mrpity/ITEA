import tkinter
import subprocess, os

def check_mem():
    first = ["free", "-h", "-t"]
    second = ["grep", "Total"]
    third = ["awk", "{print $3}"]
    fourth = ["awk", "-FG", "{print $1}"]
    p1 = subprocess.Popen(first, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(second, stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(third, stdin=p2.stdout, stdout=subprocess.PIPE)
    p4 = subprocess.Popen(fourth, stdin=p3.stdout, stdout=subprocess.PIPE)
    return float(p4.stdout.read())

def prepare_icon():

    try:
        current_mem = check_mem()
    except Exception as e:
        print("Cann't get float value from subprocess PIPE. ERROR: {}".format(e))

    root = tkinter.Tk()
    lab = tkinter.Label(root, text="WARNING!\nMemory limit: {}".format(current_mem), font="Arial 18")
    lab.pack()
    return root




if __name__ == '__main__':
    prepare_icon().mainloop()
    