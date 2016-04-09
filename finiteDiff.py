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

#print observed

# Frequency bins of the FFT
fftBins = np.linspace(0, Fsample, Fsample*Tobs)

#print fftBins

# FFT the data
fftObserved = np.fft.fft(observed)
asdObserved = np.absolute(fftObserved)

#print asdObserved

# Plot the FFT of the data
def plotASD(xBins, asdData1, asdData2, fileName):
    fig = plt.figure()
    plt.semilogy(fftBins,asdData1)
    plt.semilogy(fftBins,asdData2)
    plt.axis([0,2*signalFreq,noiseAmp/1e2, signalAmp*1e8])
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude spectral density [sqrt(Hz)]')
    plt.title('Fourier domain: signal and enhanced signal')
    fig.savefig(fileName)
    plt.close()

def plotTD(temporal, observable1, observable2, fileName):
    fig = plt.figure()
    plt.plot(temporal, observable1)
    plt.plot(temporal, observable2)
    plt.axis([0, 4.0/signalFreq, -2.0*signalAmp, 2.0*signalAmp])
    plt.xlabel('Time [s]')
    plt.ylabel('(dimensionless)')
    plt.title('Time domain: signal and enhanced signal')
    fig.savefig(fileName)
    plt.close()


# See if stacking the derivatives helps any
def differenceTaker(dataToStack, Fsample, testFreq):
    return -1/(2*np.pi*testFreq) * np.diff(np.diff(dataToStack))

def diffStacker(dataToStack, Fsample, testFreq, stackHeight):
    secondDerivativeInput = dataToStack
    partSum = dataToStack
    print 'Stacking'
    for x in range(0,stackHeight):
        thisSecondDerivative = differenceTaker(secondDerivativeInput, Fsample, testFreq)
        secondDerivativeInput = thisSecondDerivative
        partSum = partSum[:-2] + thisSecondDerivative
    diffInLength = len(dataToStack) - len(partSum)
    paddedSum = np.pad(partSum, (0, diffInLength), 'constant', constant_values=(0,0))
    return paddedSum

stackedObserved = diffStacker(observed, Fsample, signalFreq, 20)

# FFT the stacked data
fftStackedObserved = np.fft.fft(stackedObserved)
asdStackedObserved = np.absolute(fftStackedObserved)

    
plotASD(fftBins, asdObserved, asdStackedObserved, 'asdObserved.png')
plotTD(time, observed, stackedObserved, 'observed.png')
