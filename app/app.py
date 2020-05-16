from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'homesData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Stats'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM homesStats ORDER BY sell')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, stats=result)


@app.route('/view/<int:home_id>', methods=['GET'])
def record_view(home_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM homesStats WHERE id=%s', home_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', bio=result[0])


@app.route('/edit/<int:home_id>', methods=['GET'])
def form_edit_get(home_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM homesStats WHERE id=%s', home_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Stats', bio=result[0])


@app.route('/edit/<int:home_id>', methods=['POST'])
def form_update_post(home_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('sell'), request.form.get('list'), request.form.get('living'),
                 request.form.get('rooms'), request.form.get('beds'), request.form.get('baths'),
                 request.form.get('age'), request.form.get('acres'),request.form.get('taxes'), home_id)
    sql_update_query = """UPDATE homesStats t SET t.sell = %s, t.list = %s, t.living = %s, t.rooms = 
    %s, t.beds = %s,  t.baths = %s,  t.age = %s,  t.acres = %s,  t.taxes = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/homes/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Homes Form')


@app.route('/homes/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('sell'), request.form.get('list'), request.form.get('living'),
                 request.form.get('rooms'), request.form.get('beds'), request.form.get('baths'),
                 request.form.get('age'),request.form.get('acres'),request.form.get('taxes'))
    sql_insert_query = """INSERT INTO homesStats (sell,list,living,rooms,beds,baths,age,acres,taxes) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:home_id>', methods=['POST'])
def form_delete_post(home_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM homesStats WHERE id = %s """
    cursor.execute(sql_delete_query, home_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/stats', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM homesStats')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/stats/<int:home_id>', methods=['GET'])
def api_retrieve(home_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM homesStats WHERE id=%s', home_id)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/stats', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (content['sell'], content['list'], content['living'], content['rooms'], content['beds'],
                 content['baths'],content['age'],content['acres'],content['taxes'])
    sql_insert_query = """INSERT INTO homesStats (sell,list,living,rooms,beds,baths,age,acres,taxes) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/stats/<int:home_id>', methods=['PUT'])
def api_edit(home_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['sell'], content['list'], content['living'], content['rooms'], content['beds'],
                 content['baths'],content['age'],content['acres'],content['taxes'], home_id)
    sql_update_query = """UPDATE homesStats t SET t.sell = %s, t.list = %s, t.living = %s, t.rooms = 
    %s, t.beds = %s, t.baths = %s, t.age = %s, t.acres = %s, t.taxes = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/stats/<int:home_id>', methods=['DELETE'])
def api_delete(home_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM homesStats WHERE id = %s """
    cursor.execute(sql_delete_query, bio_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)