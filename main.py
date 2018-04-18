import pydocumentdb
import pydocumentdb.document_client as document_client
from flask import Flask, render_template, request, jsonify
import dbcsms

app = Flask(__name__)

@app.route('/')
def hello_world():
    name = '誰なんだか'
    return render_template('hello.html', title='Flask test', name=name)

@app.route('/api/<sorg>/<brand>/<contactid>', methods=['GET'])
def getContact(sorg, brand, contactid):

    query = {
      'query': 'SELECT * FROM entries e WHERE e.id = "{0}" and e.orgid = "{1}" and e.brandid = "{2}"'.format(contactid, sorg, brand)
    }

    options = {} 
    options['enableCrossPartitionQuery'] = True
    options['maxItemCount'] = 2

    db = dbcsms.DbCsms()
    res = db.query(query, options)

    return jsonify(res)

@app.route('/api/<sorg>/<brand>/<page>/<pageline>', methods=['GET'])
def getContactList(sorg, brand, page, pageline):
    sql = 'SELECT * FROM entries e WHERE e.orgid = "{0}" and e.brandid = "{1}" order by e.orderno'.format(sorg, brand)
    options = {
        'enableCrossPartitionQuery': True,
        'maxItemCount': 3
    }

    db = dbcsms.DbCsms()
    res = db.execute('getPagingList', [sql, options, pageline, page])

    return jsonify(res)

if __name__ == '__main__':
    app.run()
