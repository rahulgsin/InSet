# This change was done on the windows to check GIT

import beam
import machine
import observable
import DeviceModules.TrafoModule as TrafoModule
import CommonModules.AmpAttModule as AmpAttModule
import CommonModules.AdcModule as AdcModule
import mpmath


dictionary_beam = {'par_type':'Ur','charge_state': 73, 'atomic_mass': 238, 'kin_energy' : 11.4, 'par_num': 10e8, 'dist_type': 'ggg', 'x_dist': [0, 5], 'y_dist': [0, 3], 'z_dist' : [0, 1000]} 
# Write a help beam command, to help filling this
defined_beam = beam.staticbeam('Ur',28,238,11.4,10e9,'gpg',[0,4],[0,7],[0,50000]) # defined_beam is a beam object
print ("Defined directly")
dict_beam = beam.staticbeam(**dictionary_beam) # dict_beam is a beam object, dont forget ** while passing a dictionary
print ("Defined using dictionary")
#defined_beam.save('UrBeam') # save the directly defined beam
#print ("Saved beam")
#recalled_beam_dict = defined_beam.load('UrBeam') # Recall the defined beam
#print (recalled_beam_dict)
#Make a new beam object
#recalled_beam = beam.staticbeam(**recalled_beam_dict)
#print (recalled_beam)

old_beam = beam.staticbeam('UrBeam')
print ("Defined using a saved beam file")
print (old_beam) # define this function

dictionary_machine = {'Type': 'Synchrotron', 'Length': 216.02, 'Tr_gamma': 5.33, 'Impedances' : [None], 'Set_tune': [None], 'Set_chromaticity': [None], 'Dispersion': [None],  'Lattice_settings': 'link to mad file', 'RF_parameters' : [4000, 216000*4, 4, 'a'], 'Injection_settings': [None]}
defined_machine = machine.staticmachine('LINAC',100,105,None,None,None,None,None,[5000,350e6],None)
dict_machine = machine.staticmachine(**dictionary_machine)
#defined_machine.save('LowEnergyUrSIS18')
#recalled_machine = defined_machine.load('LowEnergyUrSIS18')

observable_linac = observable.staticobservable(defined_beam,defined_machine) # A dictionary of all beam observables
observable_sis18 = observable.staticobservable(dict_beam,defined_machine) # A dictionary of all beam observables

<<<<<<< HEAD
print ("The calculated current is",  observable_linac.current)
=======
print ("The calculated current is", observable_linac.current)
>>>>>>> 956bc732c2c0ab3356dd63f3e85e58f954624432

trafo_dic_1st ={'Torus_radii': [70,90], 'Torus_thickness': 16, 'Torus_permeability': 10000, 'Num_windings': 10, 'Output_resistance': 50,  'Stray_capacitance': 10,  'Magnetic_noise' : None} # Trafo parameters for first transformer
trafo_dic_2nd ={'Torus_radii': [30,45], 'Torus_thickness': 25, 'Torus_permeability': 10000, 'Num_windings': 20,'Output_resistance': 50, 'Stray_capacitance': 10,  'Magnetic_noise' : None} # Trafo parameters for the second transformer
special_trafo = TrafoModule.generictrafo(**trafo_dic_1st)
special_trafo_2nd = TrafoModule.generictrafo(**trafo_dic_2nd)

trafo_amp1 = AmpAttModule.genericAmpAtt([100,10,10e6,10,'lb'],[1,0.1,100,0.01,'lt'],5,None)
 # Gain (factor), Bandwidth in MHz, , Input noise nV/sqrt(Hz)(FUnction of bandwidth and gain, save in a table) Can be saved and recalled
trafo_amp2 = AmpAttModule.genericAmpAtt([10000,10,10e6,10,'lb'],[2,0.1,100,0.01,'lt'],5,None)

trafo_adc = AdcModule.genericAdc([1,0,2,0.1,'lt'],[-1,-2,0,0.1,'lb'],12,None) # Maximum, Minimum (in V) and effective number of bits, Distortion value or table

trafo_system_one = special_trafo.combine_systems(trafo_amp1,trafo_adc) #  This function combines sensor with its accesories for full DA system
trafo_system_two = special_trafo_2nd.combine_systems(trafo_amp2,trafo_adc)

results1 = trafo_system_one.output(observable_linac)
results2 = trafo_system_two.output(observable_sis18)
settings = trafo_system_one.optimize(observable_linac, constraints_linac)
settings = trafo_system_two.optimize(observable_sis18, constraints_sis18)



