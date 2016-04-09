#!/opt/local/bin/python
# Grant David Meadors
# 02016-04-09 (JD 2457488)
# g r a n t . m e a d o r s @ a e i . m p g . d e
# Script to test idea for finite differences

# These two lines are necessary
import numpy as np
import matplotlib.pyplot as plt

# These three lines are used to create high-quality plots
# and can be commented out for fast runs
from matplotlib import rc
rc('font', **{'family':'serif','serif':['Times']})
rc('text',usetex=True)

# Sampling frequency and observation time
Fsample = 16384.0
Tobs = 2.0


# Frequency bins of the FFT
fftBins = np.linspace(0, Fsample, Fsample*Tobs)

# FFT the data
H1fft = np.fft.fft(H1dataZeroed[:,1])
H1asd = np.absolute(H1fft)

# Plot the data
def plotASD(xBins, asdData, fileName):
    fig = plt.figure()
    plt.plot(fftBins,H1asd)
    plt.axis([100,300,0,2e-17])
    plt.xlabel('Frequency [Hz]')
    plt.title('Amplitude spectral density')
    fig.savefig(fileName)
    plt.close()

plotASD(fftBins, H1asd, 'H1asd.png')
