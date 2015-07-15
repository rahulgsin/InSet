#!/usr/bin/python
""" This module defines the beam object

The module takes the following arguments

Property --- Key --- Value type --- Description

Circumference --- circumference --- Float --- Circumference of the machine

Compaction factor --- com_fact --- Float --- Momentum compaction factor

Set tune --- set_tune --- List of Float --- Horizontal and vertical tune

Set Chromaticity --- set_chro --- List of float --- Horizontal and vertical chromaticity """

# meta info
__author__ = 'Rahul Singh'
__email__ = 'r.singh@gsi.de'
__version__ = '-1.0'
__lastchanged__ ='13072015'


import os
import sys
import inspect
import csv

# Typical beam parameters

class staticmachine():
    
    """ The machine class defines all the machine parameters"""
    
    """ Machine settings can be stored in an external file and retrieved"""

    def __init__(self,*args,**kwargs):
        """ Instantiation behaviour for the beam class, the arguments can be file name with beam parameters, a dictionary object or a list of beam parameters """
        # 
        argspec = inspect.getargspec(staticmachine)
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
        elif len(args) == 10:
            self.parameters = {}
            self.parameters["Type"]= args[0] # Machine Type
            self.parameters["Length"] = args[1] # Machine Length
            self.parameters["Tr_gamma"] = args[2] # Relativistic Gamma at transition
            self.parameters["Impedances"] = args[3] # Transverse and longitudinal impedances
            self.parameters["Set_tune"] = args[4] # Set tune
            self.parameters["Set_chromaticity"] = args[5] # Set chromaticity
            self.parameters["Dispersion"] = args[6] # Average Machine dispersion
            self.parameters["Lattice_Settings"] = args[7] # MAD output of lattice settings
            self.parameters["RF_parameters"] = args[8] # Cavity parameters
            self.parameters["Injection_settings"] = args[9] # Injection parameters, multi turn etc.
        else:
            print('You have the wrong number of arguments, Please use help...')
        
        
        # Check if the some parameters are not defined or assigned to None
        
        
        # Calculate all the internal machine parameters
        
        
        # Print the class instance variables
        
        for key in self.parameters:
            print (key, '\t', self.parameters[key])
        
    def save(self,name_of_file):
        
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
            temp = dict(x for x in reader) 
        return temp
        
        
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
    
class dynamicmachine():
    """This attributes are similar to a static beam, however, the beam energy, number of beam particles and beam structure is updated for several turns (depends on the length of list) and stored"""
    
    def __init__(self,*args,**kwargs):
        """ Instantiation behaviour for the beam class, the arguments can be file name with beam parameters, a dictionary object or a list of beam parameters """
        # 
        argspec = inspect.getargspec(dynamicmachine)
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
        elif len(args) == 10:
            self.parameters = {}
            self.parameters["Type"]= args[0] # Machine Type
            self.parameters["Length"] = args[1] # Machine Length
            self.parameters["Tr_gamma"] = args[2] # Relativistic Gamma at transition
            self.parameters["Impedances"] = args[3] # Transverse and longitudinal impedances
            self.parameters["Set_tune"] = args[4] # Set tune
            self.parameters["Set_chromaticity"] = args[5] # Set chromaticity
            self.parameters["Dispersion"] = args[6] # Average Machine dispersion
            self.parameters["Lattice_Settings"] = args[7] # MAD output of lattice settings
            self.parameters["RF_parameters"] = args[8] # Cavity parameters
            self.parameters["Injection_settings"] = args[9] # Injection parameters, multi turn etc.
        else:
            print('You have the wrong number of arguments, Please use help...')
        
        
        # Check if the some parameters are not defined or assigned to None
        
        for key in self.parameters:
            print (key, '\t', self.parameters[key])
        
    def save(self,name_of_file):
        
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
            temp = dict(x for x in reader) 
        return temp
        
        
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)