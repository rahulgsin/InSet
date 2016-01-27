#!/usr/bin/python
""" Generic ngspice transient response and plotting module

The module takes the following arguments

Schematic --- Name of the NGspice schematic /Netlist: Include the source parameter, sim parameter and plot file to it

Source_type --- Type of souce, e.g. Arbitrary, Pulse or sinusoidal AND either voltage or current source

Source_parameters --- Parameters based on source type, in case of arbitrary, it is an external file

Sim_parameters --- Simulation parameters for the transient simulation

plot_nodes_branches --- Voltage nodes/ Current branches to be plotted"""

# meta info
__author__ = 'Rahul Singh/(Org: Rajesh Asutkar)'
__email__ = 'asutkarrajesh@sggs.ac.in'
__version__ = '-1.0'
__lastchanged__ ='27012016'

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

        """ It takes the specified Ngspice schematic file name, Type of input: Current/Voltage, Input signal/stimulus, and the voltage nodes/current branches to be plotted from the user"""
### When the class is initialized in non script mode        

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
        elif len(args) == 3: ### Check this later !!!!
            self.parameters = {}
            self.parameters["Schematic"]= args[0] # .cir extension
            self.parameters["Source_type"] = args[1] #Source Type
            self.parameters["Source_Parameters"] = args[2] #Source parameters
            self.parameters["Sim_Parameters"] = args[2] #Simulation parameters
            self.parameters["plot_nodes_branches"] = args[3] #voltage nodes/current branches to plot
        else:
            print('You have the wrong number of arguments, Please use help...')
        
### Check the schematic
        
        # Check if the some parameters are not defined or assigned to None or have the wrong type
    
        if self.parameters["Schematic"] == None:
            print ("Schematic is not defined, exiting the program")
            sys.exit()
        if type(self.parameters["Schematic"]) != 'str':
           self.parameters["Schematic"] = str( self.parameters["Schematic"])
        if os.path.isfile(self.parameters["Schematic"]) == False:
                print('Specified file '+self.parameters["Schematic"]+ ' does not exist, please check the file name ...')
                sys.exit()
   
### Write the source file
                
        if self.parameters["Source_type"] == None:
            print ("Source type is not defined, exiting the program")
            sys.exit()
           
           
        if self.parameters["Source_nodes"] == None:
            print ("Source nodes are not defined, exiting the program")
            sys.exit()
        if type(self.parameters["Source_nodes"]) != 'str':
           self.parameters["Source_nodes"] = str( self.parameters["Source_nodes"])
           
                          
        if self.parameters["Source_Parameters"] == None:
            print ("Source parameters are not defined, exiting the program")
            sys.exit()
        else:
            
            Input_para = open("Circuits/Tempfiles/Source_signal.txt","w")
            print(self.parameters['Source_type'][0])
            if self.parameters['Source_type'][0] == 'Arb':
                Input_para.write("A"+self.parameters["Source_type"][1]+"SRC1 %"+self.parameters["Source_type"][1]+"(["+self.parameters["Source_nodes"]+"]) filesrc\n")
                Input_para.write(".model filesrc filesource (file="+'"'+self.parameters["Source_Parameters"]+'"'+")")
                
            if self.parameters['Source_type'][0] == 'Pulse':
                Input_para.write(self.parameters["Source_type"][1]+"IN "+self.parameters["Source_nodes"]+" PULSE("+self.parameters["Source_Parameters"]+")")

            if self.parameters['Source_type'][0] == 'Sin':
                Input_para.write(self.parameters["Source_type"][1]+"IN "+self.parameters["Source_nodes"]+" SIN("+self.parameters["Source_Parameters"]+")")
                
            Input_para.close()

### Write the simulation parameters
        
        if self.parameters["Sim_Parameters"] == None:
            print ("Simulation parameters are not defined, exiting the program")
            sys.exit()
        else:
                
            Sim_para = open("Circuits/Tempfiles/Sim_parameters.txt","w")    
            Sim_para.write(".CONTROL\n")
            Sim_para.write("TRAN "+self.parameters["Sim_Parameters"][0]+" "+self.parameters["Sim_Parameters"][1])  
            Sim_para.close()            
        self.parameters["No_of_plots"] = len(self.parameters['plot_nodes_branches'])
        plotng = open("Circuits/Tempfiles/plotng.txt","w")
        time.sleep(2)
        for N in range(0,int(self.parameters["No_of_plots"])):
            plotng.write("wrdata Circuits/Tempfiles/plot"+str(N)+" "+self.parameters['plot_nodes_branches'][N]+'\n')
            
