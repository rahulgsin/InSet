#!/usr/bin/python
""" Beam position measurement(BPM) module takes beam and machine object and returns the beam position

The module takes the following arguments

Beam --- Beam object fully specifying the beam

Machine --- Accelerator setting object

bpm_Type --- button or shoe type """

# meta info
__author__ = 'Rajesh Asutkar'
__email__ = 'r.asutkar@gsi.de'
__version__ = '-1.0'
__lastchanged__ ='23072015'


import os
import sys
import inspect
import csv
import beam
import machine
import numpy as np
from mpmath import mpf
from scipy import integrate

# Typical beam parameters

class parainfo():
    
    """ The parainfo class defines all the pick up related parameters"""
    
    """ bpm settings can be stored in an external file and retrieved"""

    def __init__(self,*args,**kwargs):
        """ Instantiation behaviour for the beam class, the arguments can be file name with beam parameters, a dictionary object or a list of beam parameters """
        # 
        #print (len(argspec[2])
        if len(args) == 0:
            self.parameters = {}
            self.parameters = kwargs
        elif len(args) == 1:
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
        elif len(args) == 13:
            self.parameters = {}
            self.parameters["Position_sensitivity_x"]= args[0] # In %/mm
            self.parameters["Position_sensitivity_y"]= args[1] # In %/mm
            self.parameters["half_aperture"] = args[2] # In m
            self.parameters["Area_plate"] = args[3] # area of plate
            self.parameters["Beam_vel"] = args[4] # beam velocity
            self.parameters["Capacitance"] = args[5] # In farad
            self.parameters["acc_freq"] = args[6] # accelarating frq
            self.parameters["Resistance"] = args[7] # Resistane value
            self.parameters["beam_pipe_R"] = arg[8] #beam pipe radius
            self.parameters["displacement"] = arg[9] # amount by which beam is located off-center
            self.parameters["theta"] = arg[10] #angle of deflection
            self.parameters["ang_cov"] = arg[11] #anglular coverage
           # self.parameters["phi"] = arg[11] # angle of deflection
            self.parameters["bpm_type"] = arg[12] #type of bpm
            
        else:
            print('You have the wrong number of arguments, Please use help...')
        
        
        # Check if the some parameters are not defined or assigned to None or have the wrong type
        
        if self.parameters["Position_sensitivity_x"] == None:
            print ("Position_sensitivity_x is not defined")
            print ("Throw exception")
        if type(self.parameters["Position_sensitivity_x"]) != 'float':
            self.parameters["Position_sensitivity_x"] = float(self.parameters["Position_sensitivity_x"])
        if self.parameters["Position_sensitivity_y"] == None:
            print ("Position_sensitivity_y is not defined")
            print ("Throw exception")
        if type(self.parameters["Position_sensitivity_y"]) != 'float':
            self.parameters["Position_sensitivity_y"] = float(self.parameters["Position_sensitivity_y"])
        if type(self.parameters["beam_type"]) != 'str':
            self.parameters["beam_type"] = str(self.parameters["beam_type"])
        # Calculate all the internal parameters
       
        
        # Print all the class instance variables
        
        #for key in self.parameters:
        #    print (key, '\t', self.parameters[key])
        
    def save(self,name_of_file,description):
        
        """ This function will save the beam object to an external file in the directory called "defined_beams" in the source directory"""
        
        dir = os.path.dirname(__file__)
        current_module = __name__
        path= current_module.split('.')
        rel_dir_name = 'defined_'+path[1]+'s'
        filename = os.path.join(dir,rel_dir_name,name_of_file)
        if os.path.isfile(filename) == True:
            in_keyboard = input("Filename specified" + name_of_file + "already exists, do you want to overwrite, yes [y] or no [n]?")
            if in_keyboard == 'n':
                name_of_file = input('Enter new file name')
            filename = os.path.join(dir,rel_dir_name,name_of_file)
            if os.path.isfile(filename) == True:
                print('Gave the same file name again, overwriting the file!!!!!')
                writer = csv.writer(open(filename, 'w'))
                writer.writerow(['Description',description])
                for key, value in self.parameters.items():
                    writer.writerow([key, value])
                print (" Successfully written at"+ filename)
        else:
            writer = csv.writer(open(filename, 'w'))
            writer.writerow(['Description',description])
            for key, value in self.parameters.items():
                writer.writerow([key, value])
            print (" Successfully written at"+ filename)
             
    def load(self,name_of_file):
        """ Loads the specific bpm settings """
        dir = os.path.dirname(__file__)
        current_module = str(__name__)
        path= current_module.split('.')
        rel_dir_name = 'defined_'+path[1]+'s'
        filename = os.path.join(dir,rel_dir_name,name_of_file)
        if os.path.isfile(filename) == False:
            print('Specified file '+filename+' to read beam parameter does not exist')
            exit()
        else:
            reader = csv.reader(open(filename, 'r'))
            temp = dict(x for x in reader) 
        return temp
        
    def combine_systems(self, *args, **kwargs):
        """ Combines all the subsystems to the sensor """
        # First append the common module parameters to the sensor parameters
        i=1
        for arg in args:
            index = 'DA'+ str(i) 
            self.parameters[index] = args[i-1]
            i=i+1
            
        # Get a list of optimizable parameters and their range
        # Confirm the object types to be combined

    def output(self,observable_in):
        #calculate the desired output for specific type of BPM method
        if parainfo.parameters['bpm_type'] is 'shoe_pickup':
            self.x = parainfo.parameter['half_aperture']*(button_pickup.parameters['Uright']-button_pickup.parameters['Uleft'])/(button_pickup.parameters['Uright']+button_pickup.parameters['Uleft'])
            self.y = parainfo.parameter['half_aperture']*(button_pickup.parameters['Uup']-button_pickup.parameters['Udown'])/(button_pickup.parameters['Uup']+button_pickup.parameters['Udown'])
        elif parainfo.parameters['bpm_type'] is 'button_pickup':
            self.x = (shoe_pickup.parameters[U2]+shoe_pickup.parameters[U4])-(shoe_pickup.parameters[U1]+shoe_pickup.parameters[U3])/(shoe_pickup.parameters[U1]+shoe_pickup.parameters[U2]+shoe_pickup.parameters[U3]+shoe_pickup.parameters[U4])
            self.Y = (shoe_pickup.parameters[U1]+shoe_pickup.parameters[U2])-(shoe_pickup.parameters[U3]+shoe_pickup.parameters[U4])/(shoe_pickup.parameters[U1]+shoe_pickup.parameters[U2]+shoe_pickup.parameters[U3]+shoe_pickup.parameters[U4])
        else:
            print("please type the correct type name: shoe_pickup or button_pickup")
    def __repr__(self):
 	       return "%s(%r)" % (self.__class__, self.__dict__) 

        #capacitive pickup class
