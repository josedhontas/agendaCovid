# AgendaCovid

## Sobre o projeto
Este projeto, denominado AgendaCovid, foi desenvolvido por José Dhonatas Alves Sales. Ele consiste em uma aplicação web para gerenciamento de vacinas.

## Tecnologias:
- Telas:
  - HTML
  - CSS
  - Javascript
- Back-end:
  - Django
- Banco de dados:
  - SQLite 

## Requisitos
Para executar este projeto, certifique-se de ter o python instalado em seu computador.

## Como executar

1. Certifique-se de ter o python instalado e configurado em sua máquina.
2. Navegue até o diretório raiz do projeto no terminal.
3. Execute o seguinte comando para instalar as dependencias do projeto:
```shell script
pip install -r requirements.txt
```
4. Para fazer a migrations e instalar os estabelecimentos presentes no arquivo xml use o comando:
```shell script
python manage.py migrate && python manage.py import_estabelecimentos
```
5. Para criar o admin use o comando:
```shell script
python manage.py createsuperuser
```
6. Após a conclusão da instalação das dependências, execute o seguinte comando para iniciar a aplicação:
```shell script
python manage.py runserver
```
7. Após a inicialização, você poderá acessar a aplicação no seu navegador em [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
## Diagrama de entidade relacionamento
![Example Image](https://drive.google.com/uc?id=17Ol6I8_7ajKzDtJJyUZGCnMJaseykNjL)




