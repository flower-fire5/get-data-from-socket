from socket import *
import threading
import time
import os
import schedule
from load_data import load_data


data_host_name="192.168.0.36" #采集板的ip地址
data_port_num=60000  #端口号

net_host_name="39.101.139.227" #公网的ip地址
net_port_num=30004  #端口号

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

def get_data(dataseversocket):
    #从采集板获得数据。获得一分钟的数据
    # 将数据进行打包，存储为txt文件
    while True:
        sock, addr = dataseversocket.accept()
        # 创建新线程来处理TCP连接:
        k = tcplink(sock, addr)
        if k == 123:
            break
    pass

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
    dataseversocket = socket(AF_INET, SOCK_STREAM)
    dataseversocket.bind((data_host_name, data_port_num))
    dataseversocket.listen(5)
    print("--------datasever is connected---------")
    get_data(dataseversocket)
    # 断开采集板的ip地址
    dataseversocket.close()
    print("--------数据采集已经完成------------")
    print("-------------------------------")
    time.sleep(5)
    # 连接服务器的ip地址
    send_data(clientsocket)
    clientsocket.close()
    # load_data()
    # 断开采集板的ip地址

def run1():
    print('-------------------')

if __name__ == '__main__':
    while True:
        clientsocket = socket(AF_INET, SOCK_STREAM)
        try:
            clientsocket.connect((net_host_name, net_port_num))  # 与服务器连接
            print("---------sever is connected--------")
            clientsocket.send('ras'.encode("utf-8"))
        except:
            print("connection is failed,please inspect sever and try again")
            time.sleep(1)
        if clientsocket.recv(1024).decode('utf-8') == "collect":
            run(clientsocket)

