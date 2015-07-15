""" The InSet package is used to model all the beam diagnotic devices

The Package revolves around 5 objects

Beam object -- Particly type, charge state, atomic mass, energy, energy spread, 6D phase space distribution

Methods : Initiate or construct each variable and define frequency used beams and recall them

Machine object -- Tunes, Chromaticity, RF cavity voltage and frequency, Machine length, Rigidity, Transverse and Longitudinal Impedances

observables = Observable(beam,machine)

observables -- Revolution frequency, beam current, peak current, synchrotron frequency, 

trafoOut = Trafo(observables, trafoParameters)
trafoSet = TrafoSet(observables, trafoParameters, trafoConstraints) """