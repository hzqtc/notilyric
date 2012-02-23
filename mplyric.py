#! /usr/bin/env python2

import sys
import getopt
import time
import mpd

from notilyric import NotiLyric

class FMLyric(object):
	def __init__(self, addr, port):
		self.addr = addr
		self.port = port

		self.notilyric = NotiLyric('fmlyric')
		self.interval = 1

		self.artist = self.title = ''

	def run(self):
		self.client = mpd.MPDClient()
		try:
			self.client.connect(self.addr, self.port)
		except:
			print 'Connect to MPD failed. Is MPD running?'
			return

		while True:
			try:
				time.sleep(self.interval)
			except:
				print 'Quit.'
				self.client.disconnect()
				self.notilyric.close()
				break

			status = self.client.status()
			if status['state'] != 'play':
				self.notilyric.close()
				continue

			song = self.client.currentsong()
			artist = song['artist']
			title = song['title']
			progress = int(status['time'].split(':')[0])

			if self.artist != artist or self.title != title:
				self.artist = artist
				self.title = title
				self.notilyric.setinfo(artist, title)
			self.notilyric.display(progress)

if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], 'a:p:')
	addr = 'localhost'
	port = 6600

	for k,v in opts:
		if k == '-a':
			addr = v
		elif k == '-p':
			port = int(v)
	fmlyric = FMLyric(addr, port)

	fmlyric.run()

