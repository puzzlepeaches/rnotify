
# rnotify


### Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)

---

## About

Operators use several tools to perform internal security assessments. These tools can be difficult to track remotely and have output that is time sensitive. The tool rnotify tries to solve this problem. Some example use cases are listed below:

- Monitor hashcat process and notify when cracking job is completed 
- Monitor folder for hashes captured using Responder
- Monitor and notify on computer account creation when using mitm6 and ntlmrelayx
- Notify when password spraying job completes

Following a change to the monitoried object, the tool can then notify using a webhook for the following communication platforms:

* Slack
* MS Teams
* Discord

### Installation

The project can be installed using pipx: 

```
pipx install rnotify 
```

## Usage

The tool is only useable on Unix based operating systems. The utility can be called using the command `rnotify` or `rn` and can monitor:

* File changes
* New files added to a folder
* Process exit (PID)

```
Usage: rn [OPTIONS] COMMAND [ARGS]...

  Notify on arbitrary filesystem events and process state changes.

Options:
  --help  Show this message and exit.

Commands:
  file    Notify on file changes
  folder  Notify on directory changes
  pid     Notify on process changes
```

All modules require the specificiation of the following options:

* Webhook URL used for notifications
* Notification provider associated with the provided webhook
* Target to monitor (file, folder, pid)

All modules optionally allow the specification of the following options:

* Daemonization of the utility to run rnotify in the background
* Sleep interval used by tool when checking for changes
* Configuration file in the format shown below

```
webhook = 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'
target = '/tmp/screen.log'
notifier = 'slack'
create_daemon = 'True'
```

### File Monitoring

File changes can be monitored using the `file` subcommand:

```
Usage: rn file [OPTIONS] TARGET

  Notify on file changes

Options:
  -w, --webhook TEXT              Webhook URL  [required]
  -n, --notifier [teams|slack|discord]
                                  Notification provider.  [required]
  -f, --filter TEXT               Filter changes by string.
  -s, --sleep INTEGER             Sleep time between checks  [default: 5]
  -d, --daemon                    Daemonize the utility
  --config FILE                   Read configuration from FILE.
  -h, --help                      Show this message and exit.
 ```
 Changes to logfiles can be filtered using the `-f` flag.
 
### Folder Monitoring

Folder changes can be monitored using the `folder` subcommand:

```
Usage: rn folder [OPTIONS] TARGET

  Notify on directory changes

Options:
  -w, --webhook TEXT              Webhook URL  [required]
  -d, --daemon                    Daemonize the utility
  -n, --notifier [teams|slack|discord]
                                  Notification provider.  [required]
  -s, --sleep INTEGER             Sleep time between checks  [default: 5]
  --config FILE                   Read configuration from FILE.
  -h, --help                      Show this message and exit.
 ```
 
### PID Monitoring

Process exits can be monitored using the `pid` subcommand:
 
```
Usage: rn pid [OPTIONS] TARGET

  Notify on process changes

Options:
  -w, --webhook TEXT              Webhook URL  [required]
  -n, --notifier [teams|slack|discord]
                                  Notification provider.  [required]
  -s, --sleep INTEGER             Sleep time between checks  [default: 5]
  -d, --daemon                    Daemonize the utility
  --config FILE                   Read configuration from FILE.
  -h, --help                      Show this message and exit.
```

### Usage examples

Watch Responder logs folder in the foreground:

```
rn folder /opt/Responder/logs -w https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX -n slack
```

Watch for hashcat process to stop in the background:

```
rn pid 54782 -w https://hooks.teams.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX -n teams -d
```

Watch for changes to gnu screen log with a filter in the foreground:

```
rn file /top/screen.log -f Account -w https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX -n slack 
```

