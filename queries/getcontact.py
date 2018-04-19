'''
Create query for 1 contact data
'''
import os

class GetContact():
    """連絡先情報1件取得"""
    sql = ''

    # コンストラクタ
    def __init__(self):
        # クラス変数処理
        if GetContact.sql == '':
            selfpath = os.path.dirname(os.path.abspath(__file__))
            f = open(selfpath + '/getcontact.sql')
            GetContact.sql = f.read()
            f.close()

        # クエリーの設定
        self.query = {'query': '', 'parameters':[]}

        # オプションの設定
        self.options = {'enableCrossPartitionQuery': True, 'maxItemCount': 1}

    # クエリ作成
    def createQuery(self, sorg, brand, contactid):
        self.query['parameters'].append({'name': '@cid', 'value': contactid})
        self.query['parameters'].append({'name': '@orgid', 'value': sorg})
        self.query['parameters'].append({'name': '@brandid', 'value': brand})
        self.query['query'] = GetContact.sql
        return {'query': self.query, 'options': self.options}

if __name__ == '__main__':
    gc = GetContact()
    res = gc.createQuery('SA21', '01', 1)
    print(res)
    print(type(res))
