# rnotify

Notify Slack channel using webhook on creation of file. Very useful for tracking logfile creation by:

* Responder
* ntlmrelayx


# Install

Install with pipx for now using:

```
pipx install git+https://github.com/puzzlepeaches/msprobe.git
```


# Usage

Help menu below:

```
rn -h

Usage: rn [OPTIONS]

  Notify on new files in a directory

Options:
  -d, --directory TEXT  Directory to watch.
  -w, --webhook TEXT    Slack Webhook URL.
  -s, --sleep INTEGER   Sleep time between checks
  --config FILE         Read configuration from FILE.
  -h, --help            Show this message and exit.
```

Possible to call the utility with both `rnotify` and `rn`. The utility also allows you to specify a configuration file with `--config`.
