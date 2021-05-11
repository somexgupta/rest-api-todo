from flask import Flask
from flask_restful import Resource, Api, reqparse,abort

todo_dic={
    1:{'task':'my task','summany':'my summary'},
    2:{'task':'my task 2','summany':'my summary2'}
}

task_post_arg = reqparse.RequestParser()
task_post_arg.add_argument("task",type=str,help="Task is required", required=True)
task_post_arg.add_argument("summany",type=str,help="Summary is required", required=True)
task_put_arg = reqparse.RequestParser()
task_put_arg.add_argument("task",type=str)
task_put_arg.add_argument("summany",type=str)

class Constant:
    param1="task"
    param2="summany"

class Todo(Resource):
    @marshal_with(resource_fields)
    def get(self,ids):
        return todo_dic[ids]
    
    def post(self,ids):
        args = task_post_arg.parse_args()
        if ids in todo_dic:
            abort(409,"Task Id already exist")
        todo_dic[ids] = {Constant.param1:args[Constant.param1],Constant.param2:args[Constant.param2]}
        return "Record Added successfully"
    
    @marshal_with(resource_fields)
    def put(self,ids):
        args = task_put_arg.parse_args()
        if ids not in todo_dic:
            abort(404,"Task Id doesn't exist")
        if args[Constant.param1]:
            todo_dic[ids][Constant.param1] = args[Constant.param1]
        if args[Constant.param2]:
            todo_dic[ids][Constant.param2] = args[Constant.param2]
        return todo_dic[ids]
    def delete(self,ids):
        if ids not in todo_dic:
            abort(404,"Task Id doesn't exist")
        del todo_dic[ids]
        return "Record deleted successfully"

class TodoList(Resource):
    def get(self):
        return todo_dic


api.add_resource(Todo,'/todos/<int:ids>')
api.add_resource(TodoList,'/todos')

if __name__ == '__main__':
    app.run(debug=True)