# def
import graphene

from ...graphql.package.types import Gaduur
from .models import Package

def generate_unique_mailID(info, instance, data):
  gaduur = graphene.Node.get_node_from_global_id(info, data["gaduur"], Gaduur)
  packages = Package.objects.filter(gaduur__id = gaduur.id).order_by('-name')

  if packages:
    name = packages[0].name
    if name:
      mail_id = int(name[-3:])
      mail_id += 1 

      return name[:-3]+str(mail_id).zfill(3)

  return gaduur.name+"500"
