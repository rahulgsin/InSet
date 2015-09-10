import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import struct as breader
import scipy.fftpack as FFT
from scipy import stats
#from matplotlib2tikz import save as tikz_save
from matplotlib import rc

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

simulation = 1
coast = 0
bunched = 1
fit_points = 1000
baseline1 = 0
baseline2 = 0
baseline3 = 0
baseline4 = 0
# fourier_points = 2048
# fc=212600
# T = 1/fc
# frequency_axis = np.linspace(0.0, 1.0/(2.0*T), fourier_points/2)

### File reading

if simulation == 0:
    file_path = "GS07DX_Raw_bin_2012-3-30_16-57-26.bin"
    plane = 0
    start_point = 20000000
    num_points = 200000
    header_length = 32
    num_channels = 4
    
    file_id = open(file_path,'rb')
    data = file_id.read(header_length)
    header = data.decode('utf-8')
    print (header)
    file_id.seek(0,2)
    size = file_id.tell()
    print ("number of data samples per plate is", (size/16*4))
    total_points = size
    if num_points*8+start_point > size:
        print("Less points is the file than asked, exiting ....")
        exit(0)
    raw_data = np.zeros((num_channels,num_points))
    ver_sum_raw_data = np.zeros((num_points))
    ver_diff_raw_data = np.zeros((num_points))
    hor_sum_raw_data = np.zeros((num_points))
    hor_diff_raw_data = np.zeros((num_points))
    noise1 = np.zeros((num_points))
    noise2 = np.zeros((num_points))
    noise3 = np.zeros((num_points))
    noise4 = np.zeros((num_points))
    file_id.seek(header_length+start_point*8,0) 
    total_raw_data=file_id.read(8*num_points)
    file_id.close()
    for i in range(num_points):
        plate = breader.unpack('hhhh',total_raw_data[2*i*num_channels:2*(i+1)*num_channels])
        raw_data[0,i]=plate[0]
        raw_data[1,i]=plate[1]
        raw_data[2,i]=plate[2]
        raw_data[3,i]=plate[3]
        ver_sum_raw_data[i] = raw_data[0,i] + raw_data[1,i]
    #     ver_diff_raw_data[i] = raw_data[0,i] - raw_data[1,i]
    #     hor_sum_raw_data[i] = raw_data[2,i] + raw_data[3,i]
    #     hor_diff_raw_data[i] = raw_data[3,i] - raw_data[2,i]







# File reading of simulated data
if simulation == 1:
    filename = "x1_ext.data"   
    plane = 0
    start_point = 1
    num_points = 2500001
    num_channels = 4
    Turns =  np.zeros((num_points))
    hor_diff_raw_data =  np.zeros((num_points))
    hor_sum_raw_data =  np.zeros((num_points))
    ver_diff_raw_data =  np.zeros((num_points))
    ver_sum_raw_data =  np.zeros((num_points))
    noise1 = np.zeros((num_points))
    noise2 = np.zeros((num_points))
    noise3 = np.zeros((num_points))
    noise4 = np.zeros((num_points))
    noise1 = np.random.normal(0, 0.0000001,num_points)
    noise2 = np.random.normal(0, 0.0000001,num_points)
    noise3 = np.random.normal(0, 0.0000001,num_points)
    noise4 = np.random.normal(0, 0.0000001,num_points)
    raw_data =  np.zeros((num_channels,num_points))
    plot_window = np.ones((num_points))*(-500)
    
    
    amplify = 1
    # For coasting
    if coast == 1:
        amplify = 9*1e3*np.sqrt(2*1e6)*73*1.6*1e-19*2*1e6*10 # Sim_particles*rest_particles*e*Z*rev_band*Zt
    # For bunched
    if bunched == 1:
        amplify = 8192/10
        #amplify = 9*1e3*1e6*73*1.6*1e-19*2*1e6*10
    
    
    if os.path.isfile(filename) == False:
        print('Specified file' +filename+ 'to read the beam parameters does not exist, exiting ...')
        exit()
    else:
        # Read and ignore header lines
        f = open(filename,'r')
        f.seek(0,2)
        size = f.tell()
        print ("size", size)
        f.seek(0,0)
        i=0
        # Loop over lines and extract variables of interest
        for line in f:
            line = line.strip()
            columns = line.split()
            #print (columns[1])
            Turns[i] = float(columns[0])
            raw_data[2,i] = amplify*float(columns[1])
            i=i+1
        f.close()
    filename = "x2_ext.data"  
    if os.path.isfile(filename) == False:
        print('Specified file' +filename+ 'to read the beam parameters does not exist, exiting ...')
        exit()
    else:
        # Read and ignore header lines
        f = open(filename,'r')
        f.seek(0,2)
        size = f.tell()
        print ("size", size)
        f.seek(0,0)
        i=0
        # Loop over lines and extract variables of interest
        for line in f:
            line = line.strip()
            columns = line.split()
            #print (columns[1])
            raw_data[3,i] = amplify*float(columns[1])
            i=i+1
        f.close()
    filename = "y1_ext.data"  
    if os.path.isfile(filename) == False:
        print('Specified file' +filename+ 'to read the beam parameters does not exist, exiting ...')
        exit()
    else:
        # Read and ignore header lines
        f = open(filename,'r')
        f.seek(0,2)
        size = f.tell()
        print ("size", size)
        f.seek(0,0)
        i=0
        # Loop over lines and extract variables of interest
        for line in f:
            line = line.strip()
            columns = line.split()
            #print (columns[1])
            raw_data[0,i] = amplify*float(columns[1])
            i=i+1
        f.close()
    filename = "y2_ext.data"   
    if os.path.isfile(filename) == False:
        print('Specified file' +filename+ 'to read the beam parameters does not exist, exiting ...')
        exit()
    else:
        # Read and ignore header lines
        f = open(filename,'r')
        f.seek(0,2)
        size = f.tell()
        print ("size", size)
        f.seek(0,0)
        i=0
        # Loop over lines and extract variables of interest
        for line in f:
            line = line.strip()
            columns = line.split()
            #print (columns[1])
            Turns[i] = float(columns[0])
            raw_data[1,i] = amplify*float(columns[1])
            i=i+1
        f.close()
    
    ver_sum_raw_data = raw_data[0] + raw_data[1]






 
 ### Bunch detection
# Detection magic numbers
tmin = -800
threshold11 = 1/3*tmin
threshold12 = -1/3*tmin
threshold21 = -1/3*tmin
threshold22 = 1/3*tmin
wait_t1 = 10 # bunch windows smaller than 10 points are avoided or spikes are avoided
wait_t2= 20 # gaps smaller than 10 points and spikes between bunches are avoided
plot_start = 50
plot_stop = 300000
start = 100
plot_window = np.ones((num_points))*(-500)

