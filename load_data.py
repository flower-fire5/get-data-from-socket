import struct
import numpy as np
import time
import os
from binascii import a2b_hex
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
        # for
        # data1[0:4]
# load_data('1679369078168204100.txt')
# files = os.listdir()
# for file in files:
#     if '.txt' in file:
#         load_data(file)

#ffe0-->-32