#p = pickupinfo()
#b = button_pickup()
#s = shoe_pickup()
""" 
class capacitive_pickup(p):
    def __init__(self,observable_in):
        self.parameters['Uright'] = (p.parameters['Area_plate']*p.parameters['acc_freq']*p.parameters['Resistance']*p.parameters['Capacitance']*observable_in.parameters['current']*1j)/(p.parameters['Beam_vel']*p.parameters['half_aperture']*2*np.pi*(1+1j*p.parameters['acc_freq']*p.parameters['Resistance']*p.parameters['Capacitance'])*beam.VEL_LIGHT)
        self.parameters['Uleft']  = (p.parameters['Area_plate']*p.parameters['acc_freq']*p.parameters['Resistance']*p.parameters['Capacitance']*observable_in.parameters['current']*1j)/(p.parameters['Beam_vel']*p.parameters['half_aperture']*2*np.pi*(1+1j*p.parameters['acc_freq']*p.parameters['Resistance']*p.parameters['Capacitance'])*beam.VEL_LIGHT)
        self.parameters['Uup']    = (p.parameters['Area_plate']*p.parameters['acc_freq']*p.parameters['Resistance']*p.parameters['Capacitance']*observable_in.parameters['current']*1j)/(p.parameters['Beam_vel']*p.parameters['half_aperture']*2*np.pi*(1+1j*p.parameters['acc_freq']*p.parameters['Resistance']*p.parameters['Capacitance'])*beam.VEL_LIGHT)
        self.parameters['Udown']  = (p.parameters['Area_plate']*p.parameters['acc_freq']*p.parameters['Resistance']*p.parameters['Capacitance']*observable_in.parameters['current']*1j)/(p.parameters['Beam_vel']*p.parameters['half_aperture']*2*np.pi*(1+1j*p.parameters['acc_freq']*p.parameters['Resistance']*p.parameters['Capacitance'])*beam.VEL_LIGHT)
        #calculate positions
        self.x = (self.parameters['Uright']-self.parameters['Uleft'])/(p.parameters['Position_sensitivity_x']*(self.parameters['Uright']+self.parameters['Uleft']))
        self.y = (self.parameters['Uup']-self.parameters['Udown'])/(p.parameters['Position_sensitivity_y']*(self.parameters['Uup']+self.parameters['Udown']))
"""

