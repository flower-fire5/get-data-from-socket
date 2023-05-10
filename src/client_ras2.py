from socket import *
import threading
import time
import os
import schedule


"""
程序设计思路：
1.与服务器建立连接
2.向服务器发送“ras”指令
3.等待接收”collect“指令
4.接收到“collect”指令后开始运行采集数据程序
5.首先连接到单片机的sever
6.持续发送采集数据的指令
7.接收单片机的回应
8.接收到单片机的回应后开始recv数据
9.到时间停止接收
10.转发数据

"""


data_host_name="192.168.0.36" #采集板的ip地址
data_port_num=60000  #端口号

net_host_name="39.101.139.227" #公网的ip地址
net_port_num=30003  #端口号

def tcplink(sock, addr):
    filename = "data.txt"
    filename2 = "data2.txt"
    if os.path.exists(filename):
        os.remove(filename)  # 若新文件名与系统中已经存在的文件重名，则删除系统中的文件
    if os.path.exists(filename2):
        os.remove(filename2)  # 若新文件名与系统中已经存在的文件重名，则删除系统中的文件
    new_file = open(filename, "ab")
    # new_file2 = open(filename2, "a")
    print('Accept new connection from %s:%s...' % addr)
    DATA=[]
    start=time.time()
    k=0
    # new_file.write(time.time_ns())
    while True:
        data = sock.recv(1024)
        k=k+1
        DATA.append(data)
        if not data:
            break
        end=time.time()
        if (end-start)>60:
            break
    # start1 = time.time()
    # m=[]
    # for data in DATA:
    #     m = m + list(data)
    # end1 = time.time()
    # print(end1-start1)
    print(k)
    for everydata in DATA:
        new_file.write(everydata)
    # new_file2.write(str(DATA))
    new_file.close()
    # new_file2.close()
    sock.close()
    print('Connection from %s:%s closed.' % addr)
    return 123

def get_data(dataclientsocket):
    #从采集板获得数据。获得一分钟的数据
    # 将数据进行打包，存储为txt文件
    filename = "data.txt"
    if os.path.exists(filename):
        os.remove(filename)  # 若新文件名与系统中已经存在的文件重名，则删除系统中的文件
    new_file = open(filename, "ab")
    DATA = []
    start = time.time()
    k = 0
    while True:
        data = dataclientsocket.recv(1024)
        k=k+1
        DATA.append(data)
        if not data:
            break
        end=time.time()
        if (end-start)>61:
            break
    print(k)
    for everydata in DATA:
        new_file.write(everydata)
    new_file.close()
    print('all data have been received ')

def send_data(clientsocket):
    #将数据通过公网ip进行传输
    if clientsocket.recv(1024).decode("utf-8") == "begin to send data":
        print("--------开始发送数据---------------")
        filename = "data.txt"
        f = open(filename, "rb")
        rdata = f.read()
        clientsocket.send(rdata)
        print("---------发送完成-------------")
    clientsocket.close()

def run(clientsocket):
    print("----------开始采集数据---------------")
    # 连接采集板的ip地址
    dataclientsocket = socket(AF_INET, SOCK_STREAM)
    while True:
        try:
            dataclientsocket.connect((data_host_name, data_port_num))
            print("--------datasever is connected---------")
            dataclientsocket.send('$ASKD,060AB'.encode('ASCII')) #采集数据的命令格式“$ASKD,[采集时间][校验码]”
        except:
            print("connection with datasever is failed,please inspect sever and try again")
            time.sleep(1)
            continue
        if clientsocket.recv(1024).decode('utf-8') == "RECV":
            get_data(dataclientsocket)

    # 断开采集板的ip地址
    dataclientsocket.close()
    print("--------数据采集已经完成------------")
    print("-------------------------------")
    time.sleep(5)
    # 连接服务器的ip地址
    send_data(clientsocket)
    clientsocket.close()


if __name__ == "__main__":
    while True:
        clientsocket = socket(AF_INET, SOCK_STREAM)
        try:
            clientsocket.connect((net_host_name, net_port_num))  # 与服务器连接
            print("---------sever is connected--------")
            clientsocket.send('ras'.encode("utf-8"))
        except:
            print("connection is failed,please inspect sever and try again")
            time.sleep(1)
            continue
        if clientsocket.recv(1024).decode('utf-8') == "collect":
            run(clientsocket)
