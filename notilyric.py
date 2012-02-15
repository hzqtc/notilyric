#! /usr/bin/env python2

import re
import thread
import urllib2
import urllib
import pynotify
from  xml.dom import minidom

class Lyric(object):
	def __init__(self):
		self.lines = {}
		self.linere = re.compile('\[([0-9]+:[0-9]+\.?[0-9]*)\]')

	def parseTimestamp(self, timestamp):
		s = timestamp.split(':')
		minute = int(s[0])
		second = int(s[1].split('.')[0])
		return minute * 60 + second

	def clear(self):
		self.lines = {}

	def load(self, fp):
		self.loads(fp.read())

	def loads(self, s):
		for line in s.split('\n'):
			res = self.linere.match(line)
			if res:
				timestamps = res.groups()
				content = line[line.rfind(']') + 1:].strip()
				if content:
					for timestamp in timestamps:
						time = self.parseTimestamp(timestamp)
						self.lines[time] = content

	def getline(self, time):
		if not self.lines:
			return ''

		maxkey = 0
		for key in self.lines:
			if key <= time and key > maxkey:
				maxkey = key

		if maxkey in self.lines:
			return self.lines[maxkey]
		else:
			return ''

class QQLyric(object):
	def search(self, artist, title):
		title = title.decode('utf-8').encode('gbk')
		artist = artist.decode('utf-8').encode('gbk')
		params = {'name': title, 'singer': artist, 'from': 'qqplayer'}
		searchURL = 'http://qqmusic.qq.com/fcgi-bin/qm_getLyricId.fcg?%s' % urllib.urlencode(params)
		try:
			searchXML = self._conxmlenc(urllib2.urlopen(searchURL).read())
		except:
			return None

		searchXMLDoc = minidom.parseString(searchXML)
		songInfoNodes = searchXMLDoc.getElementsByTagName('songinfo')
		if songInfoNodes.length == 0:
			return None

		lyricId = int(songInfoNodes[0].attributes['id'].value)
		lyricURL = 'http://music.qq.com/miniportal/static/lyric/%d/%d.xml' % (lyricId % 100, lyricId)
		return self._fetch(lyricURL)

	def _fetch(self, url):
		try:
			lyricXML = self._conxmlenc(urllib2.urlopen(url).read())
		except:
			return None

		lyricXMLDoc = minidom.parseString(lyricXML)
		try:
			lyricContent = lyricXMLDoc.getElementsByTagName('lyric')[0].firstChild.data
			return lyricContent
		except:
			return ''
	
	def _conxmlenc(self, xml):
		xml = xml.decode('gbk').encode('utf-8')
		return xml.replace('gb2312', 'utf-8')

class NotiLyric(object):
	def __init__(self, app = 'notilyric'):
		self.searchengine = QQLyric()
		self.lyric = Lyric()

		self.artist = self.title = ''
		self.notification = pynotify.Notification('', '')

		self.download_lock = thread.allocate_lock()

		pynotify.init(app)

	def setinfo(self, artist, title, cover = ''):
		self.artist = artist
		self.title = title
		thread.start_new_thread(self._download, ())

	def _download(self):
		self.download_lock.acquire()

		self.lyric.clear()
		self.notification.update("%s - %s" % (self.artist, self.title), 'Lyric downloading...')
		self.notification.show()
		lyricContent = self.searchengine.search(self.artist, self.title)
		if lyricContent:
			self.lyric.loads(lyricContent)
			self.notification.update("%s - %s" % (self.artist, self.title), 'Lyric downloaded!')
			self.notification.show()
		else:
			self.notification.update("%s - %s" % (self.artist, self.title), 'Lyric not found!')
			self.notification.show()

		self.download_lock.release()

	def close(self):
		self.notification.close()

	def display(self, progress):
		lyricLine = self.lyric.getline(progress)
		if lyricLine:
			self.notification.update("%s - %s" % (self.artist, self.title), lyricLine)
			self.notification.show()

