'''
Database access
'''
import pydocumentdb
import pydocumentdb.document_client as document_client
import json

class DbCsms:
    """ データベースアクセスクラス """

    # コンストラクタ
    def __init__(self):
        # dbcsms.jsonから接続情報読み込み
        f = open('dbcsms.json')
        self.config = json.load(f)
        f.close()

        # db&collectonのid
        self.database_id = 'dbs/' + self.config['DOCUMENTDB_DATABASE']
        self.collection_id = self.database_id + '/colls/' +self.config['DOCUMENTDB_COLLECTION']
        self.sproc_pref = self.collection_id + '/sprocs/'

        # 接続クライアント作成
        self.client = document_client.DocumentClient(self.config['ENDPOINT'], {'masterKey': self.config['MASTERKEY']})

        # 対象コレクション設定
        self.collection = self.client.ReadCollection(self.collection_id)

    # クエリー発行
    def query(self, query, options):
        result_iterable = self.client.QueryDocuments(self.collection_id, query, options)
        res = list(result_iterable)
        return res

    # ストアド実行
    def execute(self, sp, params):
        result_str = self.client.ExecuteStoredProcedure(self.sproc_pref + sp, params)
        res = json.loads(result_str)
        return res

if __name__ == '__main__':
    # クエリーテスト
    query = {
        'query': 'SELECT TOP @topno e.id, e.contactname FROM entries e WHERE e.orderno <= @prevkey ORDER BY e.orderno desc',
        'parameters':[
            {'name': '@topno', 'value': 3},
            {'name': '@prevkey', 'value': 3}
        ]
    }
    options = {
        'enableCrossPartitionQuery': True,
        'maxItemCount': 10
    } 
    db = DbCsms()
    res = db.query(query, options)
    res.reverse()
    print(res)

    # ストアドテスト
    res = db.execute('getPagingList', [
        'SELECT r.id, r.contactname FROM root r ORDER BY r.orderno',
        {
            'enableCrossPartitionQuery': True,
            'maxItemCount': 3
        },
        3,
        1
    ])
    print(res)
