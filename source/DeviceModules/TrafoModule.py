#!/usr/bin/python
""" Generic Trafo module takes beam and machine object and returns the TrafoOut

The module takes the following arguments

Beam --- Beam object fully specifying the beam

Machine --- Accelerator setting object

TrafoType (Optional) --- Specific transformer types to define exact Trafo behaviour  """

# meta info
__author__ = 'Rahul Singh'
__email__ = 'r.singh@gsi.de'
__version__ = '-1.0'
__lastchanged__ ='13072015'


import os
import sys
import inspect
import csv
import beam
import machine
import numpy as np
from mpmath import mpf

# Typical beam parameters

class generictrafo():
    
    """ The Generic trafo class defines all the generic trafo parameters"""
    
    """ Trafo settings can be stored in an external file and retrieved"""

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
        elif len(args) == 7:
            self.parameters = {}
            self.parameters["Torus_radii"]= args[0] # List with inner and outer radii of Torus
            self.parameters["Torus_thickness"] = args[1] # Thickness of the Torus
            self.parameters["Torus_permeability"] = args[2] # Permeability of the Torus
            self.parameters["Num_windings"] = args[3] # NUmber of windings
            self.parameters["Output_resistance"] = args[4] # Resistance across which voltage is measured (in Ohm)
            self.parameters["Stray_capacitance"] = args[5] # Stray capacitance (in pF)
            self.parameters["Magnetic_noise"] = args[6] # Average Machine dispersion

        else:
            print('You have the wrong number of arguments, Please use help...')
        
        
        # Check if the some parameters are not defined or assigned to None or have the wrong type
        
        if self.parameters["Torus_radii"] == None:
            print ("Torus_radii is not defined")
            print ("Throw exception")
        if type(self.parameters["Torus_radii"][0]) != 'float':
            self.parameters["Torus_radii"][0] = float(self.parameters["Torus_radii"][0])
            self.parameters["Torus_radii"][1] = float(self.parameters["Torus_radii"][1])
        if self.parameters["Torus_thickness"] == None:
            print ("Torus_thickness is not defined")
            print ("Throw exception")
        if type(self.parameters["Torus_thickness"]) != 'float':
            self.parameters["Torus_thickness"] = float(self.parameters["Torus_thickness"])
        if self.parameters["Torus_permeability"] == None:
            print ("Torus_permeability is not defined")
            print ("Throw exception")
        if type(self.parameters["Torus_permeability"]) != 'float':
            self.parameters["Torus_permeability"] = float(self.parameters["Torus_permeability"])
        if self.parameters["Output_resistance"] == None:
            print ("Output_resistance is not defined")
        if type(self.parameters["Output_resistance"]) != 'float':
            self.parameters["Output_resistance"] = float(self.parameters["Output_resistance"])
        if self.parameters["Num_windings"] == None:
            print ("Num_windings is not defined")
            print ("Throw exception")
        if type(self.parameters["Num_windings"]) != 'int':
            self.parameters["Num_windings"] = int(self.parameters["Num_windings"])
        if self.parameters["Stray_capacitance"] == None:
            print ("Stray_capacitance is not defined")
        if type(self.parameters["Stray_capacitance"]) != 'float':
            self.parameters["Stray_capacitance"] = float(self.parameters["Stray_capacitance"])
            
            
        # Calculate all the internal parameters
        self.parameters['Inductance'] = self.parameters["Torus_permeability"]*beam.PERMEABILITY_SPACE* self.parameters["Torus_thickness"]*np.power(self.parameters["Num_windings"],2)*np.log(self.parameters["Torus_radii"][1]/self.parameters["Torus_radii"][0])/(2*np.pi)
        self.parameters['rise_time'] = self.parameters["Output_resistance"]*self.parameters["Stray_capacitance"]
        self.parameters['droop_time'] = self.parameters["Inductance"]/self.parameters["Output_resistance"]
        self.parameters['sensitivity'] = self.parameters["Output_resistance"]/self.parameters["Num_windings"]
        
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
        """ Loads the specific trafo settings """
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
        """ Calculates the output of the device module or the system """
        output_dict = {}
        voltage_sensor = self.parameters['sensitivity']*observable_in.parameters['current'] # Only scalar at present, play with FFT and inverse later
        voltage_sensor_profile = self.parameters['sensitivity']*observable_in.parameters['current_profile'] 
        #print (voltage_sensor)
        voltage_DA1 = voltage_sensor*(self.parameters['DA1']).parameters['Gain'][0]
        #print (voltage_DA1)
        noise_voltage_DA1 = np.sqrt((self.parameters['DA1']).parameters['Bandwidth'][0]*mpf(1e-6))*(self.parameters['DA1']).parameters['Input_noise']*(self.parameters['DA1']).parameters['Gain'][0]
        noise_profile = [np.random.normal(0,noise_voltage_DA1) for x in range(0, len(voltage_sensor_profile))]
        voltage_sensor_profile= voltage_sensor_profile + noise_profile
        #print (noise_voltage_DA1)
        if voltage_DA1 > (self.parameters['DA2']).parameters['ADC_maximum'][0]:
            #voltage_DA2 = (self.parameters['DA2']).parameters['ADC_maximum'][0]
            #print (" ADC is saturated ")
            voltage_DA2 = voltage_DA1
        elif voltage_DA1 < (self.parameters['DA2']).parameters['ADC_minimum'][0]:
            #voltage_DA2 = (self.parameters['DA2']).parameters['ADC_minimum'][0]
            #print (" ADC is saturated ")
            voltage_DA2 = voltage_DA1
        else:
            voltage_DA2 = voltage_DA1
            
        noise_voltage_DA2 = noise_voltage_DA1
        return [voltage_DA2,noise_voltage_DA2,voltage_sensor_profile]
        
    
    def optimize(self,observable_in,constraints):
        """ Predicts optimal settings for all the variable parameters in the device module, common module or any combination """
        
        """ First is a brute force method """
        
        Output = constraints["Output"]
        present_output = self.output(observable_in)
        print ("Optimize the ", constraints["Amp"][0], "setting\n" )
        print ("Initial "+ constraints["Amp"][0] + " setting", (self.parameters['DA1']).parameters[constraints["Amp"][0]][0])
        setting1 = (self.parameters['DA1']).parameters[constraints["Amp"][0]][0]
        counter = 0 # Avoid run-aways
        while (setting1 < (self.parameters['DA1']).parameters[constraints["Amp"][0]][2] and setting1 > (self.parameters['DA1']).parameters[constraints["Amp"][0]][1]):
            counter = counter + 1
            if Output[0][0] - present_output[0] >= Output[0][1]:
                setting1 = setting1*(self.parameters['DA1']).parameters[constraints["Amp"][0]][3]
                (self.parameters['DA1']).parameters[constraints["Amp"][0]][0] = setting1
                present_output = self.output(observable_in)
                if Output[0][0]- present_output[0] < Output[0][1]:
                    break
            if Output[0][0]- present_output[0] < -1*Output[0][1]:
                setting1 = setting1/(self.parameters['DA1']).parameters[constraints["Amp"][0]][3]
                (self.parameters['DA1']).parameters[constraints["Amp"][0]][0] = setting1
                present_output = self.output(observable_in)
                if Output[0][0]- present_output[0] > -1*Output[0][1]:
                    break
                    
            else:
                print ('Fine setting')
                break
                
            if counter > 100: # Just in case
                break
        print ("Final "+ constraints["Amp"][0] + " setting", (self.parameters['DA1']).parameters[constraints["Amp"][0]][0],"\n")
        #print (self.output(observable_in))
        
        print ("Optimize the ",constraints["Amp"][1], "setting\n" )
        print ("Initial "+ constraints["Amp"][1] + " setting", (self.parameters['DA1']).parameters[constraints["Amp"][1]][0])
        setting1 = (self.parameters['DA1']).parameters[constraints["Amp"][1]][0]
        counter = 0 # Avoid run-aways
        while (setting1 < (self.parameters['DA1']).parameters[constraints["Amp"][1]][2] and setting1 > (self.parameters['DA1']).parameters[constraints["Amp"][1]][1]):
            counter = counter + 1
            if present_output[1] >= Output[1][0]:
                setting1 = setting1/(self.parameters['DA1']).parameters[constraints["Amp"][1]][3]
                (self.parameters['DA1']).parameters[constraints["Amp"][1]][0] = setting1
                present_output = self.output(observable_in)
                if present_output[1] < Output[1][0]:
                    break
            elif present_output[1] < Output[1][0]/Output[1][1]:
                setting1 = setting1*(self.parameters['DA1']).parameters[constraints["Amp"][1]][3]
                (self.parameters['DA1']).parameters[constraints["Amp"][1]][0] = setting1
                present_output = self.output(observable_in)
                if present_output[1] > Output[1][0]/Output[1][1]:
                    break
            else:
                print ('Fine setting')
                break
                
            if counter > 100: # Just in case
                break
                
        
        print ("Final "+ constraints["Amp"][1] + " setting", (self.parameters['DA1']).parameters[constraints["Amp"][1]][0],"\n")
        #print (self.output(observable_in))
        return [(self.parameters['DA1']).parameters[constraints["Amp"][0]][0],(self.parameters['DA1']).parameters[constraints["Amp"][1]][0]]
        
        #bandwidth = (self.parameters['DA1']).parameters['Bandwidth'][0]
        #while (bandwidth > (self.parameters['DA1']).parameters['Bandwidth'][2] and (gain > (self.parameters['DA1']).parameters['Bandwidth'][1]):
        
        
        """ Second would use convex optimization """
        
        
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
