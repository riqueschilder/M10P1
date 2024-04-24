# PlayList com proteção de rotas
Playlist Maker feita em Flask utilizando uma proteção de rotas feita com JWT.

## Como executar?
Para executar, primeiro precisamos baixar as bibliotecas Flask, flask_jwt_extended e Flask_sqlalchemy, após isso precisamos digitar o seguinte comando para criar um banco de dados para nós:
```
python3 main.py create_db
```

Após isso, teremos uma pasta chamada Instance com um banco em sqlite3, então só temos que iniciar nossa aplicação para termos uma API com interface funcionando:
```
python3 -m flask --app main run
```

Com isso, só precisamos acessar o seguinte endereço: [http://localhost:5000/user-login](http://localhost:5000/user-login)

Com isso, podemos usar toda a interface da aplicação e as rotas documentadas tanto pelo Insomnia, quanto Swagger, quanto interface.
