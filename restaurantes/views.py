from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from restaurantes.forms import RestForm
from django.http import HttpResponseRedirect
from django.urls import reverse
import re



db = settings.DB
col = db.restaurants


success=-1
ult_busqueda=''


def index(request):
    return render(request, 'restaurantes/home.html')


def restaurantes(request):
    global success, ult_busqueda

    if request.method == "POST" and request.POST.get("search", "")!='':
        ult_busqueda = request.POST.get("search", "")
        regex = ".*" + ult_busqueda + ".*";
        rest =  list(col.find({"name":{"$regex":re.compile(regex, re.IGNORECASE)}}))

    else:
        rest = list(col.find().skip(col.count() - 10))
        
    ult_b = ult_busqueda
    ult_busqueda = ''
    context = {'rest': rest, 'success' : success, 'ult_busqueda': ult_b, 'length' : len(rest)}
    success=-1

    return render(request, 'restaurantes/restaurantes.html', context)

@login_required
def editar_restaurante(request):
    global success
    if request.method == "POST":
        form = RestForm(request.POST)
        if form.is_valid():
            id_rest = form.cleaned_data['iden']
            ciudad = form.cleaned_data['ciudad']
            nombre = form.cleaned_data['nombre']
            cuisine = form.cleaned_data['cuisine']
            ciudad = form.cleaned_data['ciudad']
            edificio = form.cleaned_data['edificio']
            calle = form.cleaned_data['calle']
            codpostal = form.cleaned_data['codpostal']
            latitud = form.cleaned_data['latitud']
            longitud = form.cleaned_data['longitud']
            success = updateRestaurante(id_rest,nombre,cuisine,ciudad,edificio,calle,codpostal,latitud,longitud)
            return redirect('restaurantes')
        else:
            return render(request, 'restaurantes/editar_restaurante.html', {'form': form})
    else:
        id_rest =  request.GET.get('id_rest', '')
        restaurante = list(col.find({'restaurant_id' : id_rest}))
        form = RestForm(restaurante=restaurante[0])
        context = {'restaurante': restaurante[0], 'form': form}
        return render(request, 'restaurantes/editar_restaurante.html', context)


@login_required
def agregar_restaurante(request):
    global success
    if request.method == "POST":
        form = RestForm(request.POST)
        if form.is_valid():
            id_rest = form.cleaned_data['iden']
            ciudad = form.cleaned_data['ciudad']
            nombre = form.cleaned_data['nombre']
            cuisine = form.cleaned_data['cuisine']
            ciudad = form.cleaned_data['ciudad']
            edificio = form.cleaned_data['edificio']
            calle = form.cleaned_data['calle']
            codpostal = form.cleaned_data['codpostal']
            latitud = form.cleaned_data['latitud']
            longitud = form.cleaned_data['longitud']

            success = insertarRestaurante(id_rest,nombre,cuisine,ciudad,edificio,calle,codpostal,latitud,longitud)
            return redirect('restaurantes')


        else:
            return render(request, 'restaurantes/agregar_restaurante.html', {'form': form})
    else:
        form = RestForm()
        return render(request, 'restaurantes/agregar_restaurante.html', {'form': form})


# funciones de insert y update los restaurantes


def insertarRestaurante(id_rest,nombre,cuisine,ciudad,edificio,calle,codpostal,latitud,longitud):
  success = 2
  if col.find_one({'restaurant_id': id_rest}) == None:
      success = 1
      res = col.insert_one(
  		    {
  		    	"address": {
     	    		"building": edificio,
     	    		"coord": [ float(latitud), float(longitud) ],
     	    		"street": calle,
     	    		"zipcode": codpostal
  		    	},
  			    "borough": ciudad,
  			    "cuisine": cuisine,
  			    "grades": [],
  			    "name": nombre,
  		    	"restaurant_id": id_rest
		    }
      )
          
  return success


def updateRestaurante(id_rest,nombre,cuisine,ciudad,edificio,calle,codpostal,latitud,longitud):
  res = col.update({'restaurant_id':id_rest}, 
              {
  		    	"address": {
     	    		"building": edificio,
     	    		"coord": [ float(latitud), float(longitud) ],
     	    		"street": calle,
     	    		"zipcode": codpostal
  		    	},
  			    "borough": ciudad,
  			    "cuisine": cuisine,
  			    "grades": [],
  			    "name": nombre,
  		    	"restaurant_id": id_rest
		    }
            , upsert=False)
  return res['nModified']


# necesito estar logueado para ver lo de eliminar restaurante

@login_required
def eliminar_restaurante(request):
    global success
    if request.method == "GET":
        id_rest =  request.GET.get('id_rest', '')
        col.remove({'restaurant_id':id_rest})
    
    success = 1

    return redirect('restaurantes')
        