window_length_guess = 50
t1=np.zeros((np.ceil(num_points/window_length_guess))) # Wont work for bunch lengths shorter than window_length_guess
t2=np.zeros((np.ceil(num_points/window_length_guess)))
beam_baseline1=np.zeros((np.ceil(num_points/window_length_guess)))
beam_baseline2=np.zeros((np.ceil(num_points/window_length_guess)))
beam_baseline3=np.zeros((np.ceil(num_points/window_length_guess)))
beam_baseline4=np.zeros((np.ceil(num_points/window_length_guess)))
bunch_frequency= np.zeros((np.ceil(num_points/window_length_guess)))
count_t1 = 0
count_t2 = 0
find_t11 = 1
find_t12 = 0
find_t21 = 0
find_t22 = 0

started = 0
new_bunch = 1
# find minimum
tmin= np.min(ver_sum_raw_data[1:1000])
beam_baseline1[0] = np.min(raw_data[0,1:1000])
beam_baseline2[0] = np.min(raw_data[1,1:1000])
beam_baseline3[0] = np.min(raw_data[2,1:1000])
beam_baseline4[0] = np.min(raw_data[3,1:1000])
for point_num in range(num_points):

    if (new_bunch == 1 and ver_sum_raw_data[point_num] < 0.8*tmin):
        if ver_sum_raw_data[point_num] < tmin:
            tmin = ver_sum_raw_data[point_num]
        threshold11 = 1/3*tmin
        threshold12 = -1/3*tmin
        threshold21 = -1/3*tmin
        threshold22 = 1/3*tmin
        beam_baseline1[count_t1] = (beam_baseline1[count_t1]+raw_data[0,point_num])/2 # Slower but convenient
        beam_baseline2[count_t1] = (beam_baseline2[count_t1]+raw_data[1,point_num])/2
        beam_baseline3[count_t1] = (beam_baseline3[count_t1]+raw_data[2,point_num])/2
        beam_baseline4[count_t1] = (beam_baseline4[count_t1]+raw_data[3,point_num])/2
        started = 1
#    if (ver_sum_raw_data[point_num] < 0 and started == 0): # Bunch detection starts if the raw data reaches any negative value
#        started = 1
#        print ('Started')
    if (ver_sum_raw_data[point_num] > threshold11 and find_t11 == 1 and started == 1): #Magic number
        if (count_t1 == 1): # Do this only for the first bunch
            t1[count_t1] = point_num
            find_t12 = 1
            find_t11 = 0
            count_t1 = count_t1 +1
            #print ('Crossed first threshold')
        else:
            if(point_num > t2[count_t2 - 1]+ wait_t2): #magic number wait
                t1[count_t1] = point_num;#  % Store the value of time at start of bunch zero crossing
                find_t12 = 1
                find_t11 = 0
                count_t1 = count_t1 +1
        new_bunch = 0        
    if (ver_sum_raw_data[point_num] > threshold12 and find_t12 == 1 and started == 1): #Magic number
        find_t21 = 1
        find_t12 = 0
        #print ('Crossed second threshold')
    if (ver_sum_raw_data[point_num] < threshold21 and find_t21 == 1 and started == 1): #Magic number            
        find_t22 = 1
        find_t21 = 0
        #print ('Crossed third threshold')
    if(ver_sum_raw_data[point_num] < threshold22 and find_t22 == 1 and point_num >= t1[count_t1 - 1]+ wait_t1):
        t2[count_t2] = point_num;  #% Store the value of time at end of bunch zero crossing
        find_t11 = 1
        find_t22 = 0
        if(count_t2 > 1):
            bunch_frequency[count_t2] = ((125*1E6))/(t2[count_t2] - t2[count_t2-1])
        count_t2 = count_t2 +1
        new_bunch = 1
        tmin= np.min(ver_sum_raw_data[point_num:point_num+100])

ver_sum_raw_data = np.zeros((num_points)) # Make it equal to zero again


out = t2[10]- t1[10]
print('length of 100th Bunch is', out)
out = t2[100] - t1[100]
print('length of 1000th Bunch is', out)



# 
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %                   Define the window with respect to t1 and t2
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 
t1 = t1-22 #Magic number
t2 = t2+22 # Magic number





## Synchronous Bunch by bunch position calculation (in detected windows)


# Restoration of the baseline
pos_count_t1 = 0
pos_count_t2 = 0
for point_num in range(num_points):  
    if(point_num > t1[pos_count_t1] and point_num < t2[pos_count_t2] and pos_count_t1 < count_t1-1):
        incr_done = 1
        raw_data[0,point_num]=raw_data[0,point_num]- beam_baseline1[pos_count_t1]
        raw_data[1,point_num]=raw_data[1,point_num]- beam_baseline2[pos_count_t1]
        raw_data[2,point_num]=raw_data[2,point_num]- beam_baseline3[pos_count_t1]
        raw_data[3,point_num]=raw_data[3,point_num]- beam_baseline4[pos_count_t1]
    if (point_num > t2[pos_count_t2] and point_num < t1[pos_count_t1 + 1] and incr_done == 1 and pos_count_t2 < count_t2 -1 and pos_count_t1< count_t1 - 2):
        incr_done = 0
        pos_count_t1 = pos_count_t1 + 1
        pos_count_t2 = pos_count_t2 + 1



raw_data[0]=raw_data[0] + baseline1 + noise1 # Arbitrary external baseline
raw_data[1]=raw_data[1] + baseline2 + noise2
raw_data[2]=raw_data[2]+ baseline3 + noise3
raw_data[3]=raw_data[3]+ baseline4 + noise4

ver_sum_raw_data = raw_data[0] + raw_data[1]
ver_diff_raw_data = raw_data[0] - raw_data[1]
hor_sum_raw_data = raw_data[2] + raw_data[3]
hor_diff_raw_data = raw_data[3] - raw_data[2]

plt.plot(raw_data[0,plot_start:plot_stop])
plt.plot(raw_data[1,plot_start:plot_stop])
plt.plot(raw_data[2,plot_start:plot_stop])
plt.plot(raw_data[3,plot_start:plot_stop])



# Start of position calculation algorithms

