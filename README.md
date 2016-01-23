Sync Settings
===============

[![Build Status](https://travis-ci.org/mfuentesg/SyncSettings.svg?branch=master)](https://travis-ci.org/mfuentesg/SyncSettings)

**Sync Settings**, is a cross-platform solution to keep the [Sublime Text](http://sublimetext.com/) configuration updated.

##How works?

**Sync Settings** uses Github-Gist allowing you to use all features that this service provides.

##Support

* Working on Windows, Linux and OSX
* Working on [Sublime Text 2](http://sublimetext.com/2), [Sublime Text 3](http://sublimetext.com/3)

##Installation:

1. Install [Package Control](https://packagecontrol.io/installation)
2. Open Package Control and looks for [Sync Settings](https://packagecontrol.io/packages/Sync%20Settings)

##Configuration

1. Creates an access [token in GitHub](https://github.com/settings/tokens/new)
2. Paste token in configuration file `Preferences > Packages Settings > Sync Settings > Settings - User`

####Options

* **access_token**: Access token provided by GitHub
* **gist_id**: Identifier of the gist that will be used for the synchronization
* **excluded_files**: It is a list with all files that will be ignored by the plugin at the time of upload or download. You can exclude by folder name, file name and/or file extension.
```json
/**
 * Excluded files example:
 * Note: Considers that each excluded item will begin with /Path/to/Sublime Text/Packages/User/
 */

{
  "excluded_files": [
    ".txt",
    "SublimeLinter",
    "awesome_file.py",
    "path/to/other/awesome/file.py"
  ]
}
```
* **included_files**: It is a list with all files what will be included by the plugin at the time of upload or download. You can include by folder name, file name and/or file extension.
```json
/**
 * Included files example:
 * Note: Considers that each include item will begin with /Path/to/Sublime Text/Packages/User/
 */

{
  "included_files": [
    ".txt",
    "SublimeLinter/some_file.py",
    "awesome_file.py",
    "path/to/other/awesome/file.py"
  ]
}
```

##Commands

1. **Create and Upload**: Creates a new gist and upload your settings. The Gist identifier will be included in `Preferences > Packages Settings > Sync Settings > Settings - User` if you accept the prompt message. 
2. **Delete and Create**: Deletes the current gist and create a new with your settings.
3. **Upload**: Upload your settings files, excluding the files included in "excluded files" option.
4. **Download**: Download your settings files, overwriting the existing files, after downloaded your files [Sublime Text](http://www.sublimetext.com) need to be restarted.
5. **Delete**: Deletes the current gist.
6. **Show Logs**: Open a new view with the log file content.

##Tests

You can run and add new tests using the following instructions. For more information consulting the [framework documentation](https://docs.python.org/3/library/unittest.html#module-unittest).

###Requirements
For running the tests, you need install the dependencies `pip install -r requirements.txt` and python 2.7+. Also, it is necessary create an environment variable called `SYNC_ACCESS_TOKEN`.

###Run tests

```bash
# Linux/OSX
export SYNC_ACCESS_TOKEN="<YOUR_ACCESS_TOKEN>"

# Windows (Run as Administrator)
setx SYNC_ACCESS_TOKEN "<YOUR_ACCESS_TOKEN>" -m


#Run all tests
python -m unittest discover -s ./tests/libs

#For run an specific test just add the `p` flag
python -m unittest discover -s ./tests/libs -p test_<name>.py
```

###Add Tests

```bash
touch test_<name>.py #Create a new file
```

```python
#Example:

from unittest import TestCase

class TestExample(TestCase):
  def test_upper(self):
    self.assertEqual('foo'.upper(), 'FOO')

  def test_<name>(self):
    self.assertFalse('bar'.lower(), 'BAR')
```

##Errors

If you find errors in the plugin, you can to execute "Show Logs" command and report a new [issue](https://github.com/mfuentesg/SyncSettings/issues/new) with the file content.

##Changelog

You can check the changes to this plugin [here](CHANGELOG.md)

##Donate

You are welcome support this project using [Paypal](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=7XCNSKK5W7DKJ)
