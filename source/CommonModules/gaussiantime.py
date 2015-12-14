import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft,fftshift,ifft
from scipy.signal import freqs
import scipy.signal as signal

sigma=10.0e-9
Ts = .5e-8
t = np.arange(0.0,1.0e-6,Ts)

x=(np.exp(-(t-0.5e-6)**2/(2*sigma)**2))
n = len(x)
#print len(t) 
k = np.arange(n)
T = n*Ts
frq = k/T
frq = frq[range(n/2)]

plt.subplot(3,1,1)
plt.plot(t,(x))

AQ = np.fft.fft(x)/n
A = AQ[range(n/2)]

#freq = np.fft.fftfreq(len(x))
plt.subplot(3,1,2)
plt.plot(frq,abs(A))

plt.subplot(3,1,3)

b = np.array([50.0*(10.0e-10),0.0])    #Numerato
a = np.array([50.0*(10.0e-10),1.0])    #Denominator
w, h = signal.freqs(b, a,worN=np.logspace(0, 8, 200))
M = [0.0]*len(AQ)
L = [0.0]*len(AQ)
for k in range(len(AQ)):
    #U =(A[k])
    V =((h[len(AQ)-k-1]))
    #M[k] = U
    L[k] = V
#print M
#M = np.asarray(M)
B = np.convolve(AQ,L)
M = np.asarray(B)
PO = M[range(n/2)]

plt.plot(frq,abs(A),w,np.abs(h),frq,abs(PO))
plt.figure()
plt.plot(frq,abs(A),frq,abs(PO))

N = np.fft.ifft(abs(M),200)
plt.figure()
plt.plot(t,x,t,500*abs(N))
plt.show()
