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
import glob
import xlrd
import logging

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] - %(process)d - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s')

def fromExcelGetAllCase(fname, method):
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


def assert_dict_str_contains(expect_data, real_data, path='', err_list=[]):
    ''' 两个dict ，list， sting 比对'''
    if isinstance(expect_data, (list, tuple)):
        for index, value in enumerate(expect_data):
            try:
                if not isinstance(value, (list, dict, tuple)):
                    # decode to unicode for diff
                    if isinstance(value, str):
                        value = value.decode('utf-8')

                    if value == real_data[index]:
                        continue
                    else:
                        err_list.append("%s.%s" % (path, str(index)))
                else:
                    err_list = assert_dict_str_contains(value, real_data[index], path + '.' + str(index), err_list)
            except Exception, e:
                logging.error(str(e))
    elif isinstance(expect_data, dict):
        for key, value in expect_data.items():
            try:
                if not isinstance(value, (list, dict, tuple)):
                    # decode to unicode for diff
                    if isinstance(value, str):
                        value = value.decode('utf-8')

                    if value == real_data[key]:
                        continue
                    else:
                        err_list.append("%s.%s" % (path, key))
                else:
                    err_list = assert_dict_str_contains(value, real_data[key], "%s.%s" % (path, key), err_list)
            except Exception, e:
                logging.error("dict compare error")
    else:
        if not expect_data == real_data:
            err_list.append("%s.%s" % (path, expect_data))

    return err_list


def prepareStrToDict(strname, ofs='\n'):
    '''
    固定格式的string 转化成 dict

    utoken: 10364121-18687-a133c50e-f3b1-4dd4-967d-b49f034916ae
    key1: values1

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
