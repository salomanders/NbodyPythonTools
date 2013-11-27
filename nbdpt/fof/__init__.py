"""
modules
--------

fof2stat
  Fof is a quick halo finder to run for quick results. This creates a 
  stat file from the grp/gtp outputs

fofscript
  Creates a bash script to run fof on all snapshots in a directory.
  Currently depends on some previous runs to calculate the correct
  linking length. I need to fix that. 

mvfof2amiga
  Pynbody expects .amiga.grp files, this converts the fof outputs to
  filenames that pynbody will accept. This means that amiga.grp files
  in a directory might not be run by amiga :/

"""

from . import checkden, fof2stat, foflinkinglength, fofscript, mvfof2amiga
