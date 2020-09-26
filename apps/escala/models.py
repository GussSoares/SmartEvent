from django.db import models
from django.utils import timezone

from ..core.models import DefaultModel
from django.utils.translation import gettext as _


class Schedule(DefaultModel):
    descricao = models.TextField(_("Descrição"), null=True, blank=True)
    inicio = models.DateTimeField(_("Início"), null=False, blank=False, default=timezone.now)
    fim = models.DateTimeField(_("Fim"), null=False, blank=False, default=timezone.now)
    obs = models.TextField(_("OBS"), null=True, blank=True)

    class Meta:
        db_table = 'escala'

    def __str__(self):
        return self.descricao


class ScheduleMember(DefaultModel):
    escala = models.ForeignKey('escala.Schedule', null=False, blank=False, on_delete=models.CASCADE)
    membro = models.ForeignKey('cliente.Member', null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        db_table = 'escala_membro'

    def __str__(self):
        return self.membro.cliente.first_name + ' - ' + self.escala.descricao