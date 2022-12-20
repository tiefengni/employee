from flask import Flask, render_template, jsonify
from flask import request
import sqlite3
import json
import os

# setting static path
template_dir = os.getcwd() + '/frontend/dist/'

# init flask framework
app = Flask(
    __name__, template_folder=template_dir,
    static_folder=template_dir, static_url_path="")

# index page
# display the template of index.html


@app.route("/")
def index_page():
    return render_template("./index.html")

# show all employee
# using sqlite database
# request for post method


@app.route("/list", methods=['POST'])
def list():
    conn = sqlite3.connect('./data.db')
    c = conn.cursor()
    cursor = c.execute("select id as key, name, sex, age, job from t_employee")
    employeeArr = []
    for row in cursor:
        employeeArr.append(
            {'key': row[0], 'name': row[1], 'sex': row[2], 'age': row[3], 'job': row[4]})
    return jsonify(employeeArr)

# add employee
# using sqlite database
# request for post method


@app.route("/add", methods=['POST'])
def add():
    conn = sqlite3.connect('./data.db')
    print('open database success!')
    c = conn.cursor()
    # insert employee sql, get values from post data
    sql = 'insert into t_employee (name, sex, age, job) values ("' + \
        request.form['name'] + '",' + request.form['sex'] + ',' + \
        request.form['age'] + ',"'+request.form['job']+'")'
    c.execute(sql)
    conn.commit()
    conn.close()
    json_data = request.form['name']
    return jsonify({'code': 1})


# delete employee
# using sqlite database
# request for post method

@app.route("/delete", methods=['POST'])
def delete():
    conn = sqlite3.connect('./data.db')
    print('open database success!')
    # delete employee sql,get id by post data
    sql = 'delete from t_employee where id = ' + request.form["id"]
    conn.execute(sql)
    conn.commit()
    conn.close()
    return jsonify({'code': 1})


if __name__ == '__main__':
    app.run()
