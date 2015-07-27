#!/usr/bin/python
""" This module defines the beam class 

The module takes the following arguments

Property --- Key --- Value Type --- Remarks

Particle type --- par_type --- String --- Ion type (p, U, Ar etc.)

Charge state --- charge_state --- Integer --- Charge state

Atomic mass --- atomic_mass ---  Integer --- 2 for Hydrogen

Particle energy --- kin_energy --- Float --- Kinetic energy per nucleon

Particle number ---par_num --- Integer --- Total number of particles (ions)

Distribution type --- d_type --- String --- a for arbitrary, p for parabolic, g for gaussian and kv for KV distribution

X Distribution ---- x_dist --- List of integers for 'a', two Ints for parabolic and gaussian --- Phase space distribution in x plane

Y Distribution ---- y_dist --- Same as X Dist. --- Phase space distribution in y plane

Z Distribution ---- z_dist --- Same as X Dist. --- Phase space distribution in z/s plane

 par_type=None, charge_state= None, atomic_mass = None, par_num= None, d_type = 'ggg', x_dist = [0,5], y_dist =[0,5], z_dist =[0,100]

The arguments can be passed in this order or by defining a dictionary or by calling a file where the parameters exist """

# meta info
__author__ = 'Rahul Singh'
__email__ = 'r.singh@gsi.de'
__version__ = '-1.0'
__lastchanged__ ='10072015'


import os
import sys
import inspect
import csv
import numpy as np
from mpmath import mpf
from matplotlib.pyplot import plot,subplot

# Global constants
PROTON_MASS = mpf(1.67e-27)  # Kg  removed e-30
VEL_LIGHT = mpf(3e8) # m/s
CHARGE = mpf(1.6e-19) # Coulomb removed e-30
PERMEABILITY_SPACE = mpf(1.256e-6)

# Typical beam parameters

