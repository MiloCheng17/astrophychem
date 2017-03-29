# astrophychem
"""

Astrophychem
Scripts will be helpful for reading and writing input output files, data information gathering!

1. Before you run any of the scripts, make sure you add the lib into your $PYTHONPATH in you .bashrc or .bash_profile file. Something like: (suppose you copied the astrophychem into your home dir)

export PYTHONPATH=/public/apps/python/2.7.10/gcc.4.4.7/lib/python2.7/site-packages:/public/apps/numpy/1.9.2/gcc.4.4.7/python.2.7.10/atlas.3.11.11/lib/python2.7/site-packages:/public/apps/numpy/numpy-1.9.2:$HOME/astrophychem/lib:$PYTHONPATH

If you still don't know how ask!!! You need to set this up first!

2. Instructions for running write_anpass_input.py
Attention: You will write your anpass.in anpass2.in in the same directory, make sure your displacement energy.dat is also in this directory, also you need to provide dir where intder.in locates

run:
/home/qcheng1/projects/astrophychem/scripts/write_anpss_input.py anpass.in ../ /home/qcheng1/projects/cu-rovib/CuOH/1ap/av5z-dk-intder/

or

/home/qcheng1/projects/astrophychem/scripts/write_anpss_input.py anpass2.in ../ /home/qcheng1/projects/cu-rovib/CuOH/1ap/av5z-dk-intder/

3. Instructions for running write_intder_input.py
## provide where the reference geom dir is, also need to have a template file ##
/home/qcheng1/projects/astrophychem/scripts/write_intder_input.py intder_freqs.in ../data/

"""
