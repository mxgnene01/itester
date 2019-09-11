#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Meng xiangguo <mxgnene01@gmail.com>
#
#        H A P P Y    H A C K I N G !
#              _____               ______
#     ____====  ]OO|_n_n__][.      |    |]
#    [________]_|__|________)<     |MENG|
#     oo    oo  'oo OOOO-| oo\_   ~o~~~o~'
# +--+--+--+--+--+--+--+--+--+--+--+--+--+
#                        17/6/13  下午5:25

import os
import sys
import glob
import xlrd
import logging

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] - %(process)d - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s')

def fromExcelGetAllCase(fname, method='GET'):
    logging.debug('from %s get all case' % fname)
    bk = xlrd.open_workbook(fname)
    try:
        sh = bk.sheet_by_index(0)
    except:
        logging.error("no sheet in %s named Sheet1" % fname)

    return [tuple(sh.row_values(i)) for i in range(2, sh.nrows) if sh.cell_value(i, 3).upper() == method and sh.cell_value(i, 2).upper() == 'Y']


def testLoader(path, pattern="test_*.xlsx"):
    os.chdir(path)
    return glob.glob(pattern)

def findAllFile(path):
    all_case = []
    for casefile in testLoader(path):
        # 多个case文件进行case 合并
        all_case = all_case + fromExcelGetAllCase(casefile, 'GET') + fromExcelGetAllCase(casefile, 'POST')
    return all_case


def cmp_dict(src_data, dst_data, path='', diff=list()):
    if isinstance(src_data, dict):
        for key in src_data:
            newpath = path + '.' + key
            if key in dst_data:
                diff = cmp_dict(src_data[key], dst_data[key], newpath, diff)
            else:
                diff[newpath] = [src_data.get(key), 'not exist is key']
    else:
        if src_data != dst_data:
            diff[path] = [src_data, dst_data]

    return diff


def prepareStrToDict(strname, ofs='\n'):
    '''
    固定格式的string 转化成 dict

    utoken: 10364121-18687-a133c50e-f3b1-4dd4-967d-b49f034916ae
    key1: values1
    :return {'utoken': '10364121-18687-a133c50e-f3b1-4dd4-967d-b49f034916ae','key1': 'values1'}
    '''
    r_dict = dict()
    if strname:
        for header in strname.split(ofs):
            h = header.split(":")
            r_dict[h[0].strip()] = h[1].strip()

    return r_dict


def prepareRequestsParam(param, ofs='&'):
    '''
    对 requests 的 post 参数进行格式化

    Usage:
        >>> param =  "id=123145&id=123133&aaa=bbb"
        >>> preparePostParam(param)
        (('id', '123145'), ('id', '123133'), ('aaa', 'bbb'))
        >>> param =""
        >>> preparePostParam(param)
        {}
    '''
    if param:
        return tuple([(i.split("=")[0], i.split("=")[1]) for i in param.split(ofs)])
    else:
        return {}

def sendmail(send_to, cc_to=list(), content='邮件内容', title='邮件标题', attachment='', sendconf=dict(), ishtml=False):
    '''
    发送短信工具类
    :param send_to: 收件人列表, 栗子如下：
                    RECEIVERS = ['mengxiangguo<mengxiangguo@daling.com>', '陈韬炼'<chentaolian@daling.com>]
    :param cc_to: 抄送人列表
    :param content: 发件内容
    :param title: 标题
    :param attachment: 附近路径
    :param sendconf: 发件人用户名和密码
    :param ishtml: 内容是否网页
    :return: None
    '''
    import smtplib
    from os.path import basename
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.utils import COMMASPACE, formatdate
    from socket import gethostname

    text = """ %s

[%s]
    """ % (content, gethostname())
    msg = MIMEMultipart()
    msg['From'] = 'npc@daling.com'
    msg['To'] = COMMASPACE.join(send_to)
    msg['Cc'] = COMMASPACE.join(cc_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = '%s' % title
    if not ishtml:
        msg.attach(MIMEText(text, 'plain', 'utf-8'))
    else:
        msg.attach(MIMEText(content, _subtype='html', _charset='utf-8'))

    if attachment:
        with open(attachment, "rb") as f:
            name = basename(attachment)
            part = MIMEApplication(f.read(), Name=name)
            part['Content-Disposition'] = 'attachment; filename="%s"' % name
            msg.attach(part)
    username = sendconf.get('username', 'npc@daling.com')
    password = sendconf.get('password', 'eayXG06H')
    smtp = smtplib.SMTP('smtp.exmail.qq.com')
    smtp.login(username, password)
    smtp.sendmail(username, send_to + cc_to, msg.as_string())
    smtp.close()


if __name__ == '__main__':
    xx = {"111": '11', "23456": {"22222": 99949, "33333": "0000", "list": ["3333", "4444", "11"]}}
    yy = {"111": '11', "23456": {"22222": 9999, "33333": "0000", "list": ["3333", "4444", "11"]}, 'key': "values"}
    print(cmp_dict(xx, yy))