from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import EveFittingSerializer
from .models import EveFitting


class FittingView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        fittings = EveFitting.objects.all()
        serializer = EveFittingSerializer(fittings, many=True)
        return JsonResponse(serializer.data, safe=False)
