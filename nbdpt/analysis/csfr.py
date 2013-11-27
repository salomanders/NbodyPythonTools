import pdb
#import struct
import numpy as np
#from astroML.plotting import scatter_contour
import matplotlib.pyplot as plt
#from scipy.integrate import quad
from .. import cosmography
import pynbody

def csfr(z):
	z0 = 1.243
	A = -0.997
	B = 0.241
	C = 0.180
	return C/(10.**(A*(z-z0)) + 10.**(B*(z-z0)))

def plot():
	filename = 'cosmo6.25cmb.192gs1bwK1BHC52.000116'
	volumesize = 6.25
	
#timeunit=np.sqrt((dKpcUnit*3.086e21)**3/(6.67e-8*dMsolUnit*1.99e33))/(3600.*24.*365.24)
	
	sim = pynbody.load(filename)
	pynbody.plot.stars.sfh(sim, log=True)
	
	plt.xlim(xmin=0)
	
	A = -0.997
	B = 0.241
	C = 0.180
	z0 = 1.243

	redshift = np.arange(2000)/100.
	omega_M = 0.24
	omega_L = 0.76
	omega_K = 1.0
	h = 0.73
	cosmo = cosmography.Cosmology(omega_M, omega_L, omega_K, h)
	
	
	
	tt = 13.7 - cosmo.Lookback_Time(redshift)*13.7
	
	plt.plot(tt, (csfr(redshift)*(volumesize*h)**3.*1e9), label='Behroozi') 
	plt.plot(np.zeros(1e6)+ 0.66, np.log10(np.arange(1e6)/1e6))
	plt.xlim(0, 1.6)
	plt.legend()
	plt.xlabel('Time [Gyrs]')
	plt.ylabel('Msol/yr/Mpc3')
	plt.savefig('cosmo6BHC52_csfr.png')

if __name__ == '__main__': plot()
