Telegram-minion is a set of python scripts that can be used to 'automate' actions throgh
telegram conversations.

ClientSockey.py	Class that provides socket communication with telegram-cli (this latter started
			as daemon by telegramclid or some other way).

MinionClass.py		A set of classes intended to 'react' to GRU's (master) commands. Anybody could extend the
				parent class defining custom actions.

minion-talk.py		This is the client, there conversation is defined, and which commands will be accepted.
				Now there are only two: miniondo=getUptime which sends back the server uptime, and
				miniondo=getFortune which sends back a fortune cookie, as provided by fortune package
				(required).

Some more documentation will be added soon.

