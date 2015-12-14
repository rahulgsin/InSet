#!/usr/bin/python
""" Generic ngspice plotting Module

The module takes the following arguments

Schematic name --- Name of the NGspice schematic

Input_signal --- Input signal .txt file

Voltage_nodes --- voltage nodes which has to be plotted"""

# meta info
__author__ = 'Rajesh Asutkar'
__email__ = 'asutkarrajesh@sggs.ac.in'
__version__ = '-1.0'
__lastchanged__ ='17082015'

import numpy as np
import subprocess
from mpmath import mpf
import matplotlib.pyplot as plt
import sys
import time
from subprocess import call
import os
import scipy.fftpack as fft

class spice():
    
    """ The Generic spice class defines all the generic spice parameters
    
    spice settings can be stored in an external file and retrieved"""

    def __init__(self,*args,**kwargs):

        """ It takes the specified Ngspice schematic file name, Input signal, Voltage nodes for plotting from the user"""
        
        if len(args) == 0:
            self.parameters = {}
            self.parameters = kwargs
        elif len(args) == 4:
            dir = os.path.dirname(__file__)
            #print (dir)
            rel_dir_name = 'defined_'+__name__ +'s'
            #print (rel_dir_name)
            filename = os.path.join(dir,rel_dir_name,args[0])
            #print (filename)
            if os.path.isfile(filename) == False:
                print('Specified file' +filename+ 'to read the beam parameters does not exist, exiting ...')
                exit()
            else:
                reader = csv.reader(open(filename, 'r'))
                self.parameters = dict(x for x in reader)       
        elif len(args) == 3:
            self.parameters = {}
            self.parameters["Schematic"]= args[0] # .cir extension
            self.parameters["Input_signal"] = args[1] #Input signal
            self.parameters["Voltage_nodes"] = args[2] #voltage nodes to plot
        else:
            print('You have the wrong number of arguments, Please use help...')
        
        
        # Check if the some parameters are not defined or assigned to None or have the wrong type
    
        if self.parameters["Schematic"] == None:
            print ("Schematic is not defined")
            print ("Throw exception")
        if type(self.parameters["Schematic"]) != 'str':
           self.parameters["Schematic"] = str( self.parameters["Schematic"])

        if os.path.isfile(self.parameters["Schematic"]) == False:
                print('Specified file '+self.parameters["Schematic"]+ ' does not exist, please check the file name ...')
                sys.exit()
            
        if self.parameters["Input_signal"] == None:
            print ("input signal is not defined")
            print ("Throw exception")
        elif self.parameters["Input_signal"] is True:
            Input_para = open("Input_signal.txt","w")
            Input_para.write(".model filesrc filesource (file="+'"'+self.parameters["Input_signal"]+'"'+")")
            
        self.parameters["No_of_plots"] = len(self.parameters['Voltage_nodes'])
        

        plotng = open("plotng.txt","w")
        time.sleep(2)
        for N in range(0,int(self.parameters["No_of_plots"])):
            plotng.write("wrdata plot"+str(N)+" "+self.parameters['Voltage_nodes'][N]+'\n')
            
        
    def NGspice(self):

        """ This function will invoke NGspice 
        
        Simulate the user defined schematic file 

        Write the data at user defined voltage nodes in files named plot0, plot1... for voltage nodes given respectively

        Plot the results from user defined voltage nodes """
        
        call(["gnome-terminal","--command=ngspice"+" "+ self.parameters["Schematic"]])  #Calls Terminal and Runs NGspice program and specified command
        time.sleep(15)  #give some time to NGspice
        plotHandles = []
        for N in range(0,int(self.parameters["No_of_plots"])):
            if os.path.isfile('plot'+str(N)+'.data') == False:
                print('Specified voltage node '+self.parameters['Voltage_nodes'][N]+ ' does not exist, exiting ...')
                sys.exit()
            self.mag = [line.rstrip('\n') for line in open('plot'+str(N)+'.data')] #Getting input in appropriate format for plotting
            self.line1 = [line.split() for line in open('plot'+str(N)+'.data',"r")]
            globals()["xpt"+str(N)]= 0*np.ones(len(self.mag))
            globals()["ypt"+str(N)]= 0*np.ones(len(self.mag))
            
            for i in range(len(self.mag)):
                globals()["xpt"+str(N)][i] = float(self.line1[i][0])/1.0e6	#collecting input points for plotting
                globals()["ypt"+str(N)][i] = float(self.line1[i][1])	#collecting input points for plotting
           
            x, = plt.plot(globals()["xpt"+str(N)], globals()["ypt"+str(N)],linewidth=1.5) #need the ',' per ** below
            plotHandles.append(x)
      

        #plt.xlabel('time t/sec',fontsize=18)
        #plt.ylabel('V',fontsize=18)
        #plt.plot(xpt,ypt,'r',xpt2,ypt2,'g',xpt3,ypt3,'+',xpt4,ypt4,'m',linewidth=2)
        #plt.legend(['Input','TOPOS op'],loc='best')
#plt.figure(1)
#plt.plot(xpt,ypt2-ypt,xpt,ypt2+ypt)
#plt.figure(2)
#plt.plot(xpt3,ypt3-ypt4,xpt3,ypt3+ypt4)
        #plt.xticks(fontsize = 22) 
        #plt.yticks(fontsize = 22)
        #plt.xlabel('time t/ usec',fontsize=22)
        #plt.ylabel('V',fontsize=22)
        #plt.xscale('log')
        plt.grid(True)
        #plt.xlabel('time t/sec')
        #plt.ylabel('input voltage v')
        #plt.legend(self.parameters['Voltage_nodes'],loc='upper right')
        #plt.legend(['Input','Peak detector output'],loc='best')
        plt.show()
        os.remove("plotng.txt")
        for N in range(0,int(self.parameters["No_of_plots"])):          #removing files which were created during simulation 
            os.remove("plot"+str(N)+".data")
            
       
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

if __name__ == "__main__":
    dict_tfx1 = {'Schematic':'envelope2.cir', 'Input_signal':None, 'Voltage_nodes': ['v(1)','v(8)','v(19)','v(89)','v(14)','v(149)','(v(14)-v(149))']}
    tfx = spice(**dict_tfx1)
    tfx.NGspice()
