from django.db import models
from link.models import Link
from django.db.models.signals import post_delete
from django.dispatch import receiver

class CircuitIdentity(models.Model):
    email = models.EmailField()
    link_id = models.IntegerField(unique=True)  # Campo para almacenar el ID del enlace
    nombre = models.CharField(max_length=100, null=True)
    url_desplegada = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'circuitIdentity'  

# Definir un receptor para la señal post_delete
@receiver(post_delete, sender=CircuitIdentity)
def delete_related_link(sender, instance, **kwargs):
    try:
        # Intenta eliminar el objeto Link relacionado con el link_id del circuito eliminado
        related_link = Link.objects.get(id=str(instance.link_id))
        related_link.delete()
    except Link.DoesNotExist:
        pass  # Si no se encuentra el objeto Link, no hacer nada