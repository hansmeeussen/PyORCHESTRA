import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

import PyORCHESTRA
#-------------------------------------------------------------------------------
# Minimalistic program to test ORCHESTRA C++ solver from Python
#
# May 2025 Hans Meeussen
#
# The ORCHESTRA solver requires:
#    - an input text file with  chemical model definition (substances reactions etc) (can be composed with Java GUI)
#    - a list of input variables for each calculation (in this case read from input text file column headers)
#    - a list of output variables for each calculation (in this case read from output text file column headers)
#    - number of cells to operate on (1 in the serial example, total number of calculations in parallel example)
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# 1) Define input variables
#-------------------------------------------------------------------------------

# provide a list of names, for example:
# inputVariableNames  = np.array(['C.tot', 'Ca.tot', 'pH'])

# Or read column headers from input datafile
dataframeInput    = pd.read_csv('input.dat', sep=r"\s+", header=0, comment='#')
inputVariables    = np.array(dataframeInput.columns)


#-------------------------------------------------------------------------------
# 2) Define output variables
#-------------------------------------------------------------------------------

# provide a list of output variable inputVariableNames, for example:
# outputVariables = np.array(['tot_nr_iter', 'pH', 'OH-.logact', 'Portlandite[s].con' ])

# or read column headers from existing output datafile
# this is similar to the way the java version works.
# so you can add output variables by adding them to the column names in the output.dat file
dataframeOutput = pd.read_csv('output.dat', sep=r"\s+", header=0, comment='#')
#outputVariables = np.array(dataframeOutput.columns)

# or create your own set of variables
#outputVariables  = np.array(['pH', 'I', 'H+.logf', 'CO2.logact', 'CO3-2.logact', 'HCO3-.logact', 'tot_nr_iter']) 
outputVariables  = np.array(['pH', 'C.diss', 'CO2.con', 'CO3-2.con', 'HCO3-.con']) 


# create empty 2d input and output data array.inputVariableNames
# in this example we use one row per calculation
inputarray  = np.zeros((len(dataframeInput.index),len(inputVariables)))
outputarray = np.zeros((len(dataframeInput.index),len(outputVariables)))


#-------------------------------------------------------------------------------
# 3) Initialise the solver
#-------------------------------------------------------------------------------
# Define number of cells/nodes, first solver has one cell
nrCells = 1

# Define the input file with the chemistry definition, usually generated with the Java GUI
chemistryFile = "chemistry1.inp"

# Create an ORCHESTRA solver object
solver = PyORCHESTRA.ORCHESTRA()

# and initialise the solver
# note that we initialise the solver with a list of input and output variable names
# the order of the variables in these lists should be the same as used later in the input and output value arrays
# after initialisation this order is fixed!! so cannot be changed. 
solver.initialise(chemistryFile, nrCells, inputVariables, outputVariables)


#-------------------------------------------------------------------------------
# 4) Call the solver for each datapoint in the input, and write the output to the output array
#    todo: probably we can directly use dataframe as input without copying to array
#-------------------------------------------------------------------------------

# the first calculation takes extra time as it includes initialization of the calculator
# so we can do this separately
inputarray[0]  = np.array([np.array(dataframeInput.iloc[0,:])]).astype('float64')
outputarray[0] = solver.set_and_calculate_single(inputarray[0])



print("starting serial calculations ...")
tic = time.perf_counter()
n=0
while(n<len(dataframeInput.index)):
    
    # fill the input array
    #inputarray[n]  = np.array([np.array(dataframeInput.iloc[n,:])]).astype('float64')
    in1 = np.array(dataframeInput.iloc[n]).astype('float64')

    # so the calculations are performed for a single data row at the time, although the input and output data sets are 2d matrices
    # it will also be possible to calculate a multiple dataset in one go, using parallel processing
    #outputarray[n] = solver.set_and_calculate_single(inputarray[n])
#    outputarray[n] = solver.set_and_calculate_single(np.array(dataframeInput.iloc[n]))
    outputarray[n] = solver.set_and_calculate_single(dataframeInput.iloc[n])
    n=n+1
    print(".", end="", flush=True)

toc = time.perf_counter()
print(f"This took  {toc - tic:0.4f} seconds")


#-------------------------------------------------------------------------------
# 5) Copy the output data to a dataframe to facilitate making graphs etc.
#-------------------------------------------------------------------------------

# create dataframe with output data and names as output column headers
outputdf = pd.DataFrame(outputarray, columns = outputVariables)

#-------------------------------------------------------------------------------
# 6) Write output dataframe to (tab separated) file.
#-------------------------------------------------------------------------------
outputdf.to_csv("output_python.dat", sep='\t',index=False)


#test = dataframeOutput.compare(outputdf,keep_shape=True, keep_equal=True)

#test




#-------------------------------------------------------------------------------
# 7) Now we demonstrate how to do the calculations in parallel
#-------------------------------------------------------------------------------
#print("starting parallel calculations...")

# Create a new solver object
#solver2 = PyORCHESTRA.ORCHESTRA()

# Use the same input dataset, number of cells is size of input dataset
# all cells are processed in single call
#nrCells = len(dataframeInput.index)

# we use the same IO variables as the serial calculations
#solver2.initialise(chemistryFile, nrCells, inputVariables, outputVariables)

#tic = time.perf_counter()

# The memory option 1 makes use of previous calculation results, which is useful for the first calculations
# on this set of cells (e.g. to initialize transport cells)
# This first calculation will take a bit longer as the calculators need to start up en be initialized
# The number of threads
#nrThreads = 8
#outputarray = solver2.set_and_calculate_multi(inputarray, nrThreads, 1)
#toc = time.perf_counter()
#print(f"This took  {toc - tic:0.4f} seconds")


# now we redo the calculations, with memory option 0, which uses the previous results as starting value for the next
# these results are stored in the set of cells
# we now have perfect start estimations for the unknowns, so no iterations necessary, which will be very quick
# The calculators are already started up
#print("starting parallel calculations second time with results of last time...")
#tic = time.perf_counter()
#outputarray = solver2.set_and_calculate_multi(inputarray, nrThreads, 0)
#toc = time.perf_counter()
#print(f"This took  {toc - tic:0.4f} seconds")

#outputdf.to_csv("output2.dat", sep='\t',index=False)

#-------------------------------------------------------------------------------
# 7) Use dataframe to make graphs
#-------------------------------------------------------------------------------
# odf = pd.read_csv("testframe.txt", sep = "\s+" ,header=0, comment='#')
odf = pd.read_csv("output_python.dat", sep = r"\s+" ,header=0, comment='#')
# now we can use the dataframe to make graphs
#odf.plot(y ='CO3-2.con', x='pH', kind = 'scatter')
#odf.plot(y ='HCO3-.con', x='pH', kind = 'line')
odf.plot(x='pH')
#outputdf.plot(x ='Si.tot', y='pH', kind = 'scatter')
#ax2 = outputdf.plot.scatter(x='Ca.tot',
#                      y='Si.tot',
#                      c='Portlandite[s].bulksolid',
#                      colormap='viridis')


plt.show()