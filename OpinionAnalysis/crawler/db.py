#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import MySQLdb
from . import logger


class MysqlDB(object):


    def __init__(self,host='localhost',port=3306,user='root',passwd='root',db='test',table='opinions'):
        self.logger = logger.get('opinion.db.MysqlDB')
        self.table = table
        try:
            self.conn = MySQLdb.connect(host,user,passwd,db,port)
        except Exception,e:
            self.logger.error('连接MYSQL数据库出错！%s' % e )
            self.conn = None


    def add(self,items):
        if len(items) == 0:
            self.logger.debug('没有数据写入MYSQL')
            return False
        if self.conn is None:
            return False


        #可以考虑多线程写入
        for m in items :
            self.insert(m)

        self.conn.close()


    def insert(self,m):
        try:
            cur=self.conn.cursor()
            cur.execute(
                'insert into '+self.table+'(prob,sentiment,title,link,summary,type,source,author,pub_date,json_data) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                ( m['prob'],m['sentiment'],m['title'],
                 m['link'],m['summary'],m['type'],
                 m['source'],m['author'],m['pub_date'],
                 json.dumps(m['json_data'])
            ))

            #插入的sql  id
            last_insert_id =int(cur.lastrowid)
            self.conn.commit()
            cur.close()
            if last_insert_id >0:
                data_info ={}
                data_info['opinion_id'] = last_insert_id
                data_info['question'] = m['title']
                data_info['ext'] = json.dumps({'source':m['source'],'type':m['type'],'prob':m['prob'],'sentiment':m['sentiment']})
                self.insert_ticket( data_info)
                self.logger.debug("成功写入 %s " % m['unique_identify'])
            else:
                self.logger.debug("写入失败 %s " % m['unique_identify'])
        except MySQLdb.Error,e:
            self.logger.error("Mysql出错！错误代码%d: 原因：%s json:%s" % (e.args[0], e.args[1],json.dumps(m)))
        except Exception,e:
            self.logger.error("写入数据库出错！%s 数据 %s " % (e,json.dumps(m)))

    #将数据插入到ticket表中
    def insert_ticket(self,data_info):
        try:
            cur=self.conn.cursor()
            cur.execute(
                'insert into t_kefu_ticket(ticket_type,fk_opinion_id,status,comment,question,ext,server_id)values(%s,%s,%s,%s,%s,%s,%s)',
                ( 1008,data_info['opinion_id'],0,'系统创建舆情分析工单',data_info['question'],data_info['ext'],1)
            )
            last_insert_id = int(cur.lastrowid)
            self.conn.commit()
            cur.close()
            if last_insert_id >0:
                self.logger.debug("成功写入t_kefu_ticket %s " % data_info['opinion_id'])
            else:
                self.logger.debug("失败写入t_kefu_ticket %s " % data_info['opinion_id'])
        except MySQLdb.Error,e:
            self.logger.error("Mysql出错！错误代码%d: 原因：%s json:%s" % (e.args[0], e.args[1],json.dumps(data_info)))
        except Exception,e:
            self.logger.error("写入t_kefu_ticket数据库出错！%s 数据 %s " % (e,json.dumps(data_info)))