### Run the NG Spice and plot the outputs
        
    def NGspice(self):

        """ This function will invoke NGspice 
        
        Simulate the user defined schematic file 

        Write the data at user defined voltage nodes in files named plot0, plot1... for voltage nodes given respectively

        Plot the results from user defined voltage nodes """
        
        call(["gnome-terminal","--command=ngspice"+" "+ self.parameters["Schematic"]])  #Calls Terminal and Runs NGspice program and specified command
        time.sleep(5)  #give some time to NGspice
        plotHandles = []
        for N in range(0,int(self.parameters["No_of_plots"])):
            if os.path.isfile('Circuits/Tempfiles/plot'+str(N)+'.data') == False:
                print('Specified voltage node and current branches '+self.parameters['plot_nodes_branches'][N]+ ' does not exist, exiting ...')
                sys.exit()
            self.mag = [line.rstrip('\n') for line in open('Circuits/Tempfiles/plot'+str(N)+'.data')] #Getting input in appropriate format for plotting
            self.line1 = [line.split() for line in open('Circuits/Tempfiles/plot'+str(N)+'.data',"r")]
            globals()["xpt"+str(N)]= 0*np.ones(len(self.mag))
            globals()["ypt"+str(N)]= 0*np.ones(len(self.mag))
            
            for i in range(len(self.mag)):
                globals()["xpt"+str(N)][i] = float(self.line1[i][0])/1.0e6	#collecting input points for plotting
                globals()["ypt"+str(N)][i] = float(self.line1[i][1])	#collecting input points for plotting
           
            x, = plt.plot(globals()["xpt"+str(N)], globals()["ypt"+str(N)],linewidth=1.5) #need the ',' per ** below
            plotHandles.append(x)
            
  #### Put the legends on the plot    
        #Plotting options/labels, text size etc.
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
        
        
        # Remove the temporary files
        
        os.remove("Circuits/Tempfiles/plotng.txt")
        os.remove("Circuits/Tempfiles/Source_signal.txt")
        os.remove("Circuits/Tempfiles/Sim_parameters.txt")
        for N in range(0,int(self.parameters["No_of_plots"])):          #removing files which were created during simulation 
            os.remove("Circuits/Tempfiles/plot"+str(N)+".data")
            
       
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

if __name__ == "__main__":
    # Arbitrary source
    dict_tfx1 = {'Schematic':'Circuits/currenttrafo.cir','Source_type': ['Arb', 'I'], 'Source_Parameters': '../simdata/current_profile2.txt','Source_nodes':'4 0','Sim_Parameters': ['1ns','10us'], 'plot_nodes_branches': ['-v(1)','-v(4)','-vr1#branch','-vc1#branch','-vl1#branch']}
    # Pulse source
    dict_tfx2 = {'Schematic':'Circuits/currenttrafo.cir','Source_type': ["Pulse", "I"], 'Source_Parameters':'-1 1 5000ns 2ns 2ns 100ns 0ns','Source_nodes':'4 0','Sim_Parameters':["1ns","10us"], 'plot_nodes_branches': ['-v(1)','-v(4)','-vr1#branch','-vc1#branch','-vl1#branch']} ### Check the spice definitions
    # Sinusoidal source
    dict_tfx3 = {'Schematic':'Circuits/currenttrafo.cir','Source_type': ["Sin", "I"], 'Source_Parameters':'0 1 10MEG 100ns 1E-10','Source_nodes':'4 0','Sim_Parameters':["1ns","10us"], 'plot_nodes_branches': ['-v(1)','-v(4)','-vr1#branch','-vc1#branch','-vl1#branch']} ### Check the spice definitions
    tfx = spice(**dict_tfx3)
    tfx.NGspice()
