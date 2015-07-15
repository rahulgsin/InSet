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
        elif len(args) == 4:
            self.parameters = {}
            self.parameters["Gain"]= args[0] # Not in dB
            self.parameters["Bandwidth"] = args[1] # In MHz
            self.parameters["Input_noise"] = args[2] # In nV/sqrt(Hz)
            self.parameters["Distortion"] = args[3] # Yet to be defined distortion parameters

        else:
            print('You have the wrong number of arguments, Please use help...')
        
        
        # Check if the some parameters are not defined or assigned to None or have the wrong type
        
        if self.parameters["Gain"] == None:
            print ("Gain is not defined")
            print ("Throw exception")
        if type(self.parameters["Gain"][0]) != 'float':
            self.parameters["Gain"][0] = float(self.parameters["Gain"][0])
            self.parameters["Gain"][1] = float(self.parameters["Gain"][1])
            self.parameters["Gain"][2] = float(self.parameters["Gain"][2])
            self.parameters["Gain"][3] = float(self.parameters["Gain"][3])
        if self.parameters["Bandwidth"] == None:
            print ("Bandwidth is not defined")
            print ("Throw exception")
        if type(self.parameters["Bandwidth"][0]) != 'float':
            self.parameters["Bandwidth"][0] = float(self.parameters["Bandwidth"][0])
            self.parameters["Bandwidth"][1] = float(self.parameters["Bandwidth"][1])
            self.parameters["Bandwidth"][2] = float(self.parameters["Bandwidth"][2])
            self.parameters["Bandwidth"][3] = float(self.parameters["Bandwidth"][3])
        if self.parameters["Input_noise"] == None:
            print ("Input_noise is not defined")
            print ("Throw exception")
        if type(self.parameters["Input_noise"]) != 'float':
            self.parameters["Input_noise"] = float(self.parameters["Input_noise"])
            
            
        # Calculate all the internal parameters

        
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