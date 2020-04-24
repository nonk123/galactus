from django.http import JsonResponse

def galactus(req):
    return JsonResponse({
        "galactus_says": "hmm?"
    })
