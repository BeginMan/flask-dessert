# coding=utf-8
"""
flask-restful api V2, 带认证的接口设计
需要安装Flask-HTTPAuth

ref:http://www.pythondoc.com/flask-restful/first.html
==========  ===============================================  =============================
HTTP 方法   URL                                              动作
==========  ===============================================  ==============================
GET         http://[hostname]/todo/api/v2.0/tasks            检索任务列表
GET         http://[hostname]/todo/api/v2.0/tasks/[task_id]  检索某个任务
POST        http://[hostname]/todo/api/v2.0/tasks            创建新任务
PUT         http://[hostname]/todo/api/v2.0/tasks/[task_id]  更新任务
DELETE      http://[hostname]/todo/api/v2.0/tasks/[task_id]  删除任务
==========  ================================================ =============================

    :copyright: (c) 2015 by fangpeng.
    :license: MIT, see LICENSE for more details.
"""
__date__ = '12/18/15'

from flask import Flask, jsonify, abort, make_response, request, url_for

# Flask-HTTPAuth
from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/todo/api/v2.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    """获取所有任务
        curl -i http://localhost:8000/todo/api/v2.0/tasks
        如果加了auth认证则
        curl -u beginman:pytho -i http://localhost:8000/todo/api/v2.0/tasks
    """
    # return jsonify({'tasks': tasks})
    return jsonify({'tasks': map(make_public_task, tasks)})


@app.route('/todo/api/v2.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """获取了指定任务"""
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task})


@app.route('/todo/api/v2.0/tasks', methods=['POST'])
def create_task():
    """
    创建任务
    $ curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:8000/todo/api/v2.0/tasks
    :arg
        JSON 格式
    :return
        把新添加的任务和状态 201 响应给客户端。
    """
    if not request.json or not 'title' in request.json:
        abort(400)          # 表示请求无效

    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route('/todo/api/v2.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    更新task
    $ curl -i -H "Content-Type: application/json" -X PUT -d '{"title":"JAVA"}' http://localhost:8000/todo/api/v2.0/tasks/2
    """
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)

    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


@app.route('/todo/api/v2.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """删除任务"""
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def make_public_task(task):
    """
    辅助函数，用户api返回Json数据的处理
    如/todo/api/v2.0/tasks 返回一堆数据，对于一些接口常更变的需求
    我们直接返回控制这些任务的完整的 URI，以便客户端可以随时使用这些 URIs

    return:
    [{
      "title": "Learn Python",
      "done": false,
      "description": "Need to find a good Python tutorial on the web",
      ++++++++++++++ "uri": "http://localhost:8000/todo/api/v2.0/tasks/2"
    }.........]
    """
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@auth.get_password
def get_password(username):
    """
    get_password 函数是一个回调函数，Flask-HTTPAuth 使用它来获取给定用户的密码。
    在一个更复杂的系统中，这个函数是需要检查一个用户数据库，但是在我们的例子中只有单一的用户因此没有必要。
    """
    if username == 'beginman':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    """
    error_handler 回调函数是用于给客户端发送未授权错误代码
    这里用403替代了403因为401在web端会弹出一个丑陋的登录框
    """
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


if __name__ == '__main__':
    app.run(port=8000, debug=True)