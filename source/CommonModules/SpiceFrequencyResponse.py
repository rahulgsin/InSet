#!/usr/bin/python
""" Generic Transfer function Module

The module takes the following arguments

Schematic name --- Name of the NGspice schematic

Freq_range --- Specify the frequency range for frequency analysis

Terminal_imp --- Specify the terminal impedance

Input_signal ---- Specify the input signal"""

import numpy as np
import subprocess as sb
from mpmath import mpf
import matplotlib.pyplot as plt
import sys
import time
from subprocess import call
import time
import os

class genericTF():
    
    """ The Generic Transfer function class defines all the generic TF parameters"""
    
    """ Trafo settings can be stored in an external file and retrieved"""

    def __init__(self,*args,**kwargs):
        """ Instantiation behaviour for the beam class, the arguments can be file name with beam parameters, a dictionary object or a list of beam parameters """
        
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
        elif len(args) == 5:
            self.parameters = {}
            self.parameters["Schematic"]= args[0] # .cir extension
            self.parameters["Freq_range"] = args[1]
            self.parameters["Terminal_imp"] = args[2]
            self.parameters["Input_signal"] = args[3] #Input signal
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
           # print ("Throw exception")

        if self.parameters["Terminal_imp"] == None:
            print ("Terminal impedance is not defined")
           # print ("Throw exception")
        if self.parameters["Terminal_imp"] is True:
            trans_para2 = open("Circuits/Terminal_imp.txt","w")  #open file to write terminal impedance
            trans_para2.write("Rt 2 0"+" "+self.parameters["Terminal_imp"])
            
        if self.parameters["Input_signal"] is True:
            Input_para = open("Circuits/Input_signal.txt","w")
            Input_para.write(".model filesrc filesource (file="+'"'+self.parameters["Input_signal"]+'"'+")")

        self.parameters["No_of_plots"] = len(self.parameters['Voltage_nodes'])
        plotng = open("plotng.txt","w")
        time.sleep(2)
        for N in range(0,int(self.parameters["No_of_plots"])):
            plotng.write("wrdata Circuits/plot"+str(N)+" "+self.parameters['Voltage_nodes'][N]+'\n')
        #self.Schematic = input("schematic")
            
        # Calculate all the internal parameters
        trans_para1 = open("Circuits/freq_analysis.txt","w")  #open file to write freq range
        trans_para1.write("AC DEC 101"+" "+self.parameters["Freq_range"])
        
        
    def NGspice(self):
        timeout_NGspice = 50
        """ this function will invoke NGspice and shows the output from NGspice"""
        try:
            proc=sb.check_call(["gnome-terminal","--command=ngspice"+" "+ self.parameters["Schematic"]],timeout=timeout_NGspice,shell = False)
        except subprocess.TimeoutExpired:
            print("NG SPICE ran too long, check circuit file")
        else:
            print("NG SPICE run successful, the PID is %f",proc)
        #proc.terminate()    
       # time.sleep(4)  #give some time to NGspice
        self.mag = [line.rstrip('\n') for line in open('Circuits/plot0.data')] #Getting data generated by NGspice in appropriate format for plotting 
        self.line1 = [line.split() for line in open('Circuits/plot0.data',"r")]
        self.xpt1 = 0*np.ones(len(self.mag))
        self.ypt1 = 0*np.ones(len(self.mag))
        for i in range(len(self.mag)):
            self.xpt1[i] = float(self.line1[i][0])
            self.ypt1[i] = float(self.line1[i][1])
        plt.figure(1)
        plt.subplot(211)
        plt.plot(self.xpt1,self.ypt1,'r--')
        plt.xscale('log')
        plt.xlabel('Frequency f/Hz')
        plt.ylabel('Magnitude')

        self.phase = [line.rstrip('\n') for line in open('Circuits/plot1.data')] #Getting data generated by NGspice in appropriate format for plotting 
        self.line2 = [line.split() for line in open('Circuits/plot1.data',"r")]
        self.xpt2 = 0*np.ones(len(self.phase))
        self.ypt2 = 0*np.ones(len(self.phase))
        for i in range(len(self.mag)):
            self.xpt2[i] = float(self.line2[i][0])
            self.ypt2[i] = float(self.line2[i][1])
        plt.subplot(212)
        plt.plot(self.xpt2,(180/np.pi)*self.ypt2,'g^')
        plt.xscale('log')
        plt.xlabel('Frequency f/Hz')
        plt.ylabel('Phase')
        plt.show()
        
        # Print all the class instance variables
        
        os.remove("plotng.txt")
        if self.parameters["Terminal_imp"] is True:
            os.remove("Circuits/Terminal_imp.txt")
        if self.parameters["Input_signal"] is True:
            os.remove("Circuits/Input_signal.txt")
        os.remove("Circuits/freq_analysis.txt")
        #for key in self.parameters:
        #    print (key, '\t', self.parameters[key])
        
    def save(self,name_of_file,description):
        
        """ This function will save the beam object to an external file in the directory called "defined_beams" in the source directory"""
        
        dir = os.path.dirname(__file__)
        current_module = __name__
        rel_dir_name = 'defined_'+current_module+'s'
        filename = os.path.join(dir,rel_dir_name,name_of_file)
        if os.path.isfile(filename) == True:
            in_keyboard = input("Filename specified" + name_of_file + "already exists, do you want to overwrite, yes [y] or no [n]?")
            if in_keyboard == 'n':
                name_of_file = input('Enter new file name')
            filename = os.path.join(dir,rel_dir_name,name_of_file)
            if os.path.isfile(filename) == True:
                print('Gave the same file name again, overwriting the file!!!!!')
        else:
            writer = csv.writer(open(filename, 'w'))
            writer.writerow('Description',description)
            for key, value in self.parameters.items():
                writer.writerow([key, value])
            print (" Successfully written at"+ filename)
             
    def load(self,name_of_file):
        dir = os.path.dirname(__file__)
        current_module = str(__name__)
        rel_dir_name = 'defined_'+current_module+'s'
        filename = os.path.join(dir,rel_dir_name,name_of_file)
        if os.path.isfile(filename) == False:
            print('Specified file '+filename+' to read beam parameter does not exist')
            exit()
        else:
            reader = csv.reader(open(filename, 'r'))
            description = next(reader)
            temp = dict(x for x in reader) 
        return temp
        
        
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

if __name__ == "__main__":
    dict_tf = {'Schematic':'Circuits/transfunc.cir', 'Freq_range':'1 1000MEG','Terminal_imp':None,'Input_signal':None, 'Voltage_nodes':['mag(v(2))', 'phase(v(2))']}
    tf = genericTF(**dict_tf)
    tf.NGspice()
