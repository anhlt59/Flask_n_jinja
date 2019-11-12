from flask import Flask, session, escape, request, redirect, url_for, render_template, jsonify, send_from_directory
import control_DB as Data
from sys import path as syspath
import datetime
import os
import copy
syspath.insert(0, os.path.join(os.path.dirname(__file__), 'render'))
from Render import *

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(24)
UPLOAD_DIRECTORY = os.path.join(os.path.dirname(__file__),'render','scripts')


@app.route('/')
def dm():
    return redirect(url_for('home'))

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        use_L = Data.findUser(request.form['nameUser'].lower(), request.form['PassUser'])
        dt = {'name': request.form['nameUser'],
              'password': request.form['PassUser']
              }
        if use_L is None:
            return render_template("login.html", errors="loi roi", data=dt)
        else:
            session['User'] = use_L["_id"]
            session['partition'] = use_L["partition"]
            session['name'] = use_L["name"]
            return redirect(url_for('home'))
    return render_template("login.html", data="")

@app.route('/sign_out')
def sign_out():
    if 'User' in session:
        session.pop('User')
        return redirect(url_for('sign_in'))
    return redirect(url_for('sign_in'))

@app.route('/admin')
def admin():
    if 'User' in session:
        if escape(session['partition']) == "1":
            dt = {'User': escape(session['User']),
                  'partition': escape(session['partition']),
                  'name': escape(session['name']),
                  }
            all_use = list(Data.findUserAll())
            all_use2 = copy.deepcopy(all_use)
            for i in all_use2:
                i.pop('password')
                i.pop('Change')
            return render_template("admin.html", dt=dt, all_use=all_use , all_use2=all_use2)
    return redirect(url_for('sign_in'))

@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    if 'User' in session:
        if escape(session['partition']) == "1":
            dat = {
                "_id": request.json["_id"].lower(),
                "password": request.json["password"],
                "partition":request.json["partition"],
                "name": request.json["name"],
                "Description": request.json["Description"],
                "Phone" :  request.json["Phone"],
                "Status": "on",
                "Change":  datetime.datetime.now()
            }
            Data.insertUser(dat)
            return jsonify({'result': "success"})
        else:
            return "user can't edit"
    return "login pleasse"

@app.route('/edit_user_info', methods=['GET', 'POST'])
def edit_user_info():
    if 'User' in session:
        if escape(session['partition']) == "1":
            a = {"_id" : request.json["_id"]}
            try:
                Data.UpdateUser(a,request.json["data"])
                return jsonify({'result': "success"})
            except Exception as e:
                return jsonify({'result': str(e)})
        else:
            return "user can't edit"
    return "login pleasse"

@app.route('/reset_pass_user', methods=['GET', 'POST'])
def reset_pass_user():
    if 'User' in session:
        if  escape(session['partition']) == "1":
            ids = {"_id" : request.json["_id"]}
            ps =  {"password" : request.json["password"]}
            try:
                Data.UpdateUser(ids,ps)
                return jsonify({'result': "success"})
            except Exception as errs:
                return jsonify({'result': str(errs)})
    return "login pleasse"

@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    if 'User' in session:
        if  escape(session['partition']) == "1":
            try:
                Data.deleteUser(request.json["user"])
                return jsonify({'result': "success"})
            except Exception as errs:
                return jsonify({'result': str(errs)})
    return "login pleasse"