pos_count_t1 = 0
pos_count_t2 = 0
ver_numerator = np.zeros((count_t1))
ver_denominator = np.zeros((count_t1))
hor_numerator = np.zeros((count_t1))
hor_denominator = np.zeros((count_t1))
incr_done = 0
ver_position_temp = np.zeros((count_t1))
ver_position_sum_diff= np.zeros((count_t1))
hor_position_temp = np.zeros((count_t1))
hor_position_sum_diff = np.zeros((count_t1))

point_in_bunch = 1
# 
for point_num in range(num_points):  
    if(point_num > t1[pos_count_t1] and point_num < t2[pos_count_t2] and pos_count_t1 < count_t1-1):
        incr_done = 1
        ver_product1 = ver_diff_raw_data[point_num]
        ver_product2 = ver_sum_raw_data[point_num]
        hor_product1 = hor_diff_raw_data[point_num]
        hor_product2 = hor_sum_raw_data[point_num]
        ver_numerator[pos_count_t1] = ver_numerator[pos_count_t1]+ ver_product1
        ver_denominator[pos_count_t1] = ver_denominator[pos_count_t1] + ver_product2
        hor_numerator[pos_count_t1] = hor_numerator[pos_count_t1]+ hor_product1
        hor_denominator[pos_count_t1] = hor_denominator[pos_count_t1] + hor_product2
        plot_window[point_num] = 1000
        point_in_bunch = point_in_bunch + 1

    if (point_num > t2[pos_count_t2] and point_num < t1[pos_count_t1 + 1] and incr_done == 1 and pos_count_t2 < count_t2 -1 and pos_count_t1< count_t1 - 2):
        ver_position_temp[pos_count_t1] =  ver_numerator[pos_count_t1]/ver_denominator[pos_count_t1]
        hor_position_temp[pos_count_t1] = hor_numerator[pos_count_t1]/hor_denominator[pos_count_t1]
        pos_count_t1 = pos_count_t1 +1
        pos_count_t2 = pos_count_t2 +1
        point_in_bunch = 1
        incr_done = 0
        ver_product1=0
        ver_product2=0
        hor_product1=0
        hor_product2=0

plt.plot(plot_window[plot_start:plot_stop]) # % See if the window generation was OK
ver_position_sum_diff = 50*ver_position_temp
hor_position_sum_diff = 120*hor_position_temp

plt.figure(2)
time = np.linspace(0,len(ver_position_sum_diff),len(ver_position_sum_diff))*5E-6
#time = t2[0:len(ver_position_sum_diff)]*8E-9
#time=np.linspace(0,(1/bunch_frequency[100])*len(ver_position_fit),len(ver_position_fit))
XPos =-2+3*np.cos(0.3*2*np.pi*(1/5E-6)*time+np.pi)
YPos =4.5+2*np.cos(0.23*2*np.pi*(1/5E-6)*time)
plt.plot(time,YPos,'b',linewidth=2.0)
plt.plot(time,XPos,'r',linewidth=2.0)
plt.plot(time,ver_position_sum_diff,'b*',linewidth=4.0)
plt.plot(time,hor_position_sum_diff,'r*',linewidth=4.0)
plt.title('Position calculated with TOPOS model',fontsize=22)
plt.axis([0.0,0.00006,-6, 14])
plt.ylabel('Position / mm',fontsize=20)
plt.xlabel('Time / s',fontsize=20)
plt.tick_params(axis='both', which='major', labelsize=22)
plt.tick_params(axis='both', which='minor', labelsize=10)
plt.legend(["Actual Vertical Position","Actual Horizontal Position","Calculated Vertical Position","Calculated Horizontal Position"],fontsize=22.0)
plt.show()
#plt.savefig('/home/Rahul/Desktop/topos.png')
# 
# ax2.set_title('Vertical Profile',fontsize=20)
# plt.setp(ax2.get_xticklabels(),fontsize=18)
# plt.setp(ax2.get_yticklabels(),fontsize=18)
# #colorbar(cax2)
# ax2.set_xticks((-10,-5,0,5,10))
# ax2.set_yticks((25,30,35,40,45,50,55))
# ax2.set_yticklabels((500,600,700,800,900,1000,1100))
# ax2.set_xlabel('y position / mm',fontsize=20)
#ax2.set_ylabel('Time / ms')
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
# %Calculate Position by Power of individual plates
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

pos_count_t1 = 2
pos_count_t2 = 2
ver_numerator = np.zeros((count_t1))
ver_denominator = np.zeros((count_t1))
hor_numerator = np.zeros((count_t1))
hor_denominator = np.zeros((count_t1))
incr_done = 0
ver_position_temp = np.zeros((count_t1))
ver_position_power = np.zeros((count_t1))
hor_position_temp = np.zeros((count_t1))
hor_position_power = np.zeros((count_t1))

point_in_bunch = 1

for point_num in range(num_points):  
    if(point_num > t1[pos_count_t1] and point_num < t2[pos_count_t2] and pos_count_t1 < count_t1-1):
        incr_done = 1
        ver_product1 = raw_data[0,point_num]*raw_data[0,point_num]
        ver_product2 = raw_data[1,point_num]*raw_data[1,point_num]
        hor_product1 = raw_data[2,point_num]*raw_data[2,point_num]
        hor_product2 = raw_data[3,point_num]*raw_data[3,point_num]
        ver_numerator[pos_count_t1] = ver_numerator[pos_count_t1]+ ver_product1
        ver_denominator[pos_count_t1] = ver_denominator[pos_count_t1] + ver_product2
        hor_numerator[pos_count_t1] = hor_numerator[pos_count_t1]+ hor_product1
        hor_denominator[pos_count_t1] = hor_denominator[pos_count_t1] + hor_product2
        plot_window[point_num] = 1000
        point_in_bunch = point_in_bunch + 1
    if (point_num > t2[pos_count_t2] and point_num < t1[pos_count_t1 + 1] and incr_done == 1 and pos_count_t2 < count_t2 -1 and pos_count_t1< count_t1 - 2):
        Ut = np.sqrt(ver_numerator[pos_count_t1])
        Ub = np.sqrt(ver_denominator[pos_count_t1])
        Ur = np.sqrt(hor_numerator[pos_count_t1])
        Ul = np.sqrt(hor_denominator[pos_count_t1])
        ver_position_temp[pos_count_t1] =  (Ut-Ub)/(Ut+Ub)
        hor_position_temp[pos_count_t1] = (-Ur+Ul)/(Ur+Ul)
        pos_count_t1 = pos_count_t1 +1
        pos_count_t2 = pos_count_t2 +1
        point_in_bunch = 1
        incr_done = 0
        ver_product1=0
        ver_product2=0
        hor_product1=0
        hor_product2=0


