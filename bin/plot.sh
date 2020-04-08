#!/bin/sh

gnuplot <<- EOP

set term png transparent truecolor
set output 'energy_surface.png'
#unset xlabel
#unset xtics
#unset ylabel
#unset ytics
#unset border
unset key
#splot 'bond_angle_energy.dat' using 1:2:7 with points palette pointsize 1 pointtype 7
set view map
set size ratio .9

set object 1 rect from graph 0, graph 0 to graph 1, graph 1 back
set object 1 rect fc rgb "black" fillstyle solid 1.0

splot "bond_angle_energy.dat" using 1:2:7 with points pointtype 5 pointsize 1 palette linewidth 30
EOP
