#!/usr/bin/python
"""Generic filter design module

The modules takes the follwing arguements

Input signal --- input signal file

Resisitor --- input amplifier resistance value

Capacitance --- pick up capacitance value

Beta --- beam velocity

Area --- area of a plate

distance = distance from the beam center

"""
# meta info
__author__ = 'Rajesh Asutkar'
__email__ = 'asutkarrajesh@sggs.ac.in'
__version__ = '-1.0'
__lastchanged__ ='24082015'


import numpy as np
import subprocess
#from mpmath import mpf
#import mpmath
import matplotlib.pyplot as plt
import sys
import time
from subprocess import call
import os
from scipy.signal import freqs
import scipy.signal as signal
from scipy.fftpack import fft,fftshift,ifft
from random import gauss

c = 3.0e8 
class gen_filter():

    """ The gen_filter class design a filter for defined parameters"""

    def __init__(self,*args,**kwargs):

        """It takes the Input_siganl,R,C,A,beta,a"""

        if len(args) == 0:
            self.parameters = {}
            self.parameters = kwargs
        elif len(args) == 7:
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
        elif len(args) == 7:
            self.parameters = {}
            self.parameters["Res"]= args[0] # Resistance in ohm
            self.parameters["Cap"] = args[1] # capacitance in F
            self.parameters["Area"] = args[3] # Area in m2
            self.parameters["a_dist"] = args[4] # distance in m
            self.parameters["beta"] = args[5] # beta
            self.parameters["Input_signal"] = args[6] # input file
        else:
            print('You have the wrong number of arguments, Please use help...')

        if type(self.parameters["Res"]) != 'int':
           self.parameters["Res"] = int( self.parameters["Res"])
        if type(self.parameters["Cap"]) != 'float':
           self.parameters["Cap"] = float( self.parameters["Cap"])
        if type(self.parameters["Area"]) != 'float':
           self.parameters["Area"] = float( self.parameters["Area"])
        if type(self.parameters["a_dist"]) != 'float':
           self.parameters["a_dist"] = float( self.parameters["a_dist"])
        if type(self.parameters["beta"]) != 'float':
           self.parameters["beta"] = float( self.parameters["beta"])
        if self.parameters["Input_signal"] == None:
            print ("Input signal is not defined")
            print ("Throw exception")
       # if self.parameters["Input_signal"] is True:
            

    def filter_design(self):

        self.mag = [line.rstrip('\n') for line in open(self.parameters['Input_signal'])]
        self.line1 = [line.split() for line in open(self.parameters['Input_signal'],"r")]
        self.xpt1 = 0*np.ones(len(self.mag))
        self.ypt1 = 0*np.ones(len(self.mag))
        for i in range(len(self.mag)):
            self.xpt1[i] = float(self.line1[i][0])
            self.ypt1[i] = float(self.line1[i][1])

        self.const = (1/(self.parameters['beta']*c))*(1/(self.parameters['Cap']))*(self.parameters['Area']/2*np.pi*self.parameters['a_dist'])

        self.b = self.const*np.array([self.parameters['Res']*self.parameters['Cap'],0.0])    #Numerator
        self.a = np.array([self.parameters['Res']*self.parameters['Cap'],1.0])    #Denominator

        #print signal.tf2zpk(self.b, self.a)
        self.w, self.h = signal.freqs(self.b, self.a,worN=np.logspace(0, 10, 5000))
        
        plt.title('Analog filter frequency response')
        plt.figure(1)   
        plt.subplot(211)
        plt.plot(self.w, (np.abs(self.h)))
        plt.xscale('log')
        plt.ylabel('Amplitude Response')
        plt.xlabel('Frequency')
        plt.grid()
        plt.subplot(212)
        plt.plot(self.w, ((180/np.pi)*np.angle(self.h)))
        plt.xscale('log')
        plt.ylabel('phase Response')
        plt.xlabel('Frequency')
        plt.grid()
        
        plt.figure(2)
        #print self.w
        plt.subplot(211)
        plt.plot(self.xpt1,self.ypt1)
        #plt.xscale('log')
        #self.window = np.random.normal(0.5e-6, 100.0e-9, 10000) #gaussian fun
        #self.window = signal.gaussian(1000, std=50)
        #self.tim1 = np.arange(0,1.0e-6,1.0e-9)
        #plt.plot(self.tim1,self.window)
        #plt.title("Gaussian")
        #plt.ylabel("Amplitude")
        #plt.xlabel("Sample")

        A = fft(self.ypt1) #/ (len(self.window)/2.0)  #fft of Iput signal
        #freq = np.linspace(-10.0, 10.0, len(A))
        #response = np.abs(fftshift(A / abs(A).max()))
        plt.subplot(212)
        #self.tim2 = np.arange(0,10.0e6,10.0e3)
        plt.plot(1/self.xpt1,abs(A))
        #plt.xscale('log')
        #plt.axis([-0.5, 0.5, -120, 0])
        #plt.grid()
        plt.figure(3)
        U = self.h*A
        N = ifft(U)             #inverese FFT
        #plt.subplot(211)
        #self.timr = np.arange(0,1.0e-6,1.0e-8)
        #plt.plot(self.xpt1,self.ypt1)
        #plt.subplot(212)
        plt.plot(self.xpt1,N)
        plt.show()

dict_tf = {'Res':'50', 'Cap':'100e-12','Area':'50e-4','Input_signal':'current_profile.txt', 'a_dist':'50e-3', 'beta':'0.5'}

filt = gen_filter(**dict_tf)
filt.filter_design()
