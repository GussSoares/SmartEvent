from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# from django.utils import timezone
from .models import Schedule, ScheduleMember
from ..cliente.models import Member, Coordinator
import datetime
import pytz
import json

timezone = pytz.timezone(settings.TIME_ZONE)


@csrf_exempt
def create_schedule(request):
    if request.method == 'POST':
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        try:
            with transaction.atomic():
                schedule = Schedule(
                    inicio=datetime.datetime.strptime(start, "%d/%m/%Y %H:%M:%S").astimezone(tz=timezone),
                    fim=datetime.datetime.strptime(end, "%d/%m/%Y %H:%M:%S").astimezone(tz=timezone),
                    descricao=request.POST.get('text'),
                    obs=request.POST.get('obs')
                )
                schedule.save()

                members_list = json.loads(request.POST.get('owner'))
                schedules_members = []
                for m in members_list:
                    schedules_members.append(ScheduleMember(
                        escala=schedule,
                        membro=Member.objects.get(id=m)
                    ))
                ScheduleMember.objects.bulk_create(schedules_members)
        except Exception as exc:
            return JsonResponse({'msg': 'error: '+str(exc)}, status=500)
        return JsonResponse({'id': schedule.id}, status=200)
    return JsonResponse({'msg': 'Method Not Supported'}, status=501)


@csrf_exempt
def update_schedule(request, pk):
    if request.method == 'POST':
        schedule = get_object_or_404(Schedule, pk=pk)
        schedule_members = schedule.schedulemember_set.all()
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        try:
            with transaction.atomic():
                schedule.inicio = datetime.datetime.strptime(start, "%d/%m/%Y %H:%M:%S").astimezone(tz=timezone)
                schedule.fim = datetime.datetime.strptime(end, "%d/%m/%Y %H:%M:%S").astimezone(tz=timezone)
                schedule.descricao = request.POST.get('text')
                schedule.obs = request.POST.get('obs')

                schedule.save()
                # remove os membros da escala
                schedule_members.delete()

                # coloca novamente os membros na escala
                members_list = json.loads(request.POST.get('owner'))
                schedules_members = []
                for m in members_list:
                    schedules_members.append(ScheduleMember(
                        escala=schedule,
                        membro=Member.objects.get(id=m)
                    ))
                ScheduleMember.objects.bulk_create(schedules_members)

        except Exception as exc:
            return JsonResponse({'msg': 'error: '+str(exc)}, status=500)
        return JsonResponse({'id': schedule.id}, status=200)
    return JsonResponse({'msg': 'Method Not Supported'}, status=501)


@csrf_exempt
def delete_schedule(request, pk):
    if request.method == 'POST':
        try:
            schedule = get_object_or_404(Schedule, pk=pk)
            schedule.delete()
        except Exception as exc:
            return JsonResponse({'msg': 'error: '+str(exc)}, status=200)
        return JsonResponse({'msg': 'success'}, status=200)
    return JsonResponse({'msg': 'Method Not Supported'}, status=501)


def get_all_schedules(request):
    # todo: precisa pegar as escalas cujo usuario é coordenador d
    user = request.user

    if user.is_coordinator:
        group = Coordinator.objects.get(cliente=user).grupo
        schedules = Schedule.objects.filter(schedulemember__membro__grupo=group)
    elif user.is_member:
        member = Member.objects.get(cliente=user)
        schedules = Schedule.objects.filter(schedulemember__membro=member)
    else:
        schedules = Schedule.objects.all()

    result = []
    for schedule in schedules:
        result.append({
            'owner': list(schedule.schedulemember_set.all().values_list('membro_id', flat=True)),
            'start_date': schedule.inicio,
            'end_date': schedule.fim,
            'calendarId': '1',
            'category': 'time',
            'id': str(schedule.id),
            'text': schedule.descricao,
            'obs': schedule.obs,
            'membros': list(schedule.schedulemember_set.all().values_list('membro__cliente__first_name', flat=True))
        })
    return JsonResponse({'data': result}, status=200)
