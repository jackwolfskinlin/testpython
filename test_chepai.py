#-*- coding: UTF-8 -*-
import json
#from mytest.lib.lib_import import *
from frame.lib.commonlib import asserts
from mytest.lib.http_driver import httpdriver
from mytest.control.plugin.mycase import MyCase
from mytest.control.env_global import EnvGlobal
import os
import random
#:/utf8
class Test_chepai(MyCase):
	def __init__(self):
		super(Test_chepai, self).__init__()
		self.host=EnvGlobal.chepai_ip
		self.port=EnvGlobal.chepai_port
		self.driver=httpdriver(self.host, self.port)

	def test_chepai_get(self):
#查询一个driverID接口"/get/?did="的测试
		dirname  = os.getcwd()+'/mytest/chepai/data.txt'
		filehandler= open(dirname, 'r')

		filehandler.seek(0)
		textlist = filehandler.readlines()
		for line in textlist:
			line = line.decode('utf-8-sig').strip()
			driverid, licenseName = line.split(',')
			license = {driverid: licenseName}
			myurl = "http://%s:%s/driverno/get/?did=%s" % (self.host, self.port, driverid)
			res = self.driver.HTTPGet(url=myurl)
			asserts.assert_equal(res['data'], license)

	def test_chepai_mget0(self):
# 查询多个driverID接口"/mget/?dids="的测试
		driverid1 = 12
		driverid2 = 13
		myurl = "http://%s:%s/driverno/mget/?dids=%d,%d" % (self.host, self.port, driverid1, driverid2)
		res = self.driver.HTTPGet(url=myurl)
		print "data in result is : %s"%res["data"]
		#asserts.assert_equal(res['data'], license)
		asserts.assert_equal(res['errno'],  0)


	def test_chepai_mget(self):
		dirname = os.getcwd() + '/mytest/chepai/data.txt'
		filehandler = open(dirname, 'r')


		dict = {}
		filehandler.seek(0)
		textlist = filehandler.readlines()
		for line in textlist:
			line = line.decode('utf-8-sig').strip()
			driverid, licenseName = line.split(',')
			#print "%s:%r"%("line : ",line)
			dict[driverid] = licenseName

		dictkeys = dict.keys()
		# dictkeys.sort()
		# dict = [dict[key] for key in dictkeys]
		#print dict
		dict_len =  len(dict)
		#print "dict_len is = %d, dictkeys[%d] = %r"%(dict_len, dict_len-1, dictkeys[0])
		did1 = dictkeys[random.randint(0,dict_len-1)]
		did2 = dictkeys[random.randint(0,dict_len-1)]
		#print "did1 = %r, did2 = %r"%(did1,did2)
		license = {did1:dict[did1], did2:dict[did2]}
		print "license is :%r"%license
		myurl = "http://%s:%s/driverno/mget/?dids=%s,%s" % (self.host, self.port, did1, did2)
		res = self.driver.HTTPGet(url=myurl)
		print "res[\"data\"] is %r"%res["data"]
		asserts.assert_equal(res['data'], license)

if __name__ == '__main__':
	mytestCase = Test_chepai()
	mytestCase.test_chepai_get()