Simple helper to run telegram-cli as daemon.
Once daemon is running you can connect a socket or:

telnet 127.0.0.1 2391

Then you can send telegram-cli command through socket.

Everything is just hardcoded, so tcp port 2391 was chosen. Lot of thing to add, to be defensive. Needed to change to unprivileged user. 
So, now, DON'T start daemon as root. USE an unpriveleged user.

Sorry, there's no even Makefile yet. Do gcc telegramclid.c -o telegramclid.

Within telegram-minion directory there is a set of python scripts which 'automates' a kind of conversation and reacts to master's commands.
