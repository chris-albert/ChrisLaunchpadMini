# Chris Launchpad Mini MK3

This repo holds the MIDI remote script for ChrisLaunchPadMini, which is a custom MIDI script
for using the LaunchPad Mini as a Live performance tool. 

Helpful Links: 
 - [Live API](https://structure-void.com/PythonLiveAPI_documentation/Live10.0.1.xml)
 - [Forum Post](https://forum.ableton.com/viewtopic.php?f=1&t=200513&start=0)
 - [Launchpad Manual](https://fael-downloads-prod.focusrite.com/customer/prod/s3fs-public/downloads/Launchpad%20Mini%20-%20Programmers%20Reference%20Manual.pdf)

This directory must be placed in Ableton's MIDI remote scripts folder, located at: 
```
/Applications/Ableton Live 11 Suite.app/Contents/App-Resources/MIDI Remote Scripts/
```
for Ableton 11....

After placing this directoruy there you must run the python "compile" step below:
```
python -m compileall .
```

Logs for ableton are at: 
```
~/Library/Preferences/Ableton/Live\ 11.0.12/Log.txt
```

Helpfull command to tail just your logs 
```
tail -f ~/Library/Preferences/Ableton/Live\ 11.0.12/Log.txt | grep "RemoteScriptMessage: (ChrisLaunchpadMini)"
```

When making changes to the script, you must recompile and then relaunch Ableton.    