# NotiLyric

NotiLyric is a python lyric library. It's very easy for applications to use.

NotiLyric can download lyrics from the internet (QQMusic is the only providor now) and display current line using a bubble notification.

![NotiLyric](http://johnny-huang.appspot.com/file/notify-lyric.png)

Based on NotiLyric, I offer you the following lyric display programs and plugins.

## FMLyric

Display lyric for [FMD](https://github.com/hzqtc/fmd).

	python2 fmlyric.py [options]

Options: -a for FMD address (default localhost), -p for FMD port (defalt 10098).

## MPLyric

Display lyric for [MPD](http://mpd.wikia.com/).

	python2 mplyric.py [options]

Options: -a for MPD address (default localhost), -p for MPD port (defalt 6600).

## QLyric

QLyric is a lyric plugin for [QuodLibet](http://code.google.com/p/quodlibet/).

First copy necessary files to QuodLibet plugin directory.

	cp qlyric.py notilyric.py ~/.quodlibet/plugins/events/

Start QuodLibet and enable QLyric plugin. You will see a bubble notification on screen displaying lyrics.

## Depends

`python2` and `python-notify` are required, `python-mpd` is a must for MPLyric.
