from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse, response
from agenda.models import Agendamento
from agenda.serializers import *
from rest_framework.decorators import api_view

# o uso do decorators é simples ela determina que tipo de requisição
#a função vai receber, exemplo ["GET"]
@api_view(http_method_names=["GET", "PATH", "DELETE"])
def agendamento_detail(request,id):
    
    if request.method == "GET":
        obj = get_object_or_404(Agendamento, id=id)
        serializer = AgendamentoSerializer(obj) 
        return JsonResponse(serializer.data)
    if request.method == "PATH":
        obj = get_object_or_404(Agendamento, id=id)
        serializer = AgendamentoSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            v_data = serializer._validated_data
            obj.data_horario = v_data.get("data_horario", obj.data_horario)
            obj.nome_cliente= v_data.get("nome_cliente", obj.nome_cliente)
            obj.email_cliente = v_data.get("email_cliente", obj.email_cliente)
            obj.telefone_cliente = v_data.get("telefone_cliente", obj.telefone_cliente)
            obj.save()
            return JsonResponse(v_data , status=200)
        return JsonResponse(serializer.errors, status=400)
    if request.method == "DELETE":
        obj = get_object_or_404(Agendamento, id=id)
        obj.delete()
        obj.cancelado = True
        return response(status=204)
@api_view(http_method_names=["GET", "POST"])
def agendamento_list(request):
        
    if request.method == "GET":
        qs = Agendamento.objects.all()
        # consigo atraves desta linha abaixo listar todos os meus dados contido no modelo adicionando o MANY=TRUE pq ele meio que 
        # transfoma todas as informações em uma lista
        serializer = AgendamentoSerializer(qs, many=True)
        # quando carregar as informações provavelmente ele iria retona um erro como: 
        # In order to allow non-dict objects to be serialized set the safe parameter to False
        # pra resolver é só passar no retun o safe=False
        return JsonResponse(serializer.data, safe=False)
    if request.method == "POST":
        data = request.data
        serializer = AgendamentoSerializer(data=data)
        if serializer.is_valid():
            validated_data =serializer.validated_data
            Agendamento.objects.create(
                data_horario = validated_data["data_horario"],
                nome_cliente = validated_data["nome_cliente"],
                email_cliente = validated_data["email_cliente"],
                telefone_cliente = validated_data["telefone_cliente"],
            )

            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status= 400)