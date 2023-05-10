from socket import *
import threading
import time
import os
import schedule

data_host_name="192.168.0.36" #采集板的ip地址
data_port_num=60000  #端口号

clientsocket = socket(AF_INET, SOCK_STREAM)
clientsocket.bind((data_host_name,data_port_num))
clientsocket.listen(5)
print("sever is connected")
def tcplink(sock, addr):
    filename = "data.txt"
    if os.path.exists(filename):
        os.remove(filename)  # 若新文件名与系统中已经存在的文件重名，则删除系统中的文件
    new_file = open(filename, "a", encoding="utf-8")
    print('Accept new connection from %s:%s...' % addr)
    DATA=[]
    for i in range(0,5000):
        data = sock.recv(1024)
        DATA.append(data)
        if not data:
            break
        print(data)
    new_file.write(str(DATA))
    new_file.close()
    sock.close()
    print('Connection from %s:%s closed.' % addr)
while True:
    # 接受一个新连接:
    sock, addr = clientsocket.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()

