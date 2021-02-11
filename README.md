### Deluge Execute plugin script example

#### How to get the plugin working:
    * path to the script: just the path without `python` command and any input arguments
        /opt/PyCharmProjects/DelugeExecute/execute_script.py
    * chown user:group to `deluge`
    * chmod 755
    * no need to restart deluge [at least in my case]
    * supports all three events. Try to test with Add event.
    * https://github.com/SHi-ON/DelugeExecute
    * see the [RHEL, CentOS] system log at `sudo tail -f /var/log/messages`
