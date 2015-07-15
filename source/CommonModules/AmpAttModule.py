#!/usr/bin/python
""" Generic Amplifier Module

The module takes the following arguments

Amplification --- The amplification/attenuation in (dB)

Noise figure --- Accelerator setting object

Input Noise --- When the input is open or terminated (in nV/sqrt(Hz))

AmplifierType (Optional) --- Specific amplifier implementation"""

class genericAmpAtt():
    
    """ The Generic trafo class defines all the generic trafo parameters"""
    
    """ Trafo settings can be stored in an external file and retrieved"""

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
        if type(self.parameters["Torus_radii"]) != 'float':
            self.parameters["Torus_radii"] = float(self.parameters["Torus_radii"])
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
        self.inductance = 
        self.rise_time =
        self.droop_time =
        
        # Print all the class instance variables
        
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