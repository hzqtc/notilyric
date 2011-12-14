# NotiLyric

NotiLyric is a python lyric library. It's very easy for applications to use.

NotiLyric can download lyrics from the internet (QQMusic is the only providor now) and display current line using a bubble notification.

See the screenshot at: http://johnny-huang.appspot.com/use-notify-system-to-display-lyric

Based on NotiLyric, there come two utilities: "FMLyric" and "QLyric".

## FMLyric

Display lyric for [FMD](https://github.com/hzqtc/fmd).

	python2 fmlyric.py [options]

Options: -a for FMD address, -p for FMD port.

## QLyric

QLyric is a QuodLibet lyric plugin. To try it, just copy "qlyric.py" and "notilyric.py" to your QuodLibet plugin directory.

	cp qlyric.py notilyric.py .quodlibet/plugins/events/

Start QuodLibet and active QLyric plugin in plugins dialog. Then play some music and enjoy!

## Depends

Python2 of course, and `python-notify` in addition.

