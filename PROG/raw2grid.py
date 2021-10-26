#!/usr/bin/python3
# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import pyart
import glob
import os
from raw2grid_settings import *
from datetime import datetime, timedelta
import math as m

## FUNCIONS ##############################################################

def dt_list(dt_i, dt_f, delta_min=6, fmt='%y%m%d%H%M'):
    """
    Given the start and end datetimes and a timestep, 
    generates a list of sequential datetime objects

    Parameters
    ----------
    dt_i : datetime object 
        Start datetime
    dt_f : datetime object 
        End datetime

    Optional parameters
    -------------------
    delta_min : float
        Time-step in minutes
    fmt : datetime formatting string
        Output datetime format

     Returns
     -------
     dt_lst : list of datetime objects
         Sequential datetimes from dt_i to dt_f in delta_min steps
     """

    dt_lst = [dt_i.strftime(fmt)]
    
    dt = dt_i
    while dt < dt_f:
        dt += timedelta(minutes=delta_min)
        dt_lst.append(dt.strftime(fmt))

    return dt_lst

def RAW2radar(path, radar, datetime, task='PPIVOL_B'):
    f = glob.glob(path + radar + datetime + '*')
    if f:
            rad = pyart.io.read(f[0])
            print(rn + ' ' + task + ' ' + datetime + ': OK')

            # TEMPORAL: el radar PBE conté les dades W només en les 
            # tasques PPIVOL_B, fet que origina un error en agrupar les 
            # dades PPIVOL_B i PPIVOL_C
            if 'spectrum_width' in rad.fields.keys():
                rad.fields.pop('spectrum_width')
            
            return(rad)

    else:
            print(rn + ' ' + task + ' ' + datetime + ': file not found')

def joinBC(radarB, radarC):

    if radarB is not None and radarC is not None:
        radarBC = pyart.util.join_radar(radarB, radarC)
    else:
        radarBC = list(filter(None, [radarB, radarC]))
        if radarBC:
            radarBC = radarBC[0]
        else:
            radarBC = None
     
    return(radarBC)

##########################################################################

# Objectes 'datetime' inicial i final
dt_i = datetime.strptime(date_i + time_i, '%Y%m%d%H:%M')
dt_f = datetime.strptime(date_f + time_f, '%Y%m%d%H:%M')

# Llistes de data i hora dels arxius PPIVOL_B i PPIVOL_C 
dtB_lst = dt_list(dt_i, dt_f)
dtC_lst = dt_list(dt_i+timedelta(minutes=2), dt_f + timedelta(minutes=2))

# Generació dels arxius de sortida per a cada data i hora
for i, dt in enumerate(dtB_lst):

    dtB = dtB_lst[i]
    dtC = dtC_lst[i]
    
    # Nom de l'arxiu de sortida
    fo = path_out + ''.join(map(str, radars)) + dtB + '.nc'
    date = datetime.strptime(dt, '%y%m%d%H%M').strftime('%Y%m%d')

    # Generació d'un objecte radar que contingui les dades 
    # de tots els radars requerits 
    rad2grid = []
    for rn in radars:

        # Directori amb les dades RAW de la data corresponent
        path_dat = path_inp + rn + "RAW" + date + "/"

        if os.path.isdir(path_dat):

            radB = RAW2radar(path=path_dat, radar=rn, 
                             datetime=dtB, task='PPIVOL_B')
            radC = RAW2radar(path=path_dat, radar=rn, 
                             datetime=dtC, task='PPIVOL_C')

            # Agrupa dades PPIVOL_B i PPIVOL_C en un únic objecte radar
            radBC = joinBC(radB, radC)

            # Afegeix l'objecte radar a la llista d'objectes radar
            rad2grid.append(radBC)
        
        else:
            print('No input folder found for ' + rn)

    rad2grid = (list(filter(None, rad2grid)))
    
    if rad2grid:      
        # Interpolació de la llista d'objectes radar a la quadrícula
        grid = pyart.map.grid_from_radars(tuple(rad2grid), 
                                        grid_shape=grid_dim,
                                        grid_limits=grid_lims,
                                        fields=grid_fields,
                                        roi_func=roi_func,
                                        min_radius=min_R,
                                        nb=beam_w,
                                        bsp=beam_sp,
                                        weighting_function=w_fun,
                                        toa=toa)

        # Write grid object to output netcdf4 file
        pyart.io.write_grid(fo, grid)

        print('OUTPUT FILE: ' + fo)
    else:
        print('!! OUTPUT FILE NOT CREATED: no data found')
