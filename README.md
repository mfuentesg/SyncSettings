Sync Settings
===============

**Sync Settings**, is a way of keeping the [Sublime Text](http://sublimetext.com/) configuration synchronized between different operating systems, the synchronization to uses Github Gist allowing you to use all the technologies that this service provides for example to see the history of your configuration file.

##Support

* Working on Windows, Linux and OSX
* Working on [Sublime Text 2](http://sublimetext.com/2), [Sublime Text 3](http://sublimetext.com/3)

##Installation:

1. Install [Package Control](https://packagecontrol.io/installation)
2. Open Package Control and looks for [Sync Settings](https://packagecontrol.io/packages/Sync%20Settings)

##Configuration

1. Creates an access [token in GitHub](https://github.com/settings/tokens)
2. Paste this code into the plugin configuration file

```Preferences > Packages Settings > Sync Settings > Settings - User```

####Options

* **access_token**: Refers to the access provided by GitHub token
* **gist_id**: Identifies to the id of the gist that is to be used for synchronization
* **excluded_files**: Are the files that are to be ignored at the time of synchronization, by default files that contain information with your editor license is found in this list.

##Commands

1. **Create and Upload**: Creates a new gist and upload your settings after uploaded a message asking if you wish to set the id of the gist in the plugin configuration is displayed. If you accept the gist id appears on 
`Preferences > Packages Settings > Sync Settings > Settings - User`.
2. **Upload**: Upload your settings files, excluding the files included in "excluded files" option.
3. **Download**: Download your settings files, overwriting the existing files, after downloaded your files  [Sublime Text](http://www.sublimetext.com) need to be restarted.
4. **Show Logs**: Open the log file in the active window.

##Tests

You can run and add new tests using the following instructions. For more information consulting the [framework documentation](https://docs.python.org/3/library/unittest.html#module-unittest).

###Requirements
For running the tests, you need install `requests` package, `pip install requests` and python 3.4+.

###Configuration
1. Rename `/path/to/plugin/tests/options.sample.json` to `/path/to/plugin/tests/options.json`
2. Set `access_token` to start the testing process

###Run tests

```bash
cd /path/to/plugin
python -m unittest discover -s ./tests

#For run an specific test just execute the following command
python -m unittest discover -s ./tests -p <test_name>.py
```

###Add Tests

```bash
cd /path/to/plugin/tests
touch test_<name>.py #Create a new file
```

```python
#Example:

from unittest import TestCase

class TestExample(TestCase):
  def test_upper(self):
    self.assertEqual('foo'.upper(), 'FOO')

  def test_<name>(self):
    self.assertEqual('bar'.lower(), 'BAR')
```

##Errors

If you find errors in the plugin, you can to execute "Show Logs" command and report a new [issue](https://github.com/mfuentesg/SyncSettings/issues/new) with the file content.

##Changelog
You can check the changes to this plugin [here](CHANGELOG.md)

##Donate
You are welcome support this project using [Paypal](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=7XCNSKK5W7DKJ)
