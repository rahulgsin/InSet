# This change was done on the windows to check GIT

import beam
import machine
import observable
import DeviceModules.TrafoModule as TrafoModule
import CommonModules.AmpAttModule as AmpAttModule
import CommonModules.AdcModule as AdcModule
import mpmath
import numpy as np
from matplotlib.pyplot import plot,subplot


#   Use a dictionary with the mentioned keys to define a machine


dictionary_machine = {'Type': 'Synchrotron', 'Length': 216.02, 'Tr_gamma': 5.33, 'Impedances' : [None], 'Set_tune': [None], 'Set_chromaticity': [None], 'Dispersion': [None],  'Lattice_settings': 'link to mad file', 'RF_parameters' : [4000, 216000*4, 4, 'a'], 'Injection_settings': [None],'Pipe_radii': [0.05,0.025]}
SIS_18_machine = machine.staticmachine(**dictionary_machine)

# The settings can be saved to a file
#defined_machine.save('LowEnergyUrSIS18','Machine settings at injection energies')

# One can also print the machine to see the saved parameters
# print ('Dictionary defined machine\n', SIS_18_machine,'\n')

# Define the mesh settings for the beam structure
beam_mesh_points = [20,20,500]


# Define the beam using the dictionary with the right keys
dictionary_beam = {'par_type':'Ur','charge_state': 73, 'atomic_mass': 238, 'kin_energy' : 11.4, 'par_num': 1e10, 'dist_type': 'ggg', 'x_dist': [0, 0.005,SIS_18_machine.parameters['Pipe_radii'][0],beam_mesh_points[0]], 'y_dist': [0, 0.003,SIS_18_machine.parameters['Pipe_radii'][1],beam_mesh_points[1]], 'z_dist' : [0, 10,SIS_18_machine.parameters['Length'],beam_mesh_points[2],SIS_18_machine.parameters['RF_parameters'][2]]} 
dict_beam = beam.staticbeam(**dictionary_beam) # dict_beam is a beam object, dont forget ** while passing a dictionary
# print ('Dictionary defined beam\n', dict_beam,'\n')

# Plot the beam strucute
#dict_beam.plot()

# One can also define the beam without using a dictionary using the arguments in the right order
defined_beam = beam.staticbeam('Ur',28,238,11.4,1e10,'ggg',[0,0.007,SIS_18_machine.parameters['Pipe_radii'][0],beam_mesh_points[0]],[0,0.004,SIS_18_machine.parameters['Pipe_radii'][1],beam_mesh_points[1]],[0,50,SIS_18_machine.parameters['Length'],beam_mesh_points[2],SIS_18_machine.parameters['RF_parameters'][2]]) # defined_beam is a beam object, the order has to be maintained


dictionary_beam = {'par_type':'Ur','charge_state': 73, 'atomic_mass': 238, 'kin_energy' : 11.4, 'par_num': 1e10, 'dist_type': 'ggg', 'x_dist': [0, 0.005,0,0.007,SIS_18_machine.parameters['Pipe_radii'][0],beam_mesh_points[0]], 'y_dist': [0, 0.003,0,0.01,SIS_18_machine.parameters['Pipe_radii'][1],beam_mesh_points[1]], 'z_dist' : [0,10,0,0.001,SIS_18_machine.parameters['Length'],beam_mesh_points[2],SIS_18_machine.parameters['RF_parameters'][2]]} 
dict_beam = beam.dynamicbeam(**dictionary_beam) # dict_beam is a beam object, dont forget ** while passing a dictionary
# print ('Dictionary defined beam\n', dict_beam,'\n')
#defined_beam.save('UrBeam','Uranium beam on the following experiment day') # save the directly defined beam

#print a list of all the save beam files, to select which beam one wants to load
beam.staticbeam.listfiles() # Sometimes, it insists passing an instance even though it is a class method

#recalled_beam_dict = defined_beam.load('UrBeam') # One can also recall saved beam parameters to make a copy of previously defines beam

#print (recalled_beam_dict)
#Make a new beam object
#recalled_beam = beam.staticbeam(**recalled_beam_dict)
#print (recalled_beam)

#old_beam = beam.staticbeam('UrBeam')
#print ("Defined using a saved beam file")
#print (old_beam) # define this function

