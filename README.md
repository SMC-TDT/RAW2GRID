# RAW2GRID
Aquest programari en llenguatge Python 3 permet, partir de les dades RAW volumètriques (PPIVOL_B i PPIVOL_C) d’un o més radars, generar un producte cartesià en 3D, el qual s’emmagatzema en un arxiu amb format netCDF4.

## DESCRIPCIÓ

L’algorisme interpola les dades en coordenades radar (el, az, r) a una quadrícula cartesiana 3D (x, y, z). Per fer la interpolació, l'algorisme defineix, al voltant de cada bin radar, un radi d'influència (RoI) i determina quins punts de la quadrícula cartesiana conté. Després, al valor de la dada de cadascun d'aquests punts inclosos en el RoI li suma la contribució adient de la dada del bin radar. La contribució a cada punt cartesià es calcula segons una funció d'assignació de pesos Gaussiana, depenent de la distància entre el bin del radar i el punt cartesià.

### Estructura de carpetes:

La carpeta RAW2GRID ha de contenir 3 carpetes:
- PROG: conté els dos scripts necessaris per a la configuració i execució de l’algorisme (*raw2grid_settings.py* i *raw2grid.py*).
- RAW: és la carpeta d’entrada on s’han de copiar els arxius RAW.
- netCDF4: és la carpeta de sortida on el programari emmagatzema els productes netCDF4 finals.

### Llibreries Python:
- py-art
- numpy
- math
- glob
- os
- datetime

## INSTRUCCIONS D'ÚS

1. Copieu els arxius RAW comprimits del període desitjat (XXXRAWYYYYMMDD.tgz) a la carpeta *./GRID2RAW/RAW/*.

  `$ cp CDVRAW20210724.tgz ./GRID2RAW/RAW`

2. Per a cada arxiu .tgz:
  
    1. Descomprimiu l’arxiu en la carpeta *./GRID2RAW/RAW/*:
    
      `$ cd ./GRID2RAW/RAW`
      
      `$ tar xzf CDVRAW20210724.tgz`
  
    2. Elimineu els arxius PPIVOL_A:
    
      `$ grep -rw . -e 'PPIVOL_A'| xargs rm -fr`
    
    3. Creeu una carpeta amb nom *XXXRAWYYYYMMDD* i moveu-hi els arxius:
    
      `$ mkdir CDVRAW20210724`
    
      `$ mv *.RAW* ./CDVRAW20210724`
    
3. En l’arxiu de configuració *raw2grid_settings.py*, modifiqueu com calgui els camps en les seccions: 
- CONFIGURACIÓ GENERAL
- CONFIGURACIÓ DE DIRECTORIS
- CONFIGURACIÓ DE LA QUADRÍCULA
- CONFIGURACIÓ DE L’ALGORISME (opcional)

4. Aneu al directori *./GRID2RAW/PROG/* i executeu l’script principal:
  
  `$ cd ../PROG`
  
  `$ python3 ./raw2grid.py`
  
5. Si tot va bé, trobareu els arxius netCDF4 amb el producte de sortida a la carpeta *./RAW2GRID/netCDF4/*.
