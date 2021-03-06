import numpy as np
import glob
import struct
import pdb
import re


class Nchilada(object):
    def __init__(self, filename):
        self.codedict = {1: 'int8', 
                         2: 'uint8',
                         3: 'int16',
                         4: 'uint16',
                         5: 'int32',
                         6: 'uint32',
                         7: 'int64',
                         8: 'uint64', 
                         9: 'float32',
                         10: 'float64'}
        self.fmt_codedict = {1: 'h',
                             2: 'H',
                             3: 'i',
                             4: 'I',
                             5: 'l',
                             6: 'L',
                             7: 'q',
                             8: 'Q',
                             9: 'f',
                             10: 'd'}



        self.codedictlen = {1: 1
                            }
        self.filename = filename

    def read_param(self):
        try:
            paramfilename = [f for f in glob.glob('*.param') if re.match('^(cosmo|h)', f)][0]
        except IndexError:
            try:
                paramfilename = [f for f in glob.glob('../*.param') if re.match('^(cosmo|h)', f)][0]
                print 'There is no param file in this directory, trying one up'
            except IndexError:
                print "Can't find param file"
                return
        f = open(paramfilename, 'rb')
        paramfile = {}
        for line in f:
            try:
                if line[0] != '#':
                    s = line.split('#')[0].split()
                    paramfile[s[0]] = "".join(s[2:])
            except IndexError, ValueError:
                pass
        self.paramfile = paramfile
        dKpcUnit = np.float(paramfile['dKpcUnit'])
        dMsolUnit = np.float(paramfile['dMsolUnit'])
        self.timeunit=np.sqrt((dKpcUnit*3.086e21)**3/
                              (6.67e-8*dMsolUnit*1.99e33)
                              )/(3600.*24.*365.24*1e9)
        try: hub = np.float(paramfile['dHubble0'])
        except KeyError: hub=0.
        dunit = np.float(paramfile['dKpcUnit'])
        munit = np.float(paramfile['dMsolUnit'])
        denunit = munit/dunit**3.
        self.velunit = 8.0285*np.sqrt(6.6743e-8*denunit)*dunit
        hubunit = 10.*self.velunit/dunit
        self.h = hub*hubunit
        f.close()
    
    def unpack_header(self, family, file):
        f = open(self.filename+'/'+family+'/'+file)
        (magic, time, iHighWord, nbodies, ndim, code) = struct.unpack('>idiiii', f.read(28))
        if (ndim < 1) or (ndim > 3):
            f.seek(0)
            (magic, time, iHighWord, nbodies, ndim, code) = struct.unpack('<idiiii', f.read(28))
            self.byte_swap = True
        f.close()
        return(time, nbodies, ndim, code)
    
    def unpack_file(self, family, file):
        time, nbodies, ndim, code = self.unpack_header(family, file)
        self.time = time
        self.nbodies = nbodies
        self.ndim = ndim
        f = open(self.filename+'/'+family+'/'+file)
        f.seek(28)
        minvalue = struct.unpack('>'+self.fmt_codedict[code],f.read(4))[0]
        maxvalue = struct.unpack('>'+self.fmt_codedict[code],f.read(4))[0]
        dtype = np.dtype({'names':('array',),'formats':('>'+self.fmt_codedict[code],)})
        ar = np.core.records.fromfile(f, dtype=dtype, shape=self.nbodies)
        return ar['array']

    def minvalue(self, family, file):
        time, nbodies, ndim, code = self.unpack_header(family, file)
        self.time = time
        self.nbodies = nbodies
        self.ndim = ndim
        f = open(self.filename+'/'+family+'/'+file)
        f.seek(28)
        minvalue = struct.unpack('>'+self.fmt_codedict[code],f.read(4))[0]
        maxvalue = struct.unpack('>'+self.fmt_codedict[code],f.read(4))[0]
        return minvalue

    def maxvalue(self, family, file):
        time, nbodies, ndim, code = self.unpack_header(family, file)
        self.time = time
        self.nbodies = nbodies
        self.ndim = ndim
        f = open(self.filename+'/'+family+'/'+file)
        f.seek(28)
        minvalue = struct.unpack('>'+self.fmt_codedict[code],f.read(4))[0]
        maxvalue = struct.unpack('>'+self.fmt_codedict[code],f.read(4))[0]
        return maxvalue
