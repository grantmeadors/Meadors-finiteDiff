#!/usr/bin/env python
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

# Noise
noiseAmp = 1.0
noise = noiseAmp * np.random.randn(Fsample*Tobs)

# Signal
signalAmp = 100.0
signalFreq = 200.0
time = np.linspace(0, Tobs, Fsample*Tobs)
signal = signalAmp * np.sin(2*np.pi*signalFreq*time) 

# Observed
observed = signal + noise

print observed

# Frequency bins of the FFT
fftBins = np.linspace(0, Fsample, Fsample*Tobs)

print fftBins

# FFT the data
fftObserved = np.fft.fft(observed)
asdObserved = np.absolute(fftObserved)

print asdObserved

# Plot the data
def plotASD(xBins, asdData, fileName):
    fig = plt.figure()
    plt.semilogy(fftBins,asdObserved)
    plt.axis([0,500,1e-2,1e10])
    plt.xlabel('Frequency [Hz]')
    plt.title('Amplitude spectral density')
    fig.savefig(fileName)
    plt.close()

plotASD(fftBins, asdObserved, 'asdObserved.png')