class shoe_pickup(parainfo):

    """ This class calculate voltages for shoe pickup type BPM'S"""

    def __init__(self,observable_in):
        self.parameters['Uright'] = (p.parameters['Area_plate']*p.parameters['acc_freq']*p.parameters['Resistance']*p.parameters['Capacitance']*observable_in.parameters['current']*1j)/(p.parameters['Beam_vel']*p.parameters['half_aperture']*2*np.pi*(1+1j*p.parameters['acc_freq']*p.parameters['Resistance']*p.parameters['Capacitance'])*beam.VEL_LIGHT)
        self.parameters['Uleft']  = (p.parameters['Area_plate']*p.parameters['acc_freq']*p.parameters['Resistance']*p.parameters['Capacitance']*observable_in.parameters['current']*1j)/(p.parameters['Beam_vel']*p.parameters['half_aperture']*2*np.pi*(1+1j*p.parameters['acc_freq']*p.parameters['Resistance']*p.parameters['Capacitance'])*beam.VEL_LIGHT)
        self.parameters['Uup']    = (p.parameters['Area_plate']*p.parameters['acc_freq']*p.parameters['Resistance']*p.parameters['Capacitance']*observable_in.parameters['current']*1j)/(p.parameters['Beam_vel']*p.parameters['half_aperture']*2*np.pi*(1+1j*p.parameters['acc_freq']*p.parameters['Resistance']*p.parameters['Capacitance'])*beam.VEL_LIGHT)
        self.parameters['Udown']  = (p.parameters['Area_plate']*p.parameters['acc_freq']*p.parameters['Resistance']*p.parameters['Capacitance']*observable_in.parameters['current']*1j)/(p.parameters['Beam_vel']*p.parameters['half_aperture']*2*np.pi*(1+1j*p.parameters['acc_freq']*p.parameters['Resistance']*p.parameters['Capacitance'])*beam.VEL_LIGHT)
        
class button_pickup(parainfo):

    """ This class calculate voltages for button pickup type BPM'S"""
    
    def __init__(self,observable_in):
        #calculate image current density 
        self.Jim = lambda phi: (observable_in.parameters['current']*(p.parameters['beam_pipe_R']**2-p.parameters['displacement']**2))/2*np.pi*p.parameters['beam_pipe_R']*((p.parameters['beam_pipe_R']**2+p.parameters['displacement']**2)-2*p.parameters['beam_pipe_R']*p.parameters['displacement']*cos(phi-p.parameters['theta']))
        #calculte image current
        self.Iim = p.parameters['beam_pipe_R']*integrate.quad(Jim,-p.parameter['ang_cov']/2,p.parameter['ang_cov']/2)
        self.parameters[U1] = self.Iim*p.parameters['Resistance']
        self.parameters[U2] = self.Iim*p.parameters['Resistance']
        self.parameters[U3] = self.Iim*p.parameters['Resistance']
        self.parameters[U4] = self.Iim*p.parameters['Resistance']
        
