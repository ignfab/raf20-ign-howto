from shapely.geometry import Point
from shapely.ops import transform
import pyproj
import math

# Point terrain test
x = 730871 # x en 2154
y = 6336988 # y en 2154
z = 918 # altitude

# Lecture du fichier RAF20.tac
with open('RAF20.tac') as f:
    
    line = f.readline()
    params = line.split()

    min_lon = float(params[0])
    max_lon = float(params[1])
    min_lat = float(params[2])
    max_lat = float(params[3])
    step_lon = float(params[4])
    step_lat = float(params[5])

    # Chargement des données de RAF20.tac dans un tableau 2D
    # 0,0 = longitude minimale, latitude minimale
    # longitude croissante sur l'axe i
    # latitude croissante sur l'axe j
    h = int((max_lat - min_lat) / step_lat) + 1
    w = int((max_lon - min_lon) /  step_lon) + 1
    raf20 = [[0 for x in range(h)] for y in range(w)] 

    i = 0
    j = h-1
    while line:
        line = f.readline()
        h_elips_row = line.split()[::2]
        for h_elips in h_elips_row:
            c = [min_lon+i*step_lon, min_lat+j*step_lat, float(h_elips)]
            raf20[i][j] = c
            i+=1
            if i==w:
                j-=1
                i=0

p = Point(x,y,z)
lamb93 = pyproj.CRS('EPSG:2154')
wgs84 = pyproj.CRS('EPSG:4326')
to4326 = pyproj.Transformer.from_crs(lamb93, wgs84,always_xy=True).transform
p_4326 = transform(to4326, p)

# interpolation bilinéaire
n = math.floor((p_4326.x - min_lon) / step_lon)
p = math.floor((p_4326.y - min_lat) / step_lat)
x = ((p_4326.x - min_lon) / step_lon) % 1
y = ((p_4326.y - min_lat) / step_lat) % 1
T = (1-x)*(1-y)*raf20[n][p][2] + x*(1-y)*raf20[n+1][p][2] + y*(1-x)*raf20[n][p+1][2]  + x*y*raf20[n+1][p+1][2] 

print("Valeur interpolée " + str(T))
print("Hauteur au dessus de l'ellispoide " + str(z+T))
