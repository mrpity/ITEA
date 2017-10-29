import tkinter
import subprocess
import time

''' GET TOTAL USED MEMORY FROM LOCALHOST'''
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

'''Check if memory using isn't high than 2.7 GB'''
def check_mem(memory):
    if memory >= 2.7:
        return True
    else:
        return False

''' Create GUI table'''
def prepare_root():
    try:
        current_mem = get_mem()
    except Exception as e:
        print("Cann't get float value from subprocess PIPE. ERROR: {}".format(e))

    if check_mem(current_mem):
        root = tkinter.Tk()
        lab = tkinter.Label(root, text="WARNING!\nMemory limit: {}GB".format(current_mem), font="Arial 18")
        lab.pack()
        return root

'''RUN app. check interval: 5 seconds'''
def main_loop():
    while True:
        try:
            prepare_root().mainloop()
        except Exception as e:
            print('ERROR: {}'.format(e))
        time.sleep(5)

if __name__ == '__main__':
    main_loop()
    