# Now calculate the observables which the diagnostic devices will observe at their installations from beam and machine object

#observable_linac = observable.staticobservable(defined_beam,defined_machine) # Observable object calculates all the observables
observable_sis18 = observable.staticobservable(dict_beam,SIS_18_machine) # A dictionary of all beam observables

# See if the calculated observable makes sense, also look into observable.py (observable class)
print ("The calculated current is",  observable_sis18.parameters['current'], "\n") # Access to the current observable
plot(defined_beam.parameters['z_range'],observable_sis18.parameters['current_profile'])

# Define the Transformer parameters using the Transformer class, lets say first is installed in one section
trafo_dic_1st ={'Torus_radii': [70,90], 'Torus_thickness': 16, 'Torus_permeability': 10000, 'Num_windings': 10, 'Output_resistance': 50,  'Stray_capacitance': 10,  'Magnetic_noise' : None} # Trafo parameters for first transformer

# Other transformer with slaightly different parameters
trafo_dic_2nd ={'Torus_radii': [30,45], 'Torus_thickness': 25, 'Torus_permeability': 10000, 'Num_windings': 20,'Output_resistance': 50, 'Stray_capacitance': 10,  'Magnetic_noise' : None} # Trafo parameters for the second transformer

# Instantiate the transformer objects with the dictionaries
special_trafo = TrafoModule.generictrafo(**trafo_dic_1st)
special_trafo_2nd = TrafoModule.generictrafo(**trafo_dic_2nd)

# Define the common modules or data acquisition elements befind the transformers

# First the amplifier modules
trafo_amp1 = AmpAttModule.genericAmpAtt([1,0.0001,1e6,3.16,'lb'],[0.001,0.00001,100,2,'lt'],5,None) # The increment or decrement always has to be greater than 1(for gain and bandwidth)
 # Gain (factor), Bandwidth in MHz, , Input noise nV/sqrt(Hz)(FUnction of bandwidth and gain, save in a table) Can be saved and recalled
trafo_amp2 = AmpAttModule.genericAmpAtt([1,0.0001,1e6,3.16,'lb'],[0.002,0.00001,100,2,'lt'],5,None) 

# Then the ADC modules
trafo_adc = AdcModule.genericAdc([1,0,2,0.1,'lt'],[-1,-2,0,0.1,'lb'],12,None) # Maximum, Minimum (in V) and effective number of bits, Distortion value or table

# Combine the common modules to the main sensor module to make a full system
special_trafo.combine_systems(trafo_amp1,trafo_adc) #  This function combines sensor with its accesories for full DA system

# One can also save the full system, so the combine system is not required for next usage
#special_trafo.save('FullSystemLINACTrafo', ' Saves the full system with the Amp and ADCs')

#special_trafo_2nd.combine_systems(trafo_amp2,trafo_adc)
#special_trafo.save('FullSystemSIS-18Trafo', ' Saves the full system with the Amp and ADCs')


# output function is used to calculate the output on the ADC
results1 = special_trafo.output(observable_sis18)
print ('Output signal and noise voltage for the first Trafo',results1[0], "and", results1[1], '\n')
#results2 = special_trafo_2nd.output(observable_sis18)
#print ('Output signal and noise voltage for the second Trafo',results2,'\n')
subplot(2,1,1)
plot(dict_beam.parameters['z_range'],results1[2])



# Define constraints, for calculating the right settings for the transformer
constraints_SIS_18 = {"Output": [[0.75,0.2],[0.1/300,5/300]], "Amp":['Gain','Bandwidth']} # No playing with ADCs "ADC":[ADC_maximum,ADC_minimum]
settings = special_trafo.optimize(observable_sis18, constraints_SIS_18)

print("Gain =", settings[0], "Bandwidth=", settings[1])

# output function called to print the output after "optimization"
new_output = special_trafo.output(observable_sis18)
print ('Output signal and noise voltage for the first Trafo',new_output[0], "and", new_output[1], '\n')
subplot(2,1,2)
plot(dict_beam.parameters['z_range'],new_output[2])
#settings = special_trafo_2nd.optimize(observable_sis18, constraints_sis18)



