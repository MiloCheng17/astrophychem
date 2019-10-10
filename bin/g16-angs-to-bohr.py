from coord_convert import *

def run_system(cmd):
    print(cmd)
    os.system(cmd)

cmd = '/public/apps/gaussian/g16/newzmat -izmat -ocart ' + 'ref.int' + ' ' + 'ref.out'
os.system(cmd)
gangstrom_bohr('ref.out','ref.out-bohr')
