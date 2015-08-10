import numpy as np
import matplotlib.pyplot as plt
   
xpos = np.random.normal(0,0.005,1e4)
xder = np.random.normal(0,0.01,1e4)
ypos = np.random.normal(0,0.003,1e4)
yder = np.random.normal(0,0.02,1e4)
zpos = np.random.normal(0,10,1e4)
mom = np.random.normal(0,0.001,1e4)
    
#count, bins, ignored = plt.hist(xpos, 30)
plt.figure(0)
plt.plot(xpos,ypos,'bo')
plt.figure(1)
plt.plot(xpos,xder,'ro')
plt.show()