ver_position_power = 50*ver_position_temp
hor_position_power = 120*hor_position_temp
plt.figure(2)
#time=np.linspace(0,(1/bunch_frequency[100])*len(ver_position_fit),len(ver_position_fit))
plt.plot(time,ver_position_power,'b+')
plt.plot(time,hor_position_power,'r+')



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %                   Calculate position by fitting
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 

point_in_bunch = 0
pos_count_t1 = 2
pos_count_t2 = 2
ver_numerator = np.zeros((count_t1))
ver_denominator = np.zeros((count_t1))
hor_numerator = np.zeros((count_t1))
hor_denominator = np.zeros((count_t1))
ver_numerator1 = np.zeros((count_t1))
ver_denominator1 = np.zeros((count_t1))
hor_numerator1 = np.zeros((count_t1))
hor_denominator1 = np.zeros((count_t1))
incr_done = 0
ver_position_temp = np.zeros((count_t1))
ver_position_temp1 = np.zeros((count_t1))
ver_position_fit = np.zeros((count_t1))
ver_position_fit1 = np.zeros((count_t1))
hor_position_temp = np.zeros((count_t1))
hor_position_fit = np.zeros((count_t1))
#diff_temp = np.zeros((count_t1))
diff_temp = np.zeros((300,), dtype=np.float)
#print (diff_temp)
sum_temp =  np.zeros((300,), dtype=np.float)
for point_num in range(num_points):  
    if(point_num > t1[pos_count_t1] and point_num < t2[pos_count_t2] and pos_count_t1 < count_t1-1):
        incr_done = 1
        ver_product_num = ver_sum_raw_data[point_num]*ver_diff_raw_data[point_num]
        ver_product_den = ver_sum_raw_data[point_num]**2
        hor_product_num = hor_sum_raw_data[point_num]*hor_diff_raw_data[point_num]
        hor_product_den = hor_sum_raw_data[point_num]**2
        hor_numerator1[pos_count_t1] = hor_numerator1[pos_count_t1]+ hor_diff_raw_data[point_num]
        ver_numerator1[pos_count_t1] = ver_numerator1[pos_count_t1]+ ver_diff_raw_data[point_num]
        hor_denominator1[pos_count_t1] = hor_denominator1[pos_count_t1]+ hor_sum_raw_data[point_num]
        ver_denominator1[pos_count_t1] = ver_denominator1[pos_count_t1]+ ver_sum_raw_data[point_num]
        ver_numerator[pos_count_t1] = ver_numerator[pos_count_t1]+ ver_product_num
        ver_denominator[pos_count_t1] = ver_denominator[pos_count_t1] + ver_product_den
        hor_numerator[pos_count_t1] = hor_numerator[pos_count_t1]+ hor_product_num
        hor_denominator[pos_count_t1] = hor_denominator[pos_count_t1] + hor_product_den
  #      diff_temp [point_in_bunch] = ver_diff_raw_data[point_num]
  #      sum_temp [point_in_bunch] = ver_sum_raw_data[point_num]
# %      diff_fraction(point_in_bunch,pos_count_t1) = ((raw_data(plane+1,point_num)) - (raw_data(plane+2,point_num)));
# %      sum_fraction(point_in_bunch,pos_count_t1) = (raw_data(plane+1,point_num)) + (raw_data(plane+2,point_num));
        point_in_bunch = point_in_bunch + 1
#    end
    if (point_num > t2[pos_count_t2] and point_num < t1[pos_count_t1 + 1] and incr_done == 1 and pos_count_t2 < count_t2 -1 and pos_count_t1< count_t1 - 2):
        hor_position_temp[pos_count_t1] = (hor_numerator[pos_count_t1]-((hor_numerator1[pos_count_t1]*hor_denominator1[pos_count_t1])/(point_in_bunch-1)))/(hor_denominator[pos_count_t1]-((hor_denominator1[pos_count_t1]*hor_denominator1[pos_count_t1])/(point_in_bunch-1)))
        ver_position_temp[pos_count_t1] = (ver_numerator[pos_count_t1]-((ver_numerator1[pos_count_t1]*ver_denominator1[pos_count_t1])/(point_in_bunch-1)))/(ver_denominator[pos_count_t1]-((ver_denominator1[pos_count_t1]*ver_denominator1[pos_count_t1])/(point_in_bunch-1)))
        diff_temp = ver_diff_raw_data[t1[pos_count_t1]:t2[pos_count_t1]]
        sum_temp = ver_sum_raw_data[t1[pos_count_t1]:t2[pos_count_t1]]
        slope, intercept, r_value, p_value, std_err = stats.linregress(sum_temp[0:point_in_bunch-1],diff_temp[0:point_in_bunch-1])
        ver_position_temp1[pos_count_t1] = slope
        pos_count_t1 = pos_count_t1 +1
        pos_count_t2 = pos_count_t2 +1
        point_in_bunch = 0
        incr_done = 0
        ver_product_num=0
        ver_product_den=0
        hor_product_num=0
        hor_product_den=0
        diff_temp = 0
        sum_temp = 0



plt.figure(1);
# 
plt.plot(plot_window[plot_start:plot_stop]) # % See if the window generation was OK
ver_position_fit = 50*ver_position_temp
hor_position_fit = 120*hor_position_temp
ver_position_fit1 = 50*ver_position_temp1
plt.figure(2)
#time=np.linspace(0,(1/bunch_frequency[100])*len(ver_position_fit),len(ver_position_fit))
plt.plot(time,ver_position_fit,'bo')
plt.plot(time,ver_position_fit1,'go')
plt.plot(time,hor_position_fit,'ro')



# N = len(ver_position_fit[1000:5096:4])
# # sample spacing
# T = 5E-6
# x = np.linspace(0.0, N*T, N)
# yf = abs(FFT.fft(ver_position_fit[1000:5096:4]))
# xf = np.linspace(0.0, 0.5, N/2)
# plt.figure(4)
# plt.plot(xf, 2.0/N * np.abs(yf[0:N/2]))





## Asynchronous position calculation
#Asynchronous power algorithm

point_in_bunch = 0
pos_count_t1 = 0
pos_count_t2 = 0
ver_numerator = np.zeros((np.floor(num_points/fit_points)))
ver_denominator = np.zeros((np.floor(num_points/fit_points)))
hor_numerator = np.zeros((np.floor(num_points/fit_points)))
hor_denominator = np.zeros((np.floor(num_points/fit_points)))
ver_position_temp = np.zeros((np.floor(num_points/fit_points)))
hor_position_temp = np.zeros((np.floor(num_points/fit_points)))
async_ver_position_power = np.zeros((np.floor(num_points/fit_points)))
async_hor_position_power = np.zeros((np.floor(num_points/fit_points)))
for point_num in range(1,num_points-2*fit_points,fit_points):
    for i in range(fit_points):
        ver_product1 = raw_data[0,point_num+point_in_bunch]*raw_data[0,point_num+point_in_bunch]
        ver_product2 = raw_data[1,point_num+point_in_bunch]*raw_data[1,point_num+point_in_bunch]
        hor_product1 = raw_data[2,point_num+point_in_bunch]*raw_data[2,point_num+point_in_bunch]
        hor_product2 = raw_data[3,point_num+point_in_bunch]*raw_data[3,point_num+point_in_bunch]
        ver_numerator[pos_count_t1] = ver_numerator[pos_count_t1]+ ver_product1
        ver_denominator[pos_count_t1] = ver_denominator[pos_count_t1] + ver_product2
        hor_numerator[pos_count_t1] = hor_numerator[pos_count_t1]+ hor_product1
        hor_denominator[pos_count_t1] = hor_denominator[pos_count_t1] + hor_product2
        point_in_bunch = point_in_bunch + 1

    Ut = np.sqrt(ver_numerator[pos_count_t1])
    Ub = np.sqrt(ver_denominator[pos_count_t1])
    Ur = np.sqrt(hor_numerator[pos_count_t1])
    Ul = np.sqrt(hor_denominator[pos_count_t1])
    ver_position_temp[pos_count_t1] =  (Ut-Ub)/(Ut+Ub)
    hor_position_temp[pos_count_t1] = (-Ur+Ul)/(Ur+Ul)
    pos_count_t1 = pos_count_t1 +1
    pos_count_t2 = pos_count_t2 +1
    point_in_bunch = 0
    ver_product1=0
    ver_product2=0
    hor_product1=0
    hor_product2=0
    
async_ver_position_power = 50*ver_position_temp
async_hor_position_power = 120*hor_position_temp   
plt.figure(5)
time=np.linspace(0,fit_points*(8E-9)*len(async_ver_position_power),len(async_ver_position_power))
plt.plot(time,async_ver_position_power,'b+')
plt.plot(time,async_hor_position_power,'r+')

# Asynchronous fitting

point_in_bunch = 0
pos_count_t1 = 0
pos_count_t2 = 0
ver_numerator = np.zeros((np.floor(num_points/fit_points)))
ver_denominator = np.zeros((np.floor(num_points/fit_points)))
hor_numerator = np.zeros((np.floor(num_points/fit_points)))
hor_denominator = np.zeros((np.floor(num_points/fit_points)))
ver_numerator1 = np.zeros((np.floor(num_points/fit_points)))
ver_denominator1 = np.zeros((np.floor(num_points/fit_points)))
hor_numerator1 = np.zeros((np.floor(num_points/fit_points)))
hor_denominator1 = np.zeros((np.floor(num_points/fit_points)))
ver_position_temp = np.zeros((np.floor(num_points/fit_points)))
hor_position_temp = np.zeros((np.floor(num_points/fit_points)))
async_ver_position_fit = np.zeros((np.floor(num_points/fit_points)))
async_hor_position_fit = np.zeros((np.floor(num_points/fit_points)))
for point_num in range(1,num_points-2*fit_points,fit_points):
    for i in range(fit_points):
        ver_product_num = ver_sum_raw_data[point_num+point_in_bunch]*ver_diff_raw_data[point_num+point_in_bunch]
        ver_product_den = ver_sum_raw_data[point_num+point_in_bunch]**2
        hor_product_num = hor_sum_raw_data[point_num+point_in_bunch]*hor_diff_raw_data[point_num+point_in_bunch]
        hor_product_den = hor_sum_raw_data[point_num+point_in_bunch]**2
        hor_numerator1[pos_count_t1] = hor_numerator1[pos_count_t1]+ hor_diff_raw_data[point_num+point_in_bunch]
        ver_numerator1[pos_count_t1] = ver_numerator1[pos_count_t1]+ ver_diff_raw_data[point_num+point_in_bunch]
        hor_denominator1[pos_count_t1] = hor_denominator1[pos_count_t1]+ hor_sum_raw_data[point_num+point_in_bunch]
        ver_denominator1[pos_count_t1] = ver_denominator1[pos_count_t1]+ ver_sum_raw_data[point_num+point_in_bunch]
        ver_numerator[pos_count_t1] = ver_numerator[pos_count_t1]+ ver_product_num
        ver_denominator[pos_count_t1] = ver_denominator[pos_count_t1] + ver_product_den
        hor_numerator[pos_count_t1] = hor_numerator[pos_count_t1]+ hor_product_num
        hor_denominator[pos_count_t1] = hor_denominator[pos_count_t1] + hor_product_den
        point_in_bunch = point_in_bunch + 1

  #  ver_position_temp[pos_count_t1] = ver_numerator[pos_count_t1]/ver_denominator[pos_count_t1]
  #  hor_position_temp[pos_count_t1] = hor_numerator[pos_count_t1]/hor_denominator[pos_count_t1]
    hor_position_temp[pos_count_t1] = (hor_numerator[pos_count_t1]-((hor_numerator1[pos_count_t1]*hor_denominator1[pos_count_t1])/(point_in_bunch-1)))/(hor_denominator[pos_count_t1]-((hor_denominator1[pos_count_t1]*hor_denominator1[pos_count_t1])/(point_in_bunch-1)))
    ver_position_temp[pos_count_t1] = (ver_numerator[pos_count_t1]-((ver_numerator1[pos_count_t1]*ver_denominator1[pos_count_t1])/(point_in_bunch-1)))/(ver_denominator[pos_count_t1]-((ver_denominator1[pos_count_t1]*ver_denominator1[pos_count_t1])/(point_in_bunch-1)))
    pos_count_t1 = pos_count_t1 +1
    pos_count_t2 = pos_count_t2 +1
    point_in_bunch = 0
    ver_product_num=0
    ver_product_den=0
    hor_product_num=0
    hor_product_den=0
    
async_ver_position_fit = 50*ver_position_temp
async_hor_position_fit = 120*hor_position_temp   
plt.figure(5)
time=np.linspace(0,fit_points*(8E-9)*len(async_ver_position_fit),len(async_ver_position_fit))
plt.plot(time,async_ver_position_fit,'bo')
plt.plot(time,async_hor_position_fit,'ro')

#Save to PGF/TikZ
#   tikz_save( 'contour.tikz', figureheight='12cm', figurewidth='9cm' ) 
#f.savefig('/home/Rahul/Desktop/profile.pdf')
closed_len = 100
#ver_closed_orbit = np.zeros((np.floor(num_points/(fit_points*closed_len))))
#hor_closed_orbit = np.zeros((np.floor(num_points/(fit_points*closed_len))))
ver_mean_orbit = np.zeros((np.floor(num_points/(fit_points*closed_len))))
hor_mean_orbit = np.zeros((np.floor(num_points/(fit_points*closed_len))))
ver_std_orbit = np.zeros((np.floor(num_points/(fit_points*closed_len))))
hor_std_orbit = np.zeros((np.floor(num_points/(fit_points*closed_len))))
ver_mean_orbit_power = np.zeros((np.floor(num_points/(fit_points*closed_len))))
hor_mean_orbit_power = np.zeros((np.floor(num_points/(fit_points*closed_len))))
ver_std_orbit_power = np.zeros((np.floor(num_points/(fit_points*closed_len))))
hor_std_orbit_power = np.zeros((np.floor(num_points/(fit_points*closed_len))))
ver_sum=0
hor_sum=0
closed_orbit_len = int(np.floor(len(async_hor_position_fit)/closed_len)-1)


for i in range(closed_orbit_len):
#    for j in range(closed_len):
#        ver_sum = ver_sum + async_ver_position_fit[i*closed_len + j]
#        hor_sum = ver_sum + async_hor_position_fit[i*closed_len + j]
#    ver_closed_orbit[i] = ver_sum/closed_len
#    hor_closed_orbit[i] = hor_sum/closed_len
    ver_mean_orbit[i] = np.mean(async_ver_position_fit[i*closed_len : (i+1)*closed_len])
    hor_mean_orbit[i] = np.mean(async_hor_position_fit[i*closed_len : (i+1)*closed_len])
    ver_std_orbit[i] = np.std(async_ver_position_fit[i*closed_len : (i+1)*closed_len])
    hor_std_orbit[i] = np.std(async_hor_position_fit[i*closed_len : (i+1)*closed_len])
    ver_mean_orbit_power[i] = np.mean(async_ver_position_power[i*closed_len : (i+1)*closed_len])
    hor_mean_orbit_power[i] = np.mean(async_hor_position_power[i*closed_len : (i+1)*closed_len])
    ver_std_orbit_power[i] = np.std(async_ver_position_power[i*closed_len : (i+1)*closed_len])
    hor_std_orbit_power[i] = np.std(async_hor_position_power[i*closed_len : (i+1)*closed_len])
    ver_sum=0
    hor_sum=0
    
plt.figure(6)
time=np.linspace(0,fit_points*closed_len*(8E-9)*len(ver_mean_orbit),len(ver_mean_orbit))
#plt.plot(time,ver_closed_orbit ,'b+')
#plt.plot(time,hor_closed_orbit,'r+')    

plt.errorbar(time,ver_mean_orbit,yerr=ver_std_orbit,fmt='bo')
plt.errorbar(time,hor_mean_orbit,yerr=hor_std_orbit,fmt='ro')
plt.figure(7)
plt.errorbar(time,ver_mean_orbit_power,yerr=ver_std_orbit_power,fmt='b*')
plt.errorbar(time,hor_mean_orbit_power,yerr=hor_std_orbit_power,fmt='r*')



N = len(ver_position_fit)
# sample spacing
T = 4.0E-7
x = np.linspace(0.0, N*T, N)
plt.figure(10)
plt.plot(x,ver_position_fit)
plt.plot(x,hor_position_fit)
yf = abs(FFT.fft(ver_position_fit))
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
xdiff = abs(FFT.fft(hor_position_fit))
plt.plot(xf, 2.0/N * np.abs(yf[0:N/2]))
plt.plot(xf, 2.0/N * np.abs(xdiff[0:N/2]))
#plt.figure(12)
#plt.semilogy(xf, 2.0/N * np.abs(yf[0:N/2]))
plt.figure(11)
ydiff = abs(FFT.fft(hor_position_sum_diff))
ydiff1 = abs(FFT.fft(ver_position_sum_diff))
plt.plot(xf, 2.0/N * np.abs(ydiff[0:N/2]))
plt.plot(xf, 2.0/N * np.abs(ydiff1[0:N/2]))

Fs = 1.0e9
lines = [line.rstrip('\n') for line in open('x2_bbq_ext.data')] #Getting data generated by NGspice in appropriate format for plotting 
line1 = [line.split() for line in open('x2_bbq_ext.data',"r")]
xpt = 0*np.ones(len(lines))
ypt = 0*np.ones(len(lines))
for i in range(len(xpt)):
    xpt[i] = float(line1[i][0])
    ypt[i] = float(line1[i][1])
yf = abs(FFT.fft(ypt))
f = np.arange(0,Fs,Fs/len(yf))
plt.plot(xf, 2000.0/N * np.abs(yf[0:N/2]),'r--')
plt.show()

#plt.figure(7)

#Save to PGF/TikZ
#   tikz_save( 'contour.tikz', figureheight='12cm', figurewidth='9cm' ) 
#    f.savefig('/home/Rahul/Desktop/profile.pdf')























