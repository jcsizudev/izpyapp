'''
Database access
'''
import pydocumentdb
import pydocumentdb.document_client as document_client
import json

class DbCsms:
    def __init__(self):
        # dbcsms.jsonから接続情報読み込み
        f = open('dbcsms.json')
        self.config = json.load(f)
        f.close()
        print(self.config)
        print(self.config['ENDPOINT'])

        # db&collectonのid
        self.database_id = 'dbs/' + self.config['DOCUMENTDB_DATABASE']
        self.collection_id = self.database_id + '/colls/' +self.config['DOCUMENTDB_COLLECTION']
        print(self.collection_id)

        # 接続クライアント作成
        self.client = document_client.DocumentClient(self.config['ENDPOINT'], {'masterKey': self.config['MASTERKEY']})

        # 対象コレクション設定
        self.collection = self.client.ReadCollection(self.collection_id)

    def query(self, query, options):
        result_iterable = self.client.QueryDocuments(self.collection['_self'], query, options)
        res = list(result_iterable)
        return res

if __name__ == '__main__':
    query = {
        'query': 'SELECT TOP 10 * FROM entries e'
    }
    options = {
        'enableCrossPartitionQuery': True,
        'maxItemCount': 10
    } 
    db = DbCsms()
    res = db.query(query, options)
    print(res)
