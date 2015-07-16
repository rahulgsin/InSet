#!/usr/bin/python
""" This module calculates the observables based on beam and machine object

The module takes the following arguments

Property --- Key --- Value type --- Description

Circumference --- circumference --- Float --- Circumference of the machine

Gamma transition --- Tr_gamma --- Float --- Gamma transition

Set tune --- set_tune --- List of Float --- Horizontal and vertical tune

Set Chromaticity --- set_chro --- List of float --- Horizontal and vertical chromaticity """

# meta info
__author__ = 'Rahul Singh'
__email__ = 'r.singh@gsi.de'
__version__ = '-1.0'
__lastchanged__ ='25062015'


import beam
class staticobservable():
    """ The machine class defines all the machine parameters"""
    
    """ Machine settings can be stored in an external file and retrieved"""
    
    def __init__(self,beam_in,machine_in):
        """This function will calculate all the observables"""
        self.parameters = {}
        self.parameters['current'] = (beam_in.parameters['par_num']*beam_in.parameters['charge_state']*beam_in.parameters['beta']*beam.VEL_LIGHT)*beam.CHARGE/(machine_in.parameters['Length'])
        
class dynamicobservable():
    """ The machine class defines all the machine parameters"""
    
    """ Machine settings can be stored in an external file and retrieved"""
    
    def __init__(self,staticbeam,staticmachine):
        """This function will calculate all the observables"""
        self.current = (staticbeam['par_num']*staticbeam['charge_state']*staticbeam['beta']*beam.VEL_LIGHT)/(staticmachine['Length'])
        