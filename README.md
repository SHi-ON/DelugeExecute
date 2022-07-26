### Deluge Execute
Automated file transfer to a remote destination upon completion.
 
1. Set your config parameters according to `config_example.env`
2. Run `sentry.py` (you can edit and run `run.py`). 

#### Tips
- For any file transfer issues consult your system log files:
  - e.g. see the [RHEL, CentOS] system log at `sudo tail -f /var/log/messages`
- rsync without password:
  - generate key-gen for user __root__, not the current user!
