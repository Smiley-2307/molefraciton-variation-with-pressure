#Variation of equilibrium products mole fractions (mainly CO2 CO and NOx) with different  P_c.

import cantera as ct
import numpy as np
import sys
import csv

# Edit these parameters to change the initial temperature, the pressure, and
# the phases in the mixture.

T = 1000.0
phi = 0.9

# phases
gas = ct.Solution('JP10.yaml')
carbon = ct.Solution('graphite.yaml')

# the phases that will be included in the calculation, and their initial moles
mix_phases = [(gas, 1.0), (carbon, 0.0)]

# gaseous fuel species
fuel_species = 'C10H16'

# equivalence ratio range
npoints = 50
P = np.linspace(0.1, 100, npoints)

mix = ct.Mixture(mix_phases)

# create some arrays to hold the data
tad = np.zeros(npoints)
xeq = np.zeros((mix.n_species, npoints))

xeq_CO = np.zeros(npoints)
xeq_CO2 = np.zeros(npoints)

for i in range(npoints):
    # set the gas state
    gas.set_equivalence_ratio(phi, fuel_species, 'O2:1.0, N2:3.76')

    # create a mixture of 1 mole of gas, and 0 moles of solid carbon.
    mix = ct.Mixture(mix_phases)
    mix.T = T
    mix.P = P[i]

    # equilibrate the mixture adiabatically
    mix.equilibrate('HP', solver='gibbs', max_steps=1000)

    tad[i] = mix.T
    xeq[:, i] = mix.species_moles
    xeq_CO[i] = xeq[11,i]
    xeq_CO2[i] = xeq[24,i]
    print('At pressure = {0:12.4g}, Xco = {1:12.4g}, Xco2 = {2:12.4g}'.format(P[i], xeq[11,i], xeq[24,i]))
    

# write output CSV file for importing into Excel
csv_file = 'Molefraction.csv'
with open(csv_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['P', 'T (K)'] + mix.species_names)
    for i in range(npoints):
        writer.writerow([P[i], tad[i]] + list(xeq[:, i]))
print('Output written to {0}'.format(csv_file))

if '--plot' in sys.argv:
    import matplotlib.pyplot as plt 
    plt.plot(P, xeq_CO)
    plt.plot(P, xeq_CO2)  
    plt.xlabel('pressure')
    plt.ylabel('Mole fraction')
    plt.legend(['CO','CO2'])
    plt.show()   
        
    
