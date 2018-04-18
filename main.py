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

if __name__ == '__main__':
    app.run()
