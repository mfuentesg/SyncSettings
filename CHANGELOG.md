##1.0.1

This version has some bug fixes found

* When files do not exist
* Remove the file repeated in the list of excluded files
* Include Default <platform>.sublime-keymap files and the User Settings
* Include Changelog file

##1.1.0

* Now your operations and errors are saved
* New commands added
* Custom Exception Added
* Fix minor errors

##1.2.0

This version executes each command as a thread, allowing that the application is not lock.

* Added threading support

##2.0.0

This version has some bug fixes found and new features

* All files inside on User folder will be included
* Enhancements on the excluded files list
  - Exclude by filename
  - Exclude by extension
  - Exclude by folder
* Show progress indicator on the status bar
* Error messages more descriptive
* Minor bug fixes

##2.1.1

This version has some bug fixes

* Add base encoding to read the files
* When a file not exists in other host this file is not created
* Function enhancements

##2.2.0

This version has some bug fixes

* Code 422 - Validation Failed
* Re-order file structure
* Enhance testing

##2.2.1

This version has some bug fixes

* Restore base encoding to read the files
* Minor fixes

#2.2.2

* Add Support to Python 2.7

#2.2.4

* Add Delete and Create Command
* Add Delete Command
* Enhancement on Excluded files filter
* Refactoring
* Minor Fixes

#2.2.5

* Minor Fixes

#2.2.6

* included_files option was added
* Minor Fixes

#2.3.0

* Check if your settings are up to date on startup
* Add PopUp support to ST Build 3070 or higher
* Auto upgrade your Settings if the auto_upgrade option is enabled
* auto_upgrade option was added
* Minor Enhancements
* MIT license was added

#2.3.1

* Fix encoding bug
* Allow special chars like 'ç'

#2.4.0

- Rename cache file from `.sync_settings_cache` to `.sync-settings.cache` (~/.sync_settings_cache)
- New Command `Sync Settings: Edit User Settings` by @JohaWeber
- Bug Logging was improved

Issues:
- Remove SyncSettings references from download process (https://github.com/mfuentesg/SyncSettings/issues/50)
- Download doesn't work and clears Gist ID (https://github.com/mfuentesg/SyncSettings/issues/46)
- downloading append a newline in configfile (https://github.com/mfuentesg/SyncSettings/issues/45)
- sync_settings_cache links to wrong directory (https://github.com/mfuentesg/SyncSettings/issues/42)

#2.4.2

Solved issues:
- Fails with Dev Channel, Build 3125 (https://github.com/mfuentesg/SyncSettings/issues/63)


#2.4.3

Solved issues:
- Syncing not works (https://github.com/mfuentesg/SyncSettings/issues/67)

#2.4.4

Solved issues:
- Not able to exclude arbitrary files (https://github.com/mfuentesg/SyncSettings/issues/51)
