#!/usr/bin/python
""" Generic ADCModule

The module takes the following arguments

Maximum --- The voltage resulting from the maximum reading (defines the ADC range)

Minimum --- The voltage resulting from the minimum reading

Effective_bits--- Effective number of bits

Distortion (Optional) --- Use distortion tables from the ADCs"""


class genericAdc():
    
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
            self.parameters["ADC_maximum"]= args[0] # ADC maximum voltage
            self.parameters["ADC_minimum"] = args[1] # ADC minimum voltage
            self.parameters["Effective_bits"] = args[2] # Effective number of bits
            self.parameters["Distortion"] = args[3] # Other distortion parameters

        else:
            print('You have the wrong number of arguments, Please use help...')
        
        
        # Check if the some parameters are not defined or assigned to None or have the wrong type
        
        if self.parameters["ADC_maximum"] == None:
            print ("ADC_maximum is not defined")
            print ("Throw exception")
        if type(self.parameters["ADC_maximum"][0]) != 'float':
            self.parameters["ADC_maximum"][0] = float(self.parameters["ADC_maximum"][0])
            self.parameters["ADC_maximum"][1] = float(self.parameters["ADC_maximum"][1])
            self.parameters["ADC_maximum"][2] = float(self.parameters["ADC_maximum"][2])
            self.parameters["ADC_maximum"][3] = float(self.parameters["ADC_maximum"][3])
        if self.parameters["ADC_minimum"] == None:
            print ("ADC_minimum is not defined")
            print ("Throw exception")
        if type(self.parameters["ADC_minimum"][0]) != 'float':
            self.parameters["ADC_minimum"][0] = float(self.parameters["ADC_minimum"][0])
            self.parameters["ADC_minimum"][1] = float(self.parameters["ADC_minimum"][1])
            self.parameters["ADC_minimum"][2] = float(self.parameters["ADC_minimum"][2])
            self.parameters["ADC_minimum"][3] = float(self.parameters["ADC_minimum"][3])
        if self.parameters["Effective_bits"] == None:
            print ("Effective_bits is not defined")
            print ("Throw exception")
        if type(self.parameters["Effective_bits"]) != 'float':
            self.parameters["Effective_bits"] = float(self.parameters["Effective_bits"])
            
            
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