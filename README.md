# AgendaCovid

## Sobre o projeto
O **AgendaCovid** é uma aplicação web desenvolvida por José Dhonatas Alves Sales para agendamento de testes de Covid-19.

## Tecnologias Utilizadas:
- **Telas:**
  - HTML
  - CSS
  - Javascript
- **Back-end:**
  - Django
- **Banco de dados:**
  - SQLite 

## Requisitos
Antes de executar este projeto, certifique-se de ter o Python instalado em seu computador.

## Como Executar

1. Certifique-se de ter o Python instalado e configurado em sua máquina.
2. Navegue até o diretório raiz do projeto no terminal.
3. Execute o seguinte comando para instalar as dependências do projeto:
    ```shell script
    pip install -r requirements.txt
    ```
4. Para criar as migrações e importar os estabelecimentos do XML, utilize o comando:
    ```shell script
    python manage.py migrate && python manage.py import_estabelecimentos
    ```
5. Crie um superusuário para acessar o painel administrativo:
    ```shell script
    python manage.py createsuperuser
    ```
6. Após a conclusão da instalação das dependências, inicie a aplicação com o seguinte comando:
    ```shell script
    python manage.py runserver
    ```
7. Após a inicialização, acesse a aplicação no seu navegador através de [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Aplicação em Deploy
A aplicação foi hospedada no Render e pode ser acessada pelo seguinte endereço: [agendaCovid](https://agendacovid.josedhonatas.ninja/)

Informações de teste:
| Cargo | CPF           | Senha  |
|-------|---------------|--------|
| admin | 08879520547   | admin  |

## Diagrama de Entidade-Relacionamento
![Diagrama ER](https://drive.google.com/uc?id=17Ol6I8_7ajKzDtJJyUZGCnMJaseykNjL)
