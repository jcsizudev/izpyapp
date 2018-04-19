import os
import pydocumentdb
import pydocumentdb.document_client as document_client
from flask import Flask, render_template, request, jsonify
import dbcsms
from queries.getcontact import GetContact
from queries.getcontactlist import GetContactList

app = Flask(__name__)

@app.route('/')
def hello_world():
    name = '誰なんだか'
    return render_template('hello.html', title='Flask test', name=name)

@app.route('/api/<sorg>/<brand>/<contactid>', methods=['GET'])
def getContact(sorg, brand, contactid):
    q = GetContact()
    query = q.createQuery(sorg, brand, contactid)
    db = dbcsms.DbCsms()
    res = db.query(query['query'], query['options'])
    return jsonify(res)

@app.route('/api/<sorg>/<brand>/<page>/<pageline>', methods=['GET'])
def getContactList(sorg, brand, page, pageline):
    # クエリパラメータ
    sortitem = request.args.get('sortitem', default='', type=str)
    sortdir = request.args.get('sortdir', default='', type=str)
    contactname = request.args.get('contactname', default='', type=str)
    activeflag = request.args.get('activeflag', default=-1, type=int)

    # クエリ作成
    q = GetContactList()
    query = q.createQuery(sorg, brand, sortitem, sortdir, contactname, activeflag)

    # クエリ実行
    db = dbcsms.DbCsms()
    res = db.execute('getPagingList', [query['query'], query['options'], int(pageline), int(page)])
    return jsonify(res)

if __name__ == '__main__':
    # ローカル環境の強制停止用にプロセスID出力
    if os.getenv('USERNAME') == 'izu_t':
        print('taskkill /pid {0} /F'.format(os.getpid()))

    # スタート
    app.run()
