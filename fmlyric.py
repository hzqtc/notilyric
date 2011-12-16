#! /usr/bin/env python2

import sys
import getopt
import socket
import time
import json
import urllib

from notilyric import NotiLyric

class FMLyric(object):
	def __init__(self, addr, port):
		self.addr = addr
		self.port = port

		self.notilyric = NotiLyric('fmlyric')
		self.interval = 1

		self.artist = self.title = ''

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

			try:
				self.conn.send('info')
				obj = json.loads(self.conn.recv(4096))
			except:
				print 'Server quit.'
				self.conn.close()
				self.notilyric.close()
				break

			status = obj['status']
			if status != 'playing':
				self.notilyric.hide()
				continue

			artist = obj['song']['artist'].encode('utf-8')
			title = obj['song']['title'].encode('utf-8')
			coverurl = obj['song']['cover']
			progress = obj['progress']

			if self.artist != artist or self.title != title:
				self.artist = artist
				self.title = title
				coverfile, header = urllib.urlretrieve(coverurl)
				self.notilyric.setinfo(artist, title, coverfile)
			self.notilyric.display(progress)

if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], 'a:p:')
	addr = 'localhost'
	port = 10098

	for k,v in opts:
		if k == '-a':
			addr = v
		elif k == '-p':
			port = int(v)
	fmlyric = FMLyric(addr, port)

	fmlyric.run()

