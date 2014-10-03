telegramclid - Solo un "daemonizador" para telegram-cli

telegram-cli es un soft grandioso, que permite usar los servicios de Telegram (https://telegram.org) desde 
la consola de un *nix (CLI) con una interfaz interactiva.
Lo bueno, es que incluye posibilidad de que telegram-cli reciba comandos desde un socket tcp/ip.

telegramclid aprovecha eso y lanza telegramd como daemon en background, escuchando conexiones en el puerto
2391 (por ahora "hardcoded").

Aplicaciones cliente pueden conectarse a ese puerto, e interactuar con telegram-cli.


1)	Procedimiento de instalación:

1.1)	Requisitos: 	telegram-cli (desde luego) y sus dependencias https://github.com/vysheng/tg/blob/master/README.md

			Standard C developer tools (gcc, normalmente build-essential package).

1.2)	Instalar telegram-cli:

	Clonar git y compilar como se describe en: https://github.com/vysheng/tg/blob/master/README.md

	Copiar binario bin/telegram-cli a /usr/local/bin, verificar permisos de ejecución.

	Copiar clave publica tg-server.key a /etc/telegram-cli/

1.3) Ejecutar telegram-cli en modo interactivo la primera vez, para hacer la activación.

1.4) Iniciar en modo daemon, por ahora solo ejecutar binario telegramclid, con el mismo usuario que se uso
	para la activación del telegram-cli.
	Opcional pero conveniente: agregar algunas opciones en la config de telegram-cli:

	$ cat /home/retux/.telegram-cli/config 
	# This is an empty config file
	# Feel free to put something here
	msg_num = true;

	
	En este caso para mostrar numero de mensajes.

1.5) Verificar si está corriendo:

	$ ps aux | grep telegr
	retux    1285  0.0  0.0   1832   392 pts/14   S    09:20   0:00 ./telegramclid
	retux    1746  0.0  0.0   1932   508 pts/14   S    09:22   0:00 /bin/sh -c /usr/local/bin/telegram-cli -k /etc/telegram-cli/tg-server.pub -d -vvvv -E -R -D -C -P 2391
	retux    1747  0.0  0.0 196456  1816 pts/14   S    09:22   0:00 /usr/local/bin/telegram-cli -k /etc/telegram-cli/tg-server.pub -d -vvvv -E -R -D -C -P 2391


	$ pstree `pidof telegramclid`
	telegramclid───sh───telegram-cli

	$ netstat -putona | grep 2391
	tcp        0      0 127.0.0.1:2391          0.0.0.0:*               LISTEN      1747/telegram-cli off (0.00/0/0)

1.6)	Conectar usando cliente, test con telnet o nc.

~$ telnet 127.0.0.1 2391
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
stats
ANSWER 97
users_allocated 10
chats_allocated 0
secret_chats_allocated  0
peer_num        10
messages_allocated      67


main_session
msg Matías_Retux Hello man! I'm alive.
ANSWER 53
598 [10:58]  Matías Retux <<< Hello man! I'm alive.




