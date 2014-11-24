Telegram-minion is a set of python scripts that can be used to 'automate' actions throgh
telegram conversations.

ClientSockey.py	Class that provides socket communication with telegram-cli (this latter started
			as daemon by telegramclid or some other way).

MinionClass.py		A set of classes intended to 'react' to GRU's (master) commands. Anybody could extend the parent class defining custom actions.

minion-talk.py		This is the client, there conversation is defined, and which commands will be accepted.	Now there are only two: miniondo=getUptime which sends back the server uptime, and miniondo=getFortune which sends back a fortune cookie, as provided by fortune package (required).

Some more documentation will be added soon.

Processing files (Auto-Download pics or files):

This version includes auto-download feature.

If pic is received it will be downloaded to Telegram's default download directory.

Remember for this feature to work turning telegram's msg_num (msg number) is required. This can be done by telegram-cli's config file, this way:

cat ~/.telegram-cli/config
# This is an empty config file
# Feel free to put something here
msg_num = true;

Within minion-talk.py there's only a basic filtering. The following lines, use a regex to filter files with .txt :

	if re.search( r'^\[document.*\.txt.*', message.strip() ):
		#// some stuff
		pass

So, more is needed, filtering by mime/type... or some safer way. And remember: we're not filtering messages by sender (GRU).
If you need it remember to filter it.

Install procedure:
-----------------

1) Install telegram-cli you can get it from here: https://github.com/vysheng/tg
   Follow build and install procedure for the architecture you'll run the program.



Start procedure:
---------------

1) Start telegram-cli by using telegramclid (telegram-cli daemonizer).

2) Start minion-talk.py in foreground, or once you're ready in background:

	$ nohup /path/to/minion-talk.py &



How the minion works?
--------------------

Minion reacts from messages received from telegram. For instance, these actions are available:

miniondo=getUptime

	Will give you back the host's uptime.

miniondo=getFortune

	Will give you back a fortune cookie. This feature requires fortune program (just apt-get install fortune)

miniondo=getBAWeather

	Will give you back the current weather conditions for Buenos Aires area.

miniondo=sendspeech(@<peer> + Hi man, how are you doing?)

	Will send convert text to speech and send the audio to <peer>, where <peer> is a contact from your
	telegram contact_list. Here "Hi man, how are you doing?" was the text to be converted to speech.	



Disclaimer: this code is under GPL License, and is provided as it is. Use at your own risk.
----------

