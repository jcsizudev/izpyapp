import pydocumentdb
import pydocumentdb.document_client as document_client
from flask import Flask, render_template, request, jsonify

config = { 
    'ENDPOINT': 'https://izcsms.documents.azure.com:443/',
    'MASTERKEY': 'M5o1Lvfs5rne5c8fmAi7iqMaZ8GBKM882PjSP3VUWimDOILsFomC2SXAjKR48FRgjJ5j5MMewOjHeqxMocg52g==',
    'DOCUMENTDB_DATABASE': 'zax',
    'DOCUMENTDB_COLLECTION': 'entries'
}

# Initialize the Python DocumentDB client
client = document_client.DocumentClient(config['ENDPOINT'], {'masterKey': config['MASTERKEY']})

# Create a database
#db = client.CreateDatabase({ 'id': config['DOCUMENTDB_DATABASE'] })
database_link = 'dbs/' + config['DOCUMENTDB_DATABASE']
db = client.ReadDatabase(database_link)

# Create collection options
options = {
    'offerEnableRUPerMinuteThroughput': True,
    'offerVersion': "V2",
    'offerThroughput': 400
}

# Create a collection
collection_link = database_link + '/colls/{0}'.format(config['DOCUMENTDB_COLLECTION'])
collection = client.ReadCollection(collection_link, options)

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

  result_iterable = client.QueryDocuments(collection['_self'], query, options)
  res = list(result_iterable)

  #res = {'sorg': sorg, 'brand': brand, 'contactid': contactid}
  return jsonify(res)

if __name__ == '__main__':
  app.run()
