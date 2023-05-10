import threading
from socket import *
import time
import os
import schedule

#39.101.139.227
host_name="39.101.139.227" #服务器的ip地址
port_num=30003  #端口号


word = 'auto'
connect_flag = False

def load_data(file):
    with open(file,'rb') as f:
        if os.path.exists('result'+file):
            os.remove('result'+file)  # 若新文件名与系统中已经存在的文件重名，则删除系统中的文件
        r = open('result'+file,'a')
        data1=f.read()
        data1 = data1.hex()
        # num = len(data1)
        data2 = data1.split('a55a')
        k = 0
        m = 0
        for everydata in data2:
            if len(everydata)>2:
                everydata = everydata[:-2]
                for i in range(int(len(everydata)/4)):
                    k += 1
                    d =everydata[4*i:4*(i+1)]
                    dd = d[2:4]+d[0:2]
                    ten = int(dd,16)
                    if ten>32768:
                        data = -(65536-ten)/32768*10
                    else:
                        data = ten/32768*10
                    if k <= 3:
                        data = data * 150 * 2
                    elif 6 <= k <= 8:
                        data = data * 6.25 * 2
                    # num = float(ten) / 32768 * 10
                    # data = (ten-32767.5)/32767.5*10
                    # DATA.append(ten)
                    r.write(str(data))
                    r.write(',')
                    if k == 8:
                        t=file.split('.txt')
                        t = int(t[0])+28800000000000 - 60000000000+m*100000
                        r.write(str(t))
                        r.write('\n')
                        k=0
                        m=m+1
                        continue
        r.close()

def receive_data():
    global connect_flag
    global word
    while not connect_flag:
        clientsocket = socket(AF_INET, SOCK_STREAM)
        try:
            clientsocket.connect((host_name, port_num))  # 与服务器连接
            while True:
                clientsocket.send('master'.encode("utf-8"))
                if clientsocket.recv(1024).decode('utf-8') == "receive master":
                    break
            print("sever is connected")
        except:
            print("connection is failed,please inspect sever and try again")
            exit(0)
        clientsocket.send("ok".encode("utf-8"))

        while True:
            if clientsocket.recv(1024).decode('utf-8') == "begin to receive data":
                print("-" * 5 + "开始接收" + "-" * 5)
                filename = str(time.time_ns()) + '.txt'
                if os.path.exists(filename):
                    os.remove(filename)
                new_file = open(filename, "ab")
                while True:
                    rdata = clientsocket.recv(1024)  # 接收文件内容
                    if not rdata:
                        break

                    new_file.write(rdata)
                new_file.close()
                print("-" * 5 + "接收完成" + "-" * 5)
                connect_flag = True
                clientsocket.close()
                word = 'auto'
                break
        print("-" * 5 + "开始处理数据" + "-" * 5)
        load_data(filename)
        print("-" * 5 + "数据处理完毕" + "-" * 5)



def check_input():
    global word
    print('input something(manual)')
    word = input()
    if word == 'manual':
        print('yes,begin collect data immediately')
    else:
        print("this command isn't useful")

def run():
    while True:
        global word
        global connect_flag
        receive_data()
        connect_flag = False
        endtime = time.time() + 60.0*60  # 1minute
        while (time.time() < endtime):
            input_thread = threading.Thread(target=check_input)
            input_thread.start()
            input_thread.join(timeout=3600)
            if word == 'manual':
                break


if __name__ == '__main__':
    run()


