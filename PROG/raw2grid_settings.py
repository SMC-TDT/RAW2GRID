#!/usr/bin/python3
# coding: utf-8

## CONFIGURACIÓ GENERAL ##################################################

# Data i hora inicial i final del periode a processar
date_i = "20210725"
time_i = "00:00"

date_f = "20210725"
time_f = "00:06"

# Llista dels radars que contribuiran a la solució final 
radars = ["CDV", "PBE"]

## CONFIGURACIÓ DE DIRECTORIS ############################################

# Directori general de treball
path_wrk = "~/RAW2GRID/" 

# Directoris d'entrada (arxius RAW) i sortida (arxius netCDF4)
path_inp = path_wrk + "RAW/"
path_out = path_wrk + "netCDF4/"

## CONFIGURACIÓ DE LA QUADRÍCULA #########################################
# NOTA: La projecció cartesiana de la quadrícula és azimutal equidistant 
# per defecte. L'origen de la quadrícula (lat, lon, z) és la localització 
# del primer radar en la llista

# Nombre de bins (z, x, y)
grid_dim = (21, 301, 301)

# Limits de la quadrícula en km ((z_i, z_f), (x_i, x_f), (y_i, y_f))
grid_lims = ((0., 10000.,), (-150000., 150000.), (-150000., 150000.))

# Llista de dades/moments a interpolar
grid_fields = ['reflectivity', 'velocity']

# Alçada màxima de l'atmosfera (metres), les dades per sobre d'aquesta no 
# s'inclouen en l'interpolació
toa = 17000.

## CONFIGURACIÓ DE L'ALGORISME ###########################################
# NOTA: l'algorisme defineix, al voltant de cada bin radar, un radi 
# d'influència (R) que conté una sèrie de punts de la quadrícula cartesiana. 
# Després, al valor de la dada de cadascun d'aquests punts inclosos en el R
# li suma la contribució de la dada del bin radar. Aquesta contribució es 
# calcula segons una funció d'assignació de pesos. 

# Funció pel càlcul del radi d'influència (R): el radi augmenta amb la 
# distància a cada radar, en base a la mida del feix virtual del radar
roi_func = 'dist_beam'
min_R = 500. # radi d'influència mínim (metres)
beam_w = 1.2 # amplada del feix virtual (angle en graus)
beam_sp = 1  # distàcia entre feixos (angle en graus)

# Assignació de pesos (w) en funció de la distància entre el bin del radar i 
# el punt cartesià (r)
#   'Nearest': funció lineal w ~ r
#   'Cressman': funció tipus parabòlic w ~ (R^2-r^2)/(R^2+r^2)
#   'Barnes2': funció gaussiana w ~ exp(-r^2/4k)
w_fun = 'Barnes2'