class staticbeam():
    
    """ Beam class defines the static beam object 

    It creates a beam object instance the parameters in a special order are specified, or simply by passing a beam dictionary

    A save keyword 's' can be used to save the beam object in a file, which can be loaded later """


    def __init__(self,*args,**kwargs):
        """ Instantiation behaviour for the beam class, the arguments can be file name with beam parameters, a dictionary object or a list of beam parameters """
        # 
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
        elif len(args) == 9:
            self.parameters = {}
            self.parameters["par_type"]= args[0] # particle type
            self.parameters["charge_state"] = args[1] # charge state
            self.parameters["atomic_mass"] = args[2] # atomic mass
            self.parameters["kin_energy"] = args[3] # kinetic energy
            self.parameters["par_num"] = args[4] # particle number
            self.parameters["dist_type"] = args[5] # distibution type
            self.parameters["x_dist"] = args[6] # distibution type
            self.parameters["y_dist"] = args[7] # distibution type
            self.parameters["z_dist"] = args[8] # distibution type
        else:
            print('You have entered wrong number of arguments, Please use help...')
        
        
        # Check if the some parameters are not defined or assigned to None or have the wrong type
        
        if self.parameters["charge_state"] == None:
            print ("Charge State is not defined")
            print ("Throw exception")
        if type(self.parameters["charge_state"]) != 'int':
            self.parameters["charge_state"] = int(self.parameters["charge_state"])
        if self.parameters["atomic_mass"] == None:
            print ("Atomic mass is not defined")
            print ("Throw exception")
        if type(self.parameters["atomic_mass"]) != 'int':
            self.parameters["atomic_mass"] = int(self.parameters["atomic_mass"])
        if self.parameters["par_num"] == None:
            print ("Particle number is not defined")
            print ("Throw exception")
        if type(self.parameters["par_num"]) != 'float':
            self.parameters["par_num"] = float(self.parameters["par_num"])
        if self.parameters["kin_energy"] == None:
            print ("Kinetic energy is not defined")
        if type(self.parameters["kin_energy"]) != 'float':
            self.parameters["kin_energy"] = float(self.parameters["kin_energy"])
            
           
        # Calculate all the internal parameters
        
        self.parameters['gamma'] = 1 + (self.parameters['kin_energy']*10e6*CHARGE)/(PROTON_MASS*np.power(VEL_LIGHT,2))
        self.parameters['beta'] = np.sqrt(1-1/np.power(self.parameters['gamma'],2))
        
        self.parameters['x_range'] = np.arange(-1*self.parameters['x_dist'][2],self.parameters['x_dist'][2],2*self.parameters['x_dist'][2]/self.parameters['x_dist'][3])
        self.parameters['y_range']= np.arange(-1*self.parameters['y_dist'][2],self.parameters['y_dist'][2],2*self.parameters['y_dist'][2]/self.parameters['y_dist'][3])
        self.parameters['z_range'] = np.arange(-1*self.parameters['z_dist'][2],self.parameters['z_dist'][2],2*self.parameters['z_dist'][2]/self.parameters['z_dist'][3])
               
        self.structure()
        # Print all the parameters
        #print ('Parameters of the beam object \n'  )
        #for key in self.parameters:
         #   print (key, '\t', self.parameters[key])
        
    def save(self,name_of_file,description):
        
        """ This function will save the beam object to an external file in the directory called "defined_beams" in the source directory"""
        
        dir = os.path.dirname(__file__)
        current_module = __name__
        rel_dir_name = 'defined_'+current_module+'s'
        filename = os.path.join(dir,rel_dir_name,name_of_file)
        if os.path.isfile(filename) == True:
            in_keyboard = input("Filename specified by you -- > " + name_of_file + " already exists, do you want to overwrite, yes [y] or no [n]?")
            if in_keyboard == 'n':
                name_of_file = input('Enter new file name')
            filename = os.path.join(dir,rel_dir_name,name_of_file)
            if os.path.isfile(filename) == True:
                print('Gave the same file name again, overwriting the file!')
                writer = csv.writer(open(filename, 'w'))
                writer.writerow(['Description',description])
                for key, value in self.parameters.items():
                    writer.writerow([key, value])
                print (" Successfully written at "+ filename)
            else:
                writer = csv.writer(open(filename, 'w'))
                writer.writerow(['Description',description])
                for key, value in self.parameters.items():
                    writer.writerow([key, value])
                print (" Successfully written at a new file at \t"+ filename)
        else:
            writer = csv.writer(open(filename, 'w'))
            writer.writerow(['Description',description])
            for key, value in self.parameters.items():
                writer.writerow([key, value])
            print (" Successfully written at a new file at \t"+ filename)
             
    def load(self,name_of_file):
        """ This function will load the beam object from the specified file in the directory called "defined_beams" in the source directory"""
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
        
    def structure(self):
        """ This function defines the structure of the beam based on the beam parameters"""
    
        #print('This is the stucture')
        beam_Profile = np.ones((self.parameters['x_dist'][3],self.parameters['y_dist'][3],self.parameters['z_dist'][3]))
        #print("The grid size is", beam_Profile.shape)

        
        if self.parameters['dist_type'][0] == 'g':
            beam_Profile_X = pow(self.parameters['par_num'],1/3)*self.gaussian(self.parameters['x_range'],self.parameters['x_dist'][0],self.parameters['x_dist'][1])

        if self.parameters['dist_type'][1] == 'g':
            beam_Profile_Y = pow(self.parameters['par_num'],1/3)*self.gaussian(self.parameters['y_range'],self.parameters['y_dist'][0],self.parameters['y_dist'][1])
            
        if self.parameters['dist_type'][2] == 'g':
            beam_Profile_Z = pow(self.parameters['par_num'],1/3)*self.gaussian(self.parameters['z_range'],self.parameters['z_dist'][0],self.parameters['z_dist'][1])           

        beam_Profile=beam_Profile*beam_Profile_X[:,None,None]

        beam_Profile=beam_Profile*beam_Profile_Y[None,:,None]

        beam_Profile=beam_Profile*beam_Profile_Z[None,None,:]

        # Check the total number of particles,
        total_Particles = beam_Profile.sum()
        #print (total_Particles)
        if total_Particles - self.parameters['par_num'] < 0.0001*self.parameters['par_num']:
            self.parameters['Beam Grid'] = beam_Profile
            
        temp = np.sum(self.parameters['Beam Grid'],2)    
        beam_Profile_X = np.sum(temp,1)
        #print (self.parameters['par_num'])
        #print (beam_Profile_X.sum())
        self.parameters['X Profile'] = beam_Profile_X
        temp = np.sum(self.parameters['Beam Grid'],2)
        beam_Profile_Y = np.sum(temp,0)
        #print (beam_Profile_Y.sum())
        self.parameters['Y Profile'] = beam_Profile_Y
        temp = np.sum(self.parameters['Beam Grid'],0)
        beam_Profile_Z = np.sum(temp,0)
        #print (beam_Profile_Z.sum())
        self.parameters['Z Profile'] = beam_Profile_Z
    
    def plot(self):
        """ This function will plot the profile of the beam in the mentioned axis"""
    
        #print('This is the plot')        
        subplot(1,3,1)
        plot(self.parameters['x_range'],self.parameters['X Profile'])
        subplot(1,3,2)
        plot(self.parameters['y_range'],self.parameters['Y Profile'])
        subplot(1,3,3)
        plot(self.parameters['z_range'],self.parameters['Z Profile'])

    def gaussian(self, x, mu, sig):
        """ Returns the normal distribution with x number of points, and mean mu, and sig """
        grid_size = (x[1]-x[0])
        return_array = np.power(sig*np.sqrt(2*np.pi),-1)*np.exp(-np.power(x - mu, 2) /( 2 * np.power(sig, 2)))*grid_size
        #print('The gaussian is normalized', (return_array*grid_Size).sum());
        # http://ftp.arl.mil/random/random.pdf Good document for distribution generation
        return return_array
        
        
    def parabolic(self, x, xmin, xmax):
        """ Returns the normal distribution with x number of points, and mean mu, and sig """
        return_array = np.power(sig*np.sqrt(2*np.pi),-1)*np.exp(-np.power(x - mu, 2) /( 2 * np.power(sig, 2)))
        #print('The gaussian is normalized', (return_array*grid_Size).sum());
        return return_array
        
    def __repr__(self):
        """ Returns the value of the object """
        return "%s(%r)" % (self.__class__, self.__dict__)
        
    @classmethod
    def listfiles(staticbeam):
        """ THis function will list all the static and dynamic beams """
        dir = os.path.dirname(__file__)
        rel_dir_name = 'defined_'+__name__ +'s'
        mypath = os.path.join(dir,rel_dir_name)
        #print (mypath)
        f = []
        description = []
        for (dirpath, dirnames, filenames) in os.walk(mypath):
            f.extend(filenames)
            break
        desc_index = 0
        print ('Beamfile','---','Description\n')
        for filename in f:
            reader = csv.reader(open(os.path.join(mypath,filename), 'r'))
            description.append(next(reader))
            print (filename,'---',description[desc_index][1])
            desc_index = desc_index + 1
        print ('----------------------------\n')
    
