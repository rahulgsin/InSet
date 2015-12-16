#!/usr/bin/python
"""Generic filter design module

The modules takes the follwing arguements

Input signal --- input signal file

Resisitor --- input amplifier resistance value

Capacitance --- pick up capacitance value

"""
# meta info
__author__ = 'Rajesh Asutkar'
__email__ = 'asutkarrajesh@sggs.ac.in'
__version__ = '-1.0'
__lastchanged__ ='25082015'

import cmath
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
 
class iir_filter():

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
        elif len(args) == 3:
            self.parameters = {}
            self.parameters["Res"]= args[0] # Resistance in ohm
            self.parameters["Cap"] = args[1] # capacitance in F
            self.parameters["Input_signal"] = args[2] # input file
        else:
            print('You have the wrong number of arguments, Please use help...')

        if type(self.parameters["Res"]) != 'float':
           self.parameters["Res"] = float( self.parameters["Res"])
        if type(self.parameters["Cap"]) != 'float':
           self.parameters["Cap"] = float( self.parameters["Cap"])
        if self.parameters["Input_signal"] == None:
            print ("Input signal is not defined")
            print ("Throw exception")
       #calculate cut off frequency
        
    def filter_design(self):

        self.mag = [line.rstrip('\n') for line in open(self.parameters['Input_signal'])]
        self.line1 = [line.split() for line in open(self.parameters['Input_signal'],"r")]
        self.xpt1 = 0*np.ones(len(self.mag))
        self.ypt1 = 0*np.ones(len(self.mag))
        for i in range(len(self.mag)):
            self.xpt1[i] = float(self.line1[i][0])
            self.ypt1[i] = float(self.line1[i][1])
        Fs = 1.0e9
        plt.figure(1)
        plt.plot(self.xpt1,self.ypt1)
        self.Fcut = 1/(2*np.pi*self.parameters['Res']*self.parameters['Cap'])
        
        self.Fcutnorm = self.Fcut/(Fs*2)
                
        self.b1 = signal.firwin(301,self.Fcutnorm,pass_zero=False)
        #self.b1 = signal.remez(301,[0,self.Fcut-500,self.Fcut,Fs],[0,1],Hz=2*Fs,type='bandpass')
        #self.b,self.a = signal.iirfilter(10,self.Fcutnorm,rp=4,rs=60,btype='high',ftype='butter')
        self.w,self.h = signal.freqz(self.b1,worN=5000)
        
        plt.title('Analog filter frequency response')
        plt.figure(2)   
        plt.subplot(211)
        plt.plot(self.w*Fs,abs(self.h))

    
        plt.xscale('log')
        #plt.yscale('log')
        plt.ylabel('Amplitude Response')
        plt.xlabel('Frequency')
        plt.grid()
        plt.subplot(212)
        #self.angles = np.unwrap(np.angle(self.h))
        plt.plot(self.w*Fs,np.angle(self.h))
        #plt.xscale('log')
        plt.ylabel('phase Response')
        plt.xlabel('Frequency')
        plt.grid()
        plt.hold(True)
        phi = np.angle(self.h)
        phi2 = np.angle(self.xpt1)
        print phi
        self.output = self.h.real*self.ypt1
        for i in range(len(self.output)):
            self.h[i] = cmath.rect(self.output[i],phi[i])

        #plt.figure(3)
        #plt.plot(self.w*Fs,np.angle(self.output))
        plt.figure(3)
        plt.plot(self.xpt1,self.ypt1,self.xpt1,-self.h.imag)

        #import ngplot
        plt.legend(['I_beam(t)','U_im(t)'],loc= 'upper right')
        plt.ylabel('V or I')
        plt.xlabel('time')
        plt.grid()
        plt.show()

dict_tf = {'Res':'1e6', 'Cap':'100e-12','Input_signal':'current_profile.txt'}

filt = iir_filter(**dict_tf)
filt.filter_design()
