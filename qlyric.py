#! /usr/bin/env python2

# QLyric: a lyric downloader and displayer for Quod Libet
# version 0.1
# (C) 2011 by Johnny Huang <hzqtc1229@gmail.com>
# Licenses under GPLv2. See Quod Libet's COPYING for more information

import thread
import time
from notilyric import NotiLyric
from quodlibet.plugins.events import EventPlugin
from quodlibet.player import playlist as player

class QLyric(EventPlugin):
	PLUGIN_ID = "QLyric"
	PLUGIN_NAME = "Quod Libet Lyric"
	PLUGIN_DESC = "A lyric downloader and displayer for Quod Libet"
	PLUGIN_VERSION = "0.1"

	def __init__(self):
		self.live = False
		self.notilyric = NotiLyric('QLyric')
		self.interval = 1

	def display(self):
		while self.live:
			time.sleep(self.interval)
			if player.paused:
				self.notilyric.hide()
				continue

			progress = int(player.get_position() // 1000)
			self.notilyric.display(progress)
		self.notilyric.close()

	def enabled(self):
		self.live = True
		thread.start_new_thread(self.display, ())
	
	def disabled(self):
		self.live = False
		self.notilyric.close()

	def plugin_on_song_started(self, song):
		self.notilyric.setinfo(song.get('artist'), song.get('title'))

