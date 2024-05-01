from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from webapp.Arbol.ArbolDecisiones import clasificar

@csrf_exempt
def diagnose(request):
    if request.method == 'POST':
        # Obtiene los datos de la solicitud POST
        data = json.loads(request.body.decode('utf-8'))

        # Extrae los síntomas de la solicitud
        symptoms = data.get('symptoms')
        print("Síntomas recibidos:", symptoms)  # Agregar esta línea para depurar

        # Verifica si se proporcionaron síntomas
        if not symptoms:
            return JsonResponse({"error": "No se proporcionaron síntomas"}, status=400)

        # Llama a la función clasificar con los síntomas
        results_gb = clasificar(symptoms)

        # Crea un JSON con los resultados y lo devuelve como respuesta
        response_data = {
            "gb": results_gb.to_dict(orient='records')
        }

        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Solicitud no permitida"}, status=405)
