import random
import string
from rest_framework import viewsets
from .models import Link
from .serializers import LinkSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import base64
import json
import os
from django.conf import settings


def generate_unique_random_string(length=30):
    """Genera una cadena aleatoria única de caracteres y números."""
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    # Verificar si la cadena generada ya existe en la base de datos
    while Link.objects.filter(cadena=random_string).exists():
        random_string = ''.join(random.choice(characters) for _ in range(length))
    
    return random_string


@csrf_exempt
def recibir_url_quirk(request):
    if request.method == 'POST':
        # Obtener los datos JSON del cuerpo de la solicitud
        data = json.loads(request.body)
        url_quirk = data.get('urlQuirk')
        screenshot_data_url = data.get('screenshotUrl')

        # Guardar la imagen en el servidor
        screenshot = None
        if screenshot_data_url:
            # Convertir la imagen en base64 a un archivo de imagen
            screenshot_data = screenshot_data_url.split(',')[1]  # Eliminar el encabezado 'data:image/png;base64,'
            screenshot_data_decoded = base64.b64decode(screenshot_data)
            screenshot = ContentFile(screenshot_data_decoded, name='screenshot.png')

        # Guardar la URL y la imagen en la base de datos
        link = Link.objects.create(url=url_quirk, screenshot=screenshot)
        
        # Generar cadena aleatoria única
        random_string = generate_unique_random_string()
        
        # Asociar la cadena aleatoria con el enlace
        link.cadena = random_string
        link.save()
        
        # Devolver la URL original, el ID generado y la cadena como respuesta con un código 200
        return JsonResponse({'id': link.id, 'url': url_quirk, 'cadena': random_string}, status=200)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)





# @csrf_exempt
# def recibir_url_quirk(request):
#     if request.method == 'POST':
#         data = request.POST.get('urlQuirk')
#         # Guardar la URL en la base de datos
#         link = Link.objects.create(url=data)
        
#         # Generar cadena aleatoria única
#         random_string = generate_unique_random_string()
        
#         # Asociar la cadena aleatoria con el enlace
#         link.cadena = random_string
#         link.save()
        
#         # Devolver la URL original, el ID generado y la cadena como respuesta con un código 200
#         return JsonResponse({'id': link.id, 'url': data, 'cadena': random_string}, status=200)
#     else:
#         return JsonResponse({'error': 'Método no permitido'}, status=405)
    




@csrf_exempt
def actualizar_url_circuito(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud como JSON
            data = json.loads(request.body.decode('utf-8'))
            
            # Obtener los datos de la URL, la cadena del circuito y la nueva captura de pantalla
            url_quirk = data.get('urlQuirk', '')
            cadena_circuito = data.get('cadenaCircuito', '')
            screenshot_data_url = data.get('screenshotUrl', '')

            print("URL recibida:", url_quirk)
            print("Cadena de circuito recibida:", cadena_circuito)

            # Buscar si ya existe una entrada con la cadena de circuito
            link = Link.objects.get(cadena=cadena_circuito)

            # Guardar la nueva captura de pantalla si se proporciona
            if screenshot_data_url:
                # Eliminar la captura de pantalla antigua si existe
                if link.screenshot and os.path.isfile(os.path.join(settings.MEDIA_ROOT, link.screenshot.name)):
                    os.remove(os.path.join(settings.MEDIA_ROOT, link.screenshot.name))

                # Convertir la nueva captura de pantalla de base64 a un archivo de imagen
                screenshot_data = screenshot_data_url.split(',')[1]
                screenshot_data_decoded = base64.b64decode(screenshot_data)
                screenshot = ContentFile(screenshot_data_decoded, name='screenshot.png')
                link.screenshot = screenshot

            # Actualizar la URL
            link.url = url_quirk
            link.save()

            # Devolver la URL actualizada como respuesta
            print("URL actualizada correctamente")
            return JsonResponse({'url': link.url}, status=200)
        except Link.DoesNotExist:
            print("Error: No se encontró ninguna cadena de circuito asociada")
            return JsonResponse({'error': 'No se encontró ninguna cadena de circuito asociada'}, status=404)
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'error': 'Error en el servidor'}, status=500)
    else:
        print("Error: Método no permitido")
        return JsonResponse({'error': 'Método no permitido'}, status=405)






# @csrf_exempt
# def actualizar_url_circuito(request):
#     if request.method == 'POST':
#         try:
#             # Decodificar el cuerpo de la solicitud como JSON
#             data = json.loads(request.body.decode('utf-8'))
            
#             # Obtener los datos de la URL y la cadena del circuito del cuerpo de la solicitud
#             url_quirk = data.get('urlQuirk', '')
#             cadena_circuito = data.get('cadenaCircuito', '')
            
#             print("URL recibida:", url_quirk)
#             print("Cadena de circuito recibida:", cadena_circuito)

#             # Buscar si ya existe una entrada con la cadena de circuito
#             link = Link.objects.get(cadena=cadena_circuito)
#             # Si existe, actualizar la URL
#             link.url = url_quirk
#             link.save()
#             # Devolver la URL actualizada como respuesta
#             print("URL actualizada correctamente")
#             return JsonResponse({'url': link.url}, status=200)
#         except Link.DoesNotExist:
#             # Si no existe, devolver un mensaje de error
#             print("Error: No se encontró ninguna cadena de circuito asociada")
#             return JsonResponse({'error': 'No se encontró ninguna cadena de circuito asociada'}, status=404)
#         except Exception as e:
#             # Manejar cualquier otro error que pueda ocurrir durante el procesamiento
#             print("Error:", e)
#             return JsonResponse({'error': 'Error en el servidor'}, status=500)
#     else:
#         print("Error: Método no permitido")
#         return JsonResponse({'error': 'Método no permitido'}, status=405)




@csrf_exempt
def get_id_from_cadena(request):
    if request.method == 'GET':
        cadena = request.GET.get('cadena') # Obtener la cadena de los parámetros GET
        try:
            # Buscar el enlace asociado con la cadena
            link = Link.objects.get(cadena=cadena)
            return JsonResponse({'id': link.id}, status=200)
        except Link.DoesNotExist:
            return JsonResponse({'error': 'No se encontró ningún enlace asociado con la cadena proporcionada'}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
