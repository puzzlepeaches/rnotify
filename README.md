# rnotify

During operations, testers will often stand up arbitrary tooling to perform long running tasks. This is great, but sort of difficult to track in the real world. This project tries to solve that problem using some really simple code. The tool rnotify in its current form allows the user to send notifications to a Slack channel using webhook following the creation of afile. Very useful for tracking logfile creation by:

* Responder
* ntlmrelayx


# Install

Install with pipx for now using:

```
pipx install git+https://github.com/puzzlepeaches/rnotify.git
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


# Coming soon

- File change tracking to notify on logfile changes. 
- More notification providers (twilio, teams, discord)
- Better notification structure
- Publishing to PyPi
- Process monitoring to notify on exit of arbitrary tools
- More customization of the notfication message
