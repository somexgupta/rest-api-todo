from flask import Flask
from flask_restful import Resource, Api, reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqllite.db'
db = SQLAlchemy(app)

class ToDoModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(200))
    summary = db.Column(db.String(500))

# db.create_all()

resource_fields={
    'id':fields.Integer,
    'task':fields.String,
    'summary':fields.String
}

# todo_dic={
#     1:{'task':'my task','summary':'my summary'},
#     2:{'task':'my task 2','summary':'my summary2'}
# }

task_post_arg = reqparse.RequestParser()
task_post_arg.add_argument("task",type=str,help="Task is required", required=True)
task_post_arg.add_argument("summary",type=str,help="Summary is required", required=True)
task_put_arg = reqparse.RequestParser()
task_put_arg.add_argument("task",type=str)
task_put_arg.add_argument("summary",type=str)

class Constant:
    param1="task"
    param2="summary"

class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self,ids):
        task = ToDoModel.query.filter_by(id=ids).first()
        if not task:
            abort(404,message="Task Id Doesn't exist")
        return task
    
    @marshal_with(resource_fields)
    def post(self,ids):
        args = task_post_arg.parse_args()
        task = ToDoModel.query.filter_by(id=ids).first()
        if task:
            abort(409,message="Task Id exist")
        todo = ToDoModel(id=ids,task=args[Constant.param1],summary=args[Constant.param2])
        db.session.add(todo)
        db.session.commit()
        return todo,201
    
    @marshal_with(resource_fields)
    def put(self,ids):
        args = task_put_arg.parse_args()
        task = ToDoModel.query.filter_by(id=ids).first()
        if not task:
            abort(404,message="Task Id doesn't exist")
        if args[Constant.param1]:
            task.task = args[Constant.param1]
        if args[Constant.param2]:
            task.summary = args[Constant.param2]
        db.session.commit()
        return task,201
        
    def delete(self,ids):
        task = ToDoModel.query.filter_by(id=ids).first()
        if not task:
            abort(404,message="Task Id doesn't exist")
        db.session.delete(task)
        db.session.commit()
        return 204,"Task Deleted Successfully"

class TodoList(Resource):
    def get(self):
        tasks = ToDoModel.query.all()
        todos={}
        for task in tasks:
            todos[task.id]={"task":task.task,"summary":task.summary}
        return todos


api.add_resource(Todo,'/todos/<int:ids>')
api.add_resource(TodoList,'/todos')

if __name__ == '__main__':
    app.run(debug=True)