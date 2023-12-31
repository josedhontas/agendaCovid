from django.core.management.base import BaseCommand
from agenda.models import Estabelecimento
import xml.etree.ElementTree as ET

class Command(BaseCommand):
    help = 'Importa dados de XML para Estabelecimento'

    def handle(self, *args, **options):
        tree = ET.parse('agenda/dados/estabelecimentos_pr.xml')
        root = tree.getroot()

        for estabelecimento_xml in root.findall('estabelecimento'):
            cnes = estabelecimento_xml.find('co_cnes').text
            nome = estabelecimento_xml.find('no_fantasia').text

            Estabelecimento.objects.create(cnes=cnes, nome=nome)

        self.stdout.write(self.style.SUCCESS('Dados importados com sucesso!'))
