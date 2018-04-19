'''
Create query for contact list
'''
import os

class GetContactList():
    """連絡先情報リスト取得"""
    sql = ''

    # コンストラクタ
    def __init__(self):
        # クラス変数処理
        if GetContactList.sql == '':
            selfpath = os.path.dirname(os.path.abspath(__file__))
            f = open(selfpath + '/getcontactlist.sql')
            GetContactList.sql = f.read()
            f.close()

        # クエリーの設定
        self.query = {'query': '', 'parameters':[]}

        # オプションの設定
        self.options = {'enableCrossPartitionQuery': True}

    # クエリ作成
    def createQuery(self, sorg, brand, sortitem, sortdir, contactname, activeflag):
        # SQLパラメータ作成
        self.query['parameters'].append({'name': '@orgid', 'value': sorg})
        self.query['parameters'].append({'name': '@brandid', 'value': brand})

        #
        wsql = GetContactList.sql
        if contactname == '':
            wsql = wsql.replace('/*@cond_contactname@*/', '')
        else:
            wsql = wsql.replace('/*@cond_contactname@*/', "and CONTAINS(e.contactname, '{0}') ".format(contactname))

        if activeflag < 0:
            wsql = wsql.replace('/*@cond_activeflag@*/', '')
        else:
            wstate = '{0}'.format(activeflag == 1)
            wsql = wsql.replace('/*@cond_activeflag@*/', "and e.activestate = {0} ".format(wstate.lower()))

        orderby = 'order by e.'
        if sortitem == '':
            orderby = orderby + 'orderno asc'
        else:
            if sortdir == '':
                orderby = orderby + '{0}'.format(sortitem) + ' asc'
            else:
                orderby = orderby + '{0} {1}'.format(sortitem, sortdir)

        wsql = wsql.replace('/*@order_by@*/', orderby)

        self.query['query'] = wsql
        return {'query': self.query, 'options': self.options}

if __name__ == '__main__':
    gc = GetContactList()
    res = gc.createQuery('SA21', '01', 'orderno', 'desc', '', 1)
    print(res)
    print(type(res))
