# astrophychem
Astrophychem
Scripts will be helpful for reading and writing input output files, data information gathering!

Instructions for running write_anpass_input.py
Attention: You will write your anpass.in anpass2.in in the same directory, make sure your displacement energy.dat is also in this directory, also you need to provide dir where intder.in locates

run:
/home/qcheng1/projects/astrophychem/scripts/write_anpss_input.py anpass.in ../ /home/qcheng1/projects/cu-rovib/CuOH/1ap/av5z-dk-intder/

or

/home/qcheng1/projects/astrophychem/scripts/write_anpss_input.py anpass2.in ../ /home/qcheng1/projects/cu-rovib/CuOH/1ap/av5z-dk-intder/

Instructions for running write_intder_input.py
## provide where the reference geom dir is, also need to have a template file ##
/home/qcheng1/projects/astrophychem/scripts/write_intder_input.py intder_freqs.in ../data/
