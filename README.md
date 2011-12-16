# NotiLyric

NotiLyric is a python lyric library. It's very easy for applications to use.

NotiLyric can download lyrics from the internet (QQMusic is the only providor now) and display current line using a bubble notification.

See the screenshot at: http://johnny-huang.appspot.com/use-notify-system-to-display-lyric

Based on NotiLyric, there comes "FMLyric" and "QLyric".

## FMLyric

Display lyric for [FMD](https://github.com/hzqtc/fmd).

	python2 fmlyric.py [options]

Options: -a for FMD address, -p for FMD port.

## QLyric

QLyric is a lyric plugin for [QuodLibet](http://code.google.com/p/quodlibet/).

First copy necessary files to QuodLibet plugin directory.

	cp qlyric.py notilyric.py ~/.quodlibet/plugins/events/

Start QuodLibet and enable QLyric plugin. You will see a bubble notification on screen displaying lyrics.

## Depends

Python2 of course, and `python-notify` in addition.