class dynamicbeam():
    """This attributes are similar to a static beam, however, the beam energy, number of beam particles and beam structure is updated for several turns (depends on the length of list) and stored"""
    
    def __init__(self,*args,**kwargs):
        """ Instantiation behaviour for the beam class, the arguments can be file name with beam parameters, a dictionary object or a list of beam parameters """
        # 
        argspec = inspect.getargspec(staticbeam)
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
        elif len(args) == 9:
            self.parameters = {}
            self.parameters["par_type"]= args[0] # particle type
            self.parameters["charge_state"] = args[1] # charge state
            self.parameters["atomic_mass"] = args[2] # atomic mass
            self.parameters["kin_energy"] = args[3] # kinetic energy
            self.parameters["par_num"] = args[4] # particle number
            self.parameters["dist_type"] = args[5] # distibution type
            self.parameters["x_dist"] = args[6] # distibution type
            self.parameters["y_dist"] = args[7] # distibution type
            self.parameters["z_dist"] = args[8] # distibution type
        else:
            print('You have the wrong number of arguments, Please use help...')
        
        #initiate the beam shape in the three dimensions
        structure(self)
        
        # Check if the some parameters are not defined or assigned to None
        
        #for key in self.parameters:
         #   print (key, '\t', self.parameters[key])
        
        
        
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
        
    def structure(self):
        """ This function defines the structure of the beam based on the beam parameters"""
        
        print('This is the stucture')
            
        beam_Profile = np.ones((self.parameters['xdist'][3],self.parameters['ydist'][3],self.parameters['zdist'][3]))
        print("The grid size is", beam_Profile.shape)
        if self.parameters['dist_type'][0] == 'g':
            beam_Profile_X = pow(self.parameters['par_num'],1/3)*gaussian(self.parameters['xdist'][3],self.parameters['xdist'][0],self.parameters['xdist'][1])
            #photons_X = photon_Profile_X.sum()
            #print('The gaussian is normalized', photons_X, pow(mean_Photons,1/3))
            #subplot(2,3,1)
        if self.parameters['dist_type'][1] == 'g':
            beam_Profile_Y = pow(self.parameters['par_num'],1/3)*gaussian(self.parameters['ydist'][3],self.parameters['ydist'][0],self.parameters['ydist'][1])
            
        if self.parameters['dist_type'][2] == 'g':
            beam_Profile_Z = pow(self.parameters['par_num'],1/3)*gaussian(self.parameters['zdist'][3],self.parameters['zdist'][0],self.parameters['zdist'][1])           

        beam_Profile=beam_Profile*beam_Profile_X[:,None,None]

        beam_Profile=beam_Profile*beam_Profile_Y[None,:,None]

        beam_Profile=beam_Profile*beam_Profile_Z[None,None,:]

        # Check the total number of particles,
        total_Particles = beam_Profile.sum()
        if total_Particles - self.parameters['par_num'] < 0.0001*self.parameters['par_num']:
            self.parameters['Beam Grid'] = beam_Profile
            
        temp = sum(self.parameters['Beam Grid'],2)    
        beam_Profile_X = sum(temp,1)
        self.parameters['X Profile'] = beam_Profile_X
        temp = sum(self.parameters['Beam Grid'],2)
        beam_Profile_Y = sum(temp,0)
        self.parameters['Y Profile'] = beam_Profile_Y
        temp = sum(self.parameters['Beam Grid'],0)
        beam_Profile_Z = sum(temp,0)
        self.parameters['Z Profile'] = beam_Profile_Z


        
    def gaussian(x, mu, sig):
        """ Returns the normal distribution with x number of points, and mean mu, and sig """
        grid_size = (x[1]-x[0])
        return_array = np.power(sig*np.sqrt(2*np.pi),-1)*np.exp(-np.power(x - mu, 2) /( 2 * np.power(sig, 2)))*grid_size
        #print('The gaussian is normalized', (return_array*grid_Size).sum());
        # http://ftp.arl.mil/random/random.pdf Good document for distribution generation
        return return_array
        
        
    def parabolic(x, xmin, xmax):
        """ Returns the normal distribution with x number of points, and mean mu, and sig """
        return_array = np.power(sig*np.sqrt(2*np.pi),-1)*np.exp(-np.power(x - mu, 2) /( 2 * np.power(sig, 2)))
        #print('The gaussian is normalized', (return_array*grid_Size).sum());
        return return_array
    

    
    def plot():
        """ This function will plot the profile of the beam in the mentioned axis"""
    
        print('This is the plot')        
        
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
    
    def listfiles(cls):
        """ THis function will list all the static and dynamic beams """
        dir = os.path.dirname(__file__)
        rel_dir_name = 'defined_'+__name__ +'s'
        mypath = os.path.join(dir,rel_dir_name)
        f = []
        description = []
        for (dirpath, dirnames, filenames) in os.walk(mypath):
            f.extend(filenames)
            break
        for filename in f:
            reader = csv.reader(open(filename, 'r'))
            description.append(next(reader))
            filename.close()
            print (f,'---',filename)
    
        
    
    
