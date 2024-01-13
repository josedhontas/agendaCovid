from django.core.management.base import BaseCommand
from agenda.models import CustomUser 

class Command(BaseCommand):
    help = 'Cria um superusuário personalizado com base no CPF e senha fornecidos'

    def add_arguments(self, parser):
        parser.add_argument('--cpf', type=str, help='CPF do superusuário')
        parser.add_argument('--password', type=str, help='Senha do superusuário')

    def handle(self, *args, **kwargs):
        cpf = kwargs['cpf']
        password = kwargs['password']

        if not cpf or not password:
            self.stdout.write(self.style.ERROR('É necessário fornecer CPF e senha.'))
            return

        user, created = CustomUser.objects.get_or_create(cpf=cpf, defaults={'is_staff': True, 'is_superuser': True})
        if not created:
            self.stdout.write(self.style.ERROR(f'Superusuário com CPF {cpf} já existe.'))
            return

        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Superusuário com CPF {cpf} criado com sucesso!'))
