import os
import numpy as np
import config
import matplotlib.pyplot as plt

heaFile = "100.hea"
datFile = "100.dat"
atrFile = "100.atr"
SAMPLES2READ = 650

f=open(os.path.join(config.dataPath, heaFile),"r")
z=f.readline().split()
nosig,sfreq=int(z[1]),int(z[2])

dformat,gain,bitres,zerovalue,firstvalue=[],[],[],[],[]
for i in range(nosig):
    z=f.readline().split()
    dformat.append(int(z[1]))
    gain.append(int(z[2]))
    bitres.append(int(z[3]))
    zerovalue.append(int(z[4]))
    firstvalue.append(int(z[5]))
f.close()

rawData = open(os.path.join(config.dataPath, datFile),"rb")
byte = rawData.read()
rawData.close()

A_init=np.frombuffer(byte,dtype=np.uint8)
A_shape0=int(A_init.shape[0]/3)
A=A_init.reshape(A_shape0,3)[:SAMPLES2READ]

M=np.zeros((SAMPLES2READ,2))     # Create Storage for Result

M2H=A[:,1]>>4     # High 4 Bit
M1H=A[:,1]&15     # Lower 4 Bit

PRL=(A[:,1]&8)*(2**9) # Sign-Bit, Highest Bit from the Lower  4 Bit, Move Left 9    ，向左移九位，等于乘2^9
PRR=(A[:,1]&128)<<5   # Sign-Bit, Highest Bit from the Higher 4 Bit, Move Left 5    取出字节高四位中最高位，向左移五位

M1H = M1H*(2**8)
M2H = M2H*(2**8)

M[:,0]=A[:,0]+M1H-PRL
M[:,1]=A[:,2]+M2H-PRR

if ((M[1,:]!=firstvalue).any()):
    print("inconsistency in the first bit values")

if nosig==2:
    M[:, 0] = (M[:, 0] - zerovalue[0]) / gain[0]
    M[:, 1] = (M[:, 1] - zerovalue[1]) / gain[1]
    TIME=np.linspace(0,SAMPLES2READ-1,SAMPLES2READ)/sfreq
elif nosig==1:
    M2=[]
    M[:, 0] = M[:, 0] - zerovalue[0]
    M[:, 1] = M[:, 1] - zerovalue[1]
    for i in range(M.shape[0]):
        M2.append(M[:,0][i])
        M2.append(M[:,1][i])
    M2.append(0)
    del M2[0]
    M2=np.array(M2)/gain[0]
    TIME=np.linspace(0,2*SAMPLES2READ-1,2*SAMPLES2READ)/sfreq
else:
    print("Sorting algorithm for more than 2 signals not programmed yet!")

####################读取atr文件######################
f=open(os.path.join(config.dataPath, atrFile),"rb")     #主要是读取ATR文件中各周期数据并在之后打印在图中
byte=f.read()
f.close()

print(byte[:20])

A_init=np.frombuffer(byte,dtype=np.uint8)
A_shape0=int(A_init.shape[0]/2)
A=A_init.reshape(A_shape0,2)

print(A_init)

ANNOT,ATRTIME=[],[]
i=0
while i < A.shape[0]:
    annoth=A[i,1]>>2
    if annoth==59:
        ANNOT.append(A[i+3,1]>>2)
        ATRTIME.append(A[i+2,0]+A[i+2,1]*(2**8)+A[i+1,0]*(2**16)+A[i+1,1]*(2**24))
        i+=3
    elif annoth==60:pass
    elif annoth==61:pass
    elif annoth==62:pass
    elif annoth==63:
        hilfe=(A[i,1]&3)*(2**8)+A[i,0]
        hilfe=hilfe+hilfe%2
        i+=int(hilfe/2)
    else:
        ATRTIME.append((A[i,1]&3)*(2**8)+A[i,0])
        ANNOT.append(A[i,1]>>2)
    i+=1

del ANNOT[len(ANNOT)-1]
del ATRTIME[len(ATRTIME)-1]

ATRTIME=np.array(ATRTIME)
ATRTIME=np.cumsum(ATRTIME)/sfreq

ind=np.where(ATRTIME<=TIME[-1])[0]
ATRTIMED=ATRTIME[ind]

ANNOT=np.round(ANNOT)
ANNOTD=ANNOT[ind]

#####################显示ECG####################
plt.plot(TIME,M[:,0],linewidth="0.5",c="r")
if nosig==2:
    plt.plot(TIME, M[:, 1], linewidth="0.5", c="b")
for i in range(len(ATRTIMED)):
    plt.text(ATRTIMED[i],0,str(ANNOTD[i]))
plt.xlim(TIME[0],TIME[-1])
plt.xlabel("Time / s")
plt.ylabel("Votage / mV")
plt.title("ECG signal ")
plt.show()