#       end
# % Position calculation algorithm for data taken at injection flat top, so
# % uses equal intervals between bunches
# % Steps to be followed
# % 1) Find the zero crossings of data to find the "time windows" (Does not
# % matter, even RF directly can be used, the Idea is to use a part of
# % bunch), finds the average distance between bunches
# 
# clear all;
# fourier_point = 2*1024; fc=212600;
# fre_axis=(0:1/fourier_point:1)*4;
# % Reading the raw data file%%%%%%%%%%%%%%%%%%%
# in_point = 32; %%%% Length of header, can change, always look at header variable first, and see if it looks like header!
# 
# file_path = input('Enter the raw data file name','s');
# plane = input('Which plane to use? For Vertical enter 0 ; For Horizontal =2 ;');
# num_points = input('Number of Points to read');
# file_id1 = fopen(file_path,'r');
# header = fread(file_id1,in_point,'32*char=>char'); 
# start_point = input('From when to start data processing, in terms of number of samples');
# fseek(file_id1,0,'eof');
# size = ftell(file_id1);
# total_points = size;
# raw_data(4,num_points) = 0;
# for i=0:3
# fseek(file_id1,in_point+start_point*8+i*2,'bof'); % raw_data(1,:) has Y+, raw_data(2,:) has Y-, raw_data(3,:) has X+
# raw_data(i+1,:) = fread(file_id1,num_points,'int16',6); % Raw data reading done in the raw_data variable
# end
# fclose(file_id1);
# 
# raw_data_shifted(4,length(raw_data(1,:))) = 0;
# sum_raw_data = raw_data(2,:) + raw_data(1,:); 
# difference_raw_data = raw_data(2,:) - raw_data(1,:); 
# % Start of the raw_data processing
# 
# raw_data(1,:) = raw_data(1,:);
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %1) Find the Windows ( Here the zero crossing has been used for finding
# %bunches, fairly simple bunch detection algorithm)%%%%%%%%%%%%%%%%%%%%%%%%%
# figure(2);
# % for i=1:100
# %   plot(raw_data(1,20+ i*145:(i+1)*145));
# %   F(i)=getframe;
# % end
# % movie(F,1,3);
# plot(raw_data(1,1:1000));
# plot(raw_data(2,1:1000),'r');
# hold on;
# % plot(raw_data(2,:));
# % plot(difference_raw_data);
# % plot(sum_raw_data);
# t1(num_points/50) = 0;t2(num_points/50) = 0;bunch_frequency(num_points/50) =0;
# count_t1 = 1; count_t2 = 1; find_t1 = 1; find_t2 =0; started = 0;wait_t1 = 10; wait_t2=10;
# for point_num = 1:1:num_points
#     % Starting condition, first crossing is positive slope resulting in
#     % detection of positive part of bunches and can be made of detect only
#     % negative parts of bunches ( bunch data ranges from -8192 to +8192)
#     if (raw_data(plane+1,point_num) < 0 && started == 0) %% Bunch detection starts if the raw data reaches any negative value
#         started = 1;
#     end
#     if(raw_data(plane+1,point_num) > 0 && find_t1 == 1 &&started == 1)
#         if (count_t1 == 1) % Do this only for the first bunch
#         t1(count_t1) = point_num;
#         find_t2 = 1;
#         find_t1 = 0;
#         count_t1 = count_t1 +1;
#         else
#             if(point_num > t2(count_t2 - 1)+ wait_t2) % magic number 30
#         t1(count_t1) = point_num;  % Store the value of time at start of bunch zero crossing
#         find_t2 = 1;
#         find_t1 = 0;
#         count_t1 = count_t1 +1;
#             end
#         end
#     end
#     if(raw_data(plane + 1,point_num) < 0 && find_t2 == 1 && point_num >= t1(count_t1 - 1)+ wait_t1)
#         t2(count_t2) = point_num;  % Store the value of time at end of bunch zero crossing
#         find_t1 = 1;
#         find_t2 = 0;
#         if(count_t2 > 1)
#         bunch_frequency(count_t2) = ((125*10^6))/(t2(count_t2) - t2(count_t2-1));
#         end
#         count_t2 = count_t2 +1;
#     end
# end
# 
# %%%%%%%%The first and foremost thing to check is the evolution of window
# %%%%%%%%length to see if algorithm really worked%%%%%%%%%%%%%%%%%%%
# 
# disp('length of 100th Bunch'); out = t2(100)- t1(100);
# disp(out);
# disp('length of 1000th Bunch'); out = t2(1000) - t1(1000);
# disp(out);
# % disp('length of 10000th Bunch'); out = t2(10000) -t1(10000);
# % disp(out);
# 
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %                   Define the window with respect to t1 and t2
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 
# t1 = t1-10;
# t2 = t2;
# 
# 
# 
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
# %Calculate Position by baseline restoration and difference over sum method
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# baseline(length(t1),4) = 0;
# 
# % for i = 1:4
# %     baseline(1,i) = raw_data(i,1);
# % for point_num = 1:1:1000 
# %     if (raw_data(i,point_num) <= baseline(1,i))
# %     baseline(1,i) = (baseline(1,i)+ raw_data(i,point_num))/2;
# %     end
# % end
# % end
# 
# pos_count_t1 = 2; pos_count_t2 = 2;
# incr_done = 0;  position_temp(length(t1)) = 0;
# plot_window(1:num_points) = -500; point_in_bunch = 1;
# diff_fraction(60,count_t1) = 0; sum_fraction(60,count_t1) = 0; base_move=1;see1 = 0;see2 = 0;
# baseline(2,1:4) = -2000;
# for point_num = 1:1:num_points 
# 
#     
#    if(point_num > t1(pos_count_t1) && point_num <= t2(pos_count_t2) && pos_count_t1 < count_t1-1)
#        if (see1 > 1)
#            baseline(pos_count_t1+1,plane+1) = baseline(pos_count_t1+1,plane+1)/see1;
#            baseline(pos_count_t1+1,plane+2) = baseline(pos_count_t1+1,plane+2)/see2;
#            see1 = 0; see2 = 0;
#        end
#      raw_data_shifted(plane+1,point_num) = raw_data(plane+1,point_num)- baseline(pos_count_t1+1,plane+1);
#      raw_data_shifted(plane+2,point_num) = raw_data(plane+2,point_num)- baseline(pos_count_t1+1,plane+2);
#      incr_done = 1;
#      plot_window(point_num) = 1000;
#      diff_fraction(point_in_bunch,pos_count_t1) = ((raw_data_shifted(plane+1,point_num)) - (raw_data_shifted(plane+2,point_num)));
#      sum_fraction(point_in_bunch,pos_count_t1) = (raw_data_shifted(plane+1,point_num)) + (raw_data_shifted(plane+2,point_num));
#      point_in_bunch = point_in_bunch + 1;
#    
#    elseif (point_num > t2(pos_count_t2) && point_num < t1(pos_count_t1 + 1) && incr_done == 1 && pos_count_t2 < count_t2 -1 && pos_count_t1< count_t1 - 2)
#       pos_count_t1 = pos_count_t1 +1;
#       pos_count_t2 = pos_count_t2 +1;
#       point_in_bunch = 1;
#       incr_done = 0; 
#    else
# %     if (rem(point_num,100) == 0)
# %     see = 1;
# %     end
#     if (raw_data(plane+1,point_num) <= baseline(pos_count_t1,plane+1)+50)
#     baseline(pos_count_t1+1,plane+1) = (baseline(pos_count_t1+1,plane+1)+ raw_data(plane+1,point_num));
# %     check(base_move,1) = baseline(plane+1);
# %     check(base_move,2) = point_num;
#      see1 = see1 +1;
#     base_move=base_move+1;
#     end
#     if (raw_data(plane+2,point_num) <= baseline(pos_count_t1,plane+2)+50)
#     baseline(pos_count_t1+1, plane+2) = (baseline(pos_count_t1+1,plane+2)+ raw_data(plane+2,point_num));
# %     check(base_move,3) = point_num;
#      see2 = see2 +1;
#     end
#     
#    end
# end
# total_diff_fraction = sum((diff_fraction),1)/point_in_bunch;
# total_sum_fraction = sum((sum_fraction),1)/point_in_bunch;
# position_sum_diff_temp = total_diff_fraction./total_sum_fraction;
# position_sum_diff = 150*position_sum_diff_temp;
# figure(2);
# plot(raw_data_shifted(plane+1,1:1000));
# plot(raw_data_shifted(plane+2,1:1000),'r');
# hold on;
# 
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %                   Calculate position by fitting
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 
# pos_count_t1 = 2; pos_count_t2 = 2;
# numerator(count_t1) = 0; denominator(count_t1) = 0;
# incr_done = 0;  position_temp(length(t1)) = 0;
# plot_window(1:num_points) = -500; point_in_bunch = 1;
# 
# for point_num = 1:1:num_points   
#    if(point_num > t1(pos_count_t1) && point_num < t2(pos_count_t2) && pos_count_t1 < count_t1-1)
#        incr_done = 1;
#      product_num = raw_data(plane+1,point_num)*raw_data(plane+2,point_num);
#      product_den = (raw_data(plane+1,point_num)^2);
#      numerator(pos_count_t1) = numerator(pos_count_t1)+ product_num;
#      denominator(pos_count_t1) = denominator(pos_count_t1) + product_den;
#      plot_window(point_num) = 1000;
# %      diff_fraction(point_in_bunch,pos_count_t1) = ((raw_data(plane+1,point_num)) - (raw_data(plane+2,point_num)));
# %      sum_fraction(point_in_bunch,pos_count_t1) = (raw_data(plane+1,point_num)) + (raw_data(plane+2,point_num));
#      point_in_bunch = point_in_bunch + 1;
#    end
#       if (point_num > t2(pos_count_t2) && point_num < t1(pos_count_t1 + 1) && incr_done == 1 && pos_count_t2 < count_t2 -1 && pos_count_t1< count_t1 - 2)
#       position_temp(pos_count_t1) = (-numerator(pos_count_t1)+ denominator(pos_count_t1))/(numerator(pos_count_t1)+ denominator(pos_count_t1));
#       pos_count_t1 = pos_count_t1 +1;
#       pos_count_t2 = pos_count_t2 +1;
#       point_in_bunch = 1;
#       incr_done = 0;
#       end
# end
# % total_diff_fraction = sum(abs(diff_fraction),1)/point_in_bunch;
# % total_sum_fraction = sum(abs(sum_fraction),1)/point_in_bunch;
# % and_position = total_diff_fraction./total_sum_fraction;
# 
# figure(2);
# 
# plot(plot_window(1:1000)); % See if the window generation was OK
# position_fit =150*position_temp;

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
# %Calculate Position by baseline restoration and difference over sum method
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# baseline(length(t1),4) = 0;
# 
# % for i = 1:4
# %     baseline(1,i) = raw_data(i,1);
# % for point_num = 1:1:1000 
# %     if (raw_data(i,point_num) <= baseline(1,i))
# %     baseline(1,i) = (baseline(1,i)+ raw_data(i,point_num))/2;
# %     end
# % end
# % end
# 
# pos_count_t1 = 2; pos_count_t2 = 2;
# incr_done = 0;  position_temp(length(t1)) = 0;
# plot_window(1:num_points) = -500; point_in_bunch = 1;
# diff_fraction(60,count_t1) = 0; sum_fraction(60,count_t1) = 0; base_move=1;see1 = 0;see2 = 0;
# baseline(2,1:4) = -2000;
# for point_num = 1:1:num_points 
# 
#     
#    if(point_num > t1(pos_count_t1) && point_num <= t2(pos_count_t2) && pos_count_t1 < count_t1-1)
#        if (see1 > 1)
#            baseline(pos_count_t1+1,plane+1) = baseline(pos_count_t1+1,plane+1)/see1;
#            baseline(pos_count_t1+1,plane+2) = baseline(pos_count_t1+1,plane+2)/see2;
#            see1 = 0; see2 = 0;
#        end
#      raw_data_shifted(plane+1,point_num) = raw_data(plane+1,point_num)- baseline(pos_count_t1+1,plane+1);
#      raw_data_shifted(plane+2,point_num) = raw_data(plane+2,point_num)- baseline(pos_count_t1+1,plane+2);
#      incr_done = 1;
#      plot_window(point_num) = 1000;
#      diff_fraction(point_in_bunch,pos_count_t1) = ((raw_data_shifted(plane+1,point_num)) - (raw_data_shifted(plane+2,point_num)));
#      sum_fraction(point_in_bunch,pos_count_t1) = (raw_data_shifted(plane+1,point_num)) + (raw_data_shifted(plane+2,point_num));
#      point_in_bunch = point_in_bunch + 1;
#    
#    elseif (point_num > t2(pos_count_t2) && point_num < t1(pos_count_t1 + 1) && incr_done == 1 && pos_count_t2 < count_t2 -1 && pos_count_t1< count_t1 - 2)
#       pos_count_t1 = pos_count_t1 +1;
#       pos_count_t2 = pos_count_t2 +1;
#       point_in_bunch = 1;
#       incr_done = 0; 
#    else
# %     if (rem(point_num,100) == 0)
# %     see = 1;
# %     end
#     if (raw_data(plane+1,point_num) <= baseline(pos_count_t1,plane+1)+50)
#     baseline(pos_count_t1+1,plane+1) = (baseline(pos_count_t1+1,plane+1)+ raw_data(plane+1,point_num));
# %     check(base_move,1) = baseline(plane+1);
# %     check(base_move,2) = point_num;
#      see1 = see1 +1;
#     base_move=base_move+1;
#     end
#     if (raw_data(plane+2,point_num) <= baseline(pos_count_t1,plane+2)+50)
#     baseline(pos_count_t1+1, plane+2) = (baseline(pos_count_t1+1,plane+2)+ raw_data(plane+2,point_num));
# %     check(base_move,3) = point_num;
#      see2 = see2 +1;
#     end
#     
#    end
# end
# total_diff_fraction = sum((diff_fraction),1)/point_in_bunch;
# total_sum_fraction = sum((sum_fraction),1)/point_in_bunch;
# position_sum_diff_temp = total_diff_fraction./total_sum_fraction;
# position_sum_diff = 150*position_sum_diff_temp;
# figure(2);
# plot(raw_data_shifted(plane+1,1:1000));
# plot(raw_data_shifted(plane+2,1:1000),'r');

