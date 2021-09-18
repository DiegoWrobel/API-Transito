import requests
import json
import os
import gmplot

key = ''        # Key de la API de Google Maps (Dejar en blanco si no tenes)
client_id = ''  # Token de la API Transporte
secret = ''     # Token de la API Transporte https://www.buenosaires.gob.ar/desarrollourbano/transporte/apitransporte

url = "https://apitransporte.buenosaires.gob.ar/transito/v1/cortes?client_id={client_id]&client_secret={secret}"
r = requests.get(url)
data = json.loads(r.text)
for i in range(len(data['incidents'])):
    print("id:", data['incidents'][i].get('id', 'Sin id'))
    print("Evento padre:", data['incidents'][i].get('parent_event', 'Sin evento padre'))
    print("Tipo :", data['incidents'][i].get('type', 'Sin tipo'))
    print("Descripcion:", data['incidents'][i].get('description', 'Sin descripcion'))
    if (data['incidents'][i].get('location', False)) == False:
        print("Calle:", 'Sin datos')
        print("Linea:", 'Sin datos')
        print("Direccion:", 'Sin datos')
    else: #tiene ubicacion
        print("Calle:", data['incidents'][i]['location']['street'])
        print("Linea:", data['incidents'][i]['location']['polyline'])
        print("Direccion:", data['incidents'][i]['location']['direction'])
    print("Creacion:", data['incidents'][i].get('creationtime', 'Sin fecha de creacion'))
    print("Actualizacion:", data['incidents'][i].get('updatetime', 'Sin fecha de actualizacion'))
    print("Inicio:", data['incidents'][i].get('starttime', 'Sin hora de inicio'))
    print("Fin:", data['incidents'][i].get('endtime', 'Sin hora de finalizacion'))
    print("################################################################################################")
#--------------------------------------------------------------------------------------------------------------------

gmap = gmplot.GoogleMapPlotter(-34.647335052490234, -58.41842269897461, 11, apikey=key, title="CORTES", map_type='roadmap')

id = []
posiciones = []

for i in range(len(data['incidents'])):
    if (data['incidents'][i].get('location', False)) != False:
        id.append(data['incidents'][i]['id'])
        posiciones.append(data['incidents'][i]['location']['polyline'].split(' '))

for i in range(len(posiciones)):  #// Remueve el ultimo registro que es ''
    del posiciones[i][-1]

geo=posiciones

for i in range(len(geo)):
    listlat=[]
    listlon=[]

    for x in range(int(len(geo[i])/2)):
        listlat.append(float(geo[i].pop(0)))
        listlon.append(float(geo[i].pop(0)))
    
    gmap.scatter(listlat, listlon, '#FF0000',size = 10, marker = True )
    gmap.plot(listlat, listlon, 'cornflowerblue', edge_width=10)
    gmap.text(listlat[0], listlon[0], id[i], color='red')

os.getcwd()
gmap.draw(os.getcwd()+"\cortes.html")
print("Mapa en", os.getcwd() + "\cortes.html")
