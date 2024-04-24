from flask import Flask
from database.database import db
from flask import jsonify, request, render_template, make_response
from database.models import User, ToDoList
from flask_jwt_extended import JWTManager, set_access_cookies, create_access_token, get_jwt_identity, jwt_required
import requests as http_request
import json
from flasgger import Swagger

app = Flask(__name__, template_folder="templates")
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
# initialize the app with the extension
db.init_app(app)
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "gojo" 
# Seta o local onde o token será armazenado
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
jwt = JWTManager(app)
swagger = Swagger(app)
# end-points com interface

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login", methods=["GET"])
def user_login():
    return render_template("login.html")

@app.route("/register", methods=["GET"])
def user_register():
    return render_template("register.html")

@app.route("/playlist", methods=["GET"])
@jwt_required
def content():
    all_posts = http_request.get("http://localhost:5000/posts")
    print(all_posts)
    return render_template("playlist.html", all_posts=all_posts)

@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")

# Gerar token JWT(auth), logins, register, etc

@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # Query your database for username and password
    user = User.query.filter_by(name=username, password=password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    # Verifica os dados enviados não estão nulos
    if username is None or password is None:
        # the user was not found on the database
        return render_template("error.html", message="Bad username or password")
    # faz uma chamada para a criação do token
    token_data = http_request.post("http://localhost:5000/token", json={"username": username, "password": password})
    if token_data.status_code != 200:
        return render_template("error.html", message="Bad username or password")
    # recupera o token
    all_posts = http_request.get("http://localhost:5000/posts")
    response = make_response(render_template("playlist.html",  all_posts=json.loads(all_posts.content.decode("utf-8"))))
    set_access_cookies(response, token_data.json()['token'])
    return response

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    if username is None or password is None:
        # the user was not found on the database
        return render_template("error.html", message="Bad username or password")
    http_request.post("http://localhost:5000/users", json={"username": username, "password": password})
    response = make_response(render_template("login.html"))
    return response


# endpoints para manuseio com a interface

@app.route("/content", methods=["POST"])
def content_add():
    post_name = request.form.get("post_name", None)
    post_content = request.form.get("post_content", None)
    if post_name is None or post_content is None:
        # the user was not found on the database
        return render_template("error.html", message="Bad Post name or content")
    http_request.post("http://localhost:5000/posts", json={"post_name": post_name, "post_content": post_content})
    all_posts = http_request.get("http://localhost:5000/posts")
    response = make_response(render_template("playlist.html",  all_posts=json.loads(all_posts.content.decode("utf-8"))))
    return response

@app.route("/edit_content", methods=["POST"])
def content_edit():
    post_id = request.form.get("post_id")
    post_name = request.form.get("post_name", None)
    post_content = request.form.get("post_content", None)
    if post_id is None or post_name is None or post_content is None:
        # the user was not found on the database
        return render_template("error.html", message="Bad Post ID, name or content")
    http_request.put(f"http://localhost:5000/posts/{post_id}", json={"post_name": post_name, "post_content": post_content})
    all_posts = http_request.get("http://localhost:5000/posts")
    response = make_response(render_template("playlist.html",  all_posts=json.loads(all_posts.content.decode("utf-8"))))
    return response

@app.route("/delete_content", methods=["POST"])
def content_delete():
    post_id = request.form.get("post_id")
    post_name = request.form.get("post_name", None)
    post_content = request.form.get("post_content", None)
    if post_id is None or post_name is None or post_content is None:
        # the user was not found on the database
        return render_template("error.html", message="Bad Post ID, name or content")
    http_request.delete(f"http://localhost:5000/posts/{post_id}")
    all_posts = http_request.get("http://localhost:5000/posts")
    response = make_response(render_template("playlist.html",  all_posts=json.loads(all_posts.content.decode("utf-8"))))
    return response


# CRUD posts API

@app.route("/posts", methods=["GET"])
def get_all_posts():
    posts = ToDoList.query.all()
    return_posts = []
    for post in posts:
        return_posts.append(post.serialize())
    return jsonify(return_posts)

@app.route("/posts/<int:id>", methods=["GET"])
def get_post_by_id(id):
    post = ToDoList.query.get(id)
    return jsonify(post.serialize())

@app.route("/posts/<int:id>", methods=["PUT"])
def update_post_by_id(id):
    data = request.json
    post = ToDoList.query.get(id)
    post.post_name = data["post_name"]
    post.post_content = data["post_content"]
    db.session.commit()
    return jsonify(post.serialize())

@app.route("/posts/<int:id>", methods=["DELETE"])
def delete_post_by_id(id):
    post = ToDoList.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify(post.serialize())

@app.route("/posts", methods=["POST"])
def create_post():
    data = request.json
    post = ToDoList(post_name=data["post_name"], post_content=data["post_content"])
    db.session.add(post)
    db.session.commit()
    return jsonify(post.serialize())


# CRUD users
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return_users = []
    for user in users:
        return_users.append(user.serialize())
    return jsonify(return_users)

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    return jsonify(user.serialize())

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(name=data["username"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    user.name = data["username"]
    user.password = data["password"]
    db.session.commit()
    return jsonify(user.serialize())

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user.serialize())

if __name__ == "__main__":
	app.run(debug=True)