@app.route('/home')
def home():
    if 'User' in session:
       dt = {'User': escape(session['User']),
              'partition': int(escape(session['partition'])),
              'name': escape(session['name']),
              }
    
       ls = Data.serviceAll()
       return render_template("home.html", dt=dt, ls=ls)
    return redirect(url_for('sign_in'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'User' in session:
        if request.method == 'POST':
            dtb = {
                "_id": request.json["name"],
                "Description": request.json["Description"],
                'User': escape(session['User']),
                "update": datetime.datetime.now(),
                "script": request.json
            }
            inp = copy.deepcopy(dtb)
            try:
                Renders(inp["script"])
                Data.serviceUpdate(request.json["name"], dtb);
                return jsonify({'result': "success"})
            except Exception as e:
                return jsonify({'result': str(e)})
        dt = {'User': escape(session['User']),
              'partition': escape(session['partition']),
              'name': escape(session['name']),
              }
        ls = Data.serviceAll()
        ls_name = [];
        for i in ls:
            ls_name.append(i["_id"])
        return render_template("add.html", dt=dt, ls=ls_name)
    return redirect(url_for('sign_in'))

@app.route("/edit/<name>", methods=['GET', 'POST'])
def edit(name):
    if 'User' in session:
        dt = {'User': escape(session['User']),
              'partition': escape(session['partition']),
              'name': escape(session['name']),
              }
        if (Data.serviceByid(name) is not None):
            scrs = Data.serviceByid(name)
            scr = scrs["script"]
            Name = scrs["_id"]
            User = scrs["User"]
            Update = scrs["update"]
            Description = scr["Description"]
            snmp = scr["snmp"]
            option = scr["option"]
            oid = scr["oid"]
            vars = scr["vars"]
            OK = scr["OK"]
            WARNING = scr["WARNING"]
            CRITICAL = scr["CRITICAL"]
            UNKNOWN = scr["UNKNOWN"]
            return render_template("edit.html", dt=dt, Name=Name, User=User, Update=Update, Description=Description,
                                   snmp=snmp, oid=oid, vars=vars, option=option, OK=OK, UNKNOWN=UNKNOWN,
                                   WARNING=WARNING, CRITICAL=CRITICAL)
        else:
            return "Permission denied!"
    return redirect(url_for('sign_in'))

@app.route('/save', methods=['GET', 'POST'])
def save():
    if 'User' in session:
        if escape(session['partition']) == "1" or "2":
            dtb = {
                "Description": request.json["Description"],
                'User': escape(session['User']),
                "update": datetime.datetime.now(),
                "script": request.json
            }
            inp = copy.deepcopy(dtb)
            list(reversed(inp["script"]["vars"]))
            try:
                Renders(inp["script"])
                Data.serviceUpdate(request.json["name"], dtb);
                return jsonify({'result': "success"})
            except Exception as e:
                return jsonify({'result': str(e)})            
        else:
            return "user can't edit"
    return "login pleasse"

@app.route("/detail/download/<name>", methods=['GET'])
def download(name):
    path_file = path.join(UPLOAD_DIRECTORY, name+'.py')
    if os.path.isfile(path_file):
        return send_from_directory(UPLOAD_DIRECTORY, name + '.py', as_attachment=True)
    else:
        return jsonify({'result': 'File not found!'})


@app.route("/detail/save_file", methods=['POST'])
def save_file():
    if 'User' in session:
        if int(escape(session['partition'])) == 1:
            content = request.json['content']
            name = request.json['name']
            path_file = path.join(UPLOAD_DIRECTORY, name+'.py')
            with open(path_file, 'w') as file:
                file.write(content)
            return jsonify({'result': 'Save file success!'})
        else:
            return jsonify({'result': 'Permission denied!'})
    return redirect(url_for('sign_in'))

@app.route("/detail/<name>", methods=['GET', 'POST'])
def detail(name):
    if 'User' in session:
        dt = {'User': escape(session['User']),
              'partition': escape(session['partition']),
              'name': escape(session['name']),
              }
        if (Data.serviceByid(name) is not None):
            scrs = Data.serviceByid(name)
            scr = scrs["script"]
            Name = scrs["_id"]
            User = scrs["User"]
            Update = scrs["update"]
            Description = scr["Description"]
            with open(path.join(UPLOAD_DIRECTORY,name+'.py')) as file:
                detail = file.readlines()            
            return render_template("detail.html", dt=dt, Name=Name, User=User, Update=Update, Description=Description,
                                   detail=detail)
        else:
            return name
    return redirect(url_for('sign_in'))

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if 'User' in session:
        if int(escape(session['partition'])) <= 2:
            try:
                os.remove(os.path.join("render", "scripts", request.json['script'] + ".py"))
                try:
                    os.rmdir(os.path.join("render", "scripts", request.json['script']))
                except:
                    pass
                Data.serviceDelete(request.json['script'])
                return jsonify({'result': "success"})
            except Exception as errs:
                return jsonify({'result': str(errs)})
        else:
            return jsonify({'result': "partition"})
    return edirect(url_for('sign_in'))

@app.route('/run', methods=['GET', 'POST'])
def run_route():
    if 'User' in session:
        if int(escape(session['partition'])) <= 2:
            try:
                aa = run(request.json["script"],request.json["cond"])
                return jsonify({'result': str(aa)})
            except Exception as e:
                return jsonify({'result': str(e)})
        else:
            return jsonify({'result': "partition"})
    return edirect(url_for('sign_in'))

def Renders(script):
    Input = {
        'name': script["name"],
        'option': script["option"],
        'snmp': script["snmp"],
        'oid': script["oid"],
        'vars': script["vars"],
        'UNKNOWN': script["UNKNOWN"],
        'CRITICAL': script["CRITICAL"],
        'WARNING': script["WARNING"],
        'OK': script["OK"],
    }
    Render(Input).script()

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8080, passthrough_errors=True)