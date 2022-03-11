#!/usr/bin/env python3

import grass.script as gs
from os import listdir
import os
from os.path import isfile, join

def main():

    '''
    You need GrassGIS installed for this script. You may directly run the code within the software environment.

    :return: A topology corrected line shapefile
    '''

    path = os.path.join("D:/", "Ebola", "grass", "Ebola", "output")
    onlyfiles = [f for f in listdir(path) if ('.shp' in f) and ('.xml' not in f)]
    for f in onlyfiles:
        i = os.path.join(path, f)
        name = f.replace('.shp', '')
        o = os.path.join(path, name + '_corrected.shp')
        gs.run_command('v.in.ogr', input=i, output='read', overwrite='True',)
        # Break roads at all intersections
        gs.run_command("v.clean", input='read', tool='break', flags="c", overwrite='True', output='brk')
        # Remove dangles (overshoot)
        gs.run_command("v.clean", input='brk', tool='rmdangle', threshold=10, overwrite='True', output='r_dngl')
        gs.run_command("v.clean", input='r_dngl', tool='chdangle', overwrite='True', output='ch_dngl')
        # Snap undershoots
        gs.run_command("v.clean", input='ch_dngl', tool='snap', threshold=10, overwrite='True', output='snp')
        gs.run_command("v.out.ogr", input='snp', type='line', format='ESRI_Shapefile',  overwrite='True', output='topo.shp')
        gs.run_command("v.import", input='topo.shp', output='topo', extent='input', overwrite='True')
        # Update road lengths
        gs.run_command("v.db.addcolumn", map='topo', columns="len DOUBLE PRECISION")
        gs.run_command("v.to.db", map='topo', qlayer=1, option='length', units='meter', columns="len", overwrite='True')
        gs.run_command("v.out.ogr", input='topo', type='line', format='ESRI_Shapefile', overwrite='True', output=o)

if __name__ == '__main__':
    main()