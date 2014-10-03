/***************************************************************************/
/* This is a simple fork procedure to help telegram-cli to run as daemon	*/
/* Author: retux												*/
/***************************************************************************/

#include <stdlib.h>
#include <stdio.h>
#include <syslog.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>

#define DAEMON_NAME "daemon_test"
#define SHELL "/bin/sh"
#define TELEGRAM "/usr/local/bin/telegram-cli -k /etc/telegram-cli/tg-server.pub -d -vvvv -E -R -D -C -P 2391"


/* Log priority (level) posibilidades:
 level
       This determines the importance of the message.  The levels are, in
       order of decreasing importance:

       LOG_EMERG      system is unusable
       LOG_ALERT      action must be taken immediately
       LOG_CRIT       critical conditions
       LOG_ERR        error conditions
       LOG_WARNING    warning conditions
       LOG_NOTICE     normal, but significant, condition
       LOG_INFO       informational message
       LOG_DEBUG      debug-level message

       The function setlogmask(3) can be used to restrict logging to
       specified levels only.

syslog function:

     Never pass a string with user-supplied data as a format, use the
       following instead:

           syslog(priority, "%s", string);
*/


int TelegramCliStart(void);
int execute(const char *command);

int main (int argc, char *argv[]) {

     	pid_t pid, sid;
	int exCode;

	setlogmask (LOG_UPTO (LOG_NOTICE));
	openlog ("telegramclid", LOG_CONS | LOG_PID | LOG_NDELAY, LOG_LOCAL1);

	// Fork the parent process
	pid = fork();
	if ( pid < 0 ) { exit(EXIT_FAILURE); }
	if ( pid == 0 )
		{
			// this is the child process
			do {
				exCode = TelegramCliStart();
				sleep(30);
			} while ( exCode == -1 || exCode == 0);
		}


	// some settings 
	// change file mask
    	umask(0);
     	//Create a new Signature Id for our child
     	sid = setsid();
     	if (sid < 0) { exit(EXIT_FAILURE); }
     	//Change Directory
     	//If we cant find the directory we exit with failure.
     	if ((chdir("/")) < 0) { exit(EXIT_FAILURE); }

	//Close Standard File Descriptors as this is a daemon
	close(STDIN_FILENO);
	close(STDOUT_FILENO);
	close(STDERR_FILENO);


    closelog();
    return(EXIT_SUCCESS);
}

int TelegramCliStart(void)
{
	int status;
	pid_t pid;
	syslog(LOG_NOTICE, "Will try to start telegram-cli.");
	// Fork the parent process
	pid = fork();
	if ( pid == 0 )
		{
			// this is the child process
			execl (SHELL, SHELL, "-c", TELEGRAM, NULL);
			//_exit (EXIT_FAILURE);
		} 
	else if ( pid < 0 )
	{
		syslog(LOG_ERR, "error couldn't open.");
		status = -1;
	}
	else
	{
		// this is the pearent, wait the child to return
		if (waitpid (pid, &status, 0) != pid)
		{
			status = -1;
		}
		else
		{
			status = 0;
			syslog(LOG_DEBUG, "Debug: fork end");
		}
	}
  return status;		
}
