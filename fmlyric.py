#! /usr/bin/env python2

import sys
import getopt
import socket
import time
import json

from notilyric import NotiLyric

class FMLyric(object):
	def __init__(self, addr = 'localhost', port = 10098):
		self.addr = addr
		self.port = port

		self.notilyric = NotiLyric('fmlyric')
		self.interval = 1

	def run(self):
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.conn.connect((socket.gethostbyname(self.addr), self.port))
		except:
			print 'Connect to FMD failed. Is FMD running?'
			return
		res = self.conn.recv(1024)	# receive welcome info

		while True:
			try:
				time.sleep(self.interval)
			except:
				print 'Quit.'
				self.conn.send('bye')
				self.conn.close()
				self.notilyric.close()
				break

			self.conn.send('info')
			obj = json.loads(self.conn.recv(4096))

			status = obj['status']
			if status == 'stopped':
				self.notilyric.hide()
				continue

			artist = obj['song']['artist'].encode('utf-8')
			title = obj['song']['title'].encode('utf-8')
			progress = obj['progress']

			self.notilyric.setinfo(artist, title)
			self.notilyric.display(progress)

if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], 'a:p:')
	if 'a' not in opts and 'p' not in opts:
		fmlyric = FMLyric()
	elif 'p' not in opts:
		fmlyric = FMLyric(opts['a'])
	else:
		fmlyric = FMLyric(opts['a'], opts['p'])

	fmlyric.run()

