from socket import *
import threading
import time


def trans(ras, local, BUFSIZ):
    ras.send("begin to send data".encode('utf-8'))
    flag = False
    if local.recv(BUFSIZ).decode('utf-8') == "ok":
        while True:
            try:
                data = ras.recv(BUFSIZ)
            except OSError:
                break
            if not data:
                ras.close()
                local.close()
            else:
                try:
                    if flag == False:
                        local.send("begin to receive data".encode('utf-8'))
                        flag = True
                    local.send(data)
                except OSError:
                    ras.close()
                    break



def find_local_computer(tcpCli):
    try:
        if tcpCli.recv(1024).decode('utf-8','ignore') == "master":
            tcpCli.send('receive master'.encode("utf-8"))
            return 1
    except ConnectionResetError as e:
        print(f"ConnectionResetError: {e}")
        tcpCli.close()
        return

if __name__ == '__main__':
    HOST = '0.0.0.0'
    POST = 30003
    ADDR = (HOST, POST)
    tcp = socket(AF_INET, SOCK_STREAM)
    tcp.bind(ADDR)
    tcp.listen(5)
    print("sever is ready")
    Users = []
    Local = []
    Addr_local = []
    Addr_users = []
    while True:
        tcpCli, addr = tcp.accept()
        if (find_local_computer(tcpCli) == 1) and (len(Local) == 0):
            Local.append(tcpCli)
            Addr_local.append(addr)
            print("接收端%s:%s 已经连接" %addr)
        else:
            Users.append(tcpCli)
            Addr_users.append(addr)
            print("发送端%s:%s 已经连接" % addr)
        if (len(Users) != 0) and (len(Local) !=0):      #暂时没有实现并行
            user = Users[-1]
            try:
                user.send("collect".encode('utf-8'))
                trans1 = threading.Thread(target=trans, args=(user, Local[0], 1024))
                trans1.start()
                Users=[]
                print("发送端%s:%s 已经退出" % Addr_users.pop(-1))
                Addr_users=[]
                Local=[]
                print("接收端%s:%s 已经退出\n" % Addr_local.pop(-1))
                Addr_local=[]
            except ConnectionResetError as e:
                print(f"ConnectionResetError: {e}")
