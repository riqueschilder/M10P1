from sqlalchemy import Column, Integer, String
from database.database import db

class User(db.Model):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50), nullable=False)
  password = Column(String(26), nullable=False)

  def __repr__(self):
    return f'<User:[id:{self.id}, name:{self.name}, password:{self.password}]>'
  
  def serialize(self):
    return {
      "id": self.id,
      "name": self.name,
      "password": self.password}
  
class ToDoList(db.Model):
  __tablename__ = 'posts'

  id = Column(Integer, primary_key=True, autoincrement=True)
  post_name = Column(String(50), nullable=False)
  post_content = Column(String(300), nullable=False)

  def __repr__(self):
    return f'<ToDoList:[id:{self.id}, post_name:{self.post_name}, post_content:{self.post_content}]>'
  
  def serialize(self):
    return {
      "id": self.id,
      "post_name": self.post_name,
      "post_content": self.post_content
      }