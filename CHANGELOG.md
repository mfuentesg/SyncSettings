## v3.0.8

This version includes some minor fixes.

- https://github.com/mfuentesg/SyncSettings/issues/165
- https://github.com/mfuentesg/SyncSettings/issues/164

## v3.0.7

This version includes encoding fixes, and minor improvements.

- https://github.com/mfuentesg/SyncSettings/issues/144
- https://github.com/mfuentesg/SyncSettings/issues/119

## v3.0.3

This version includes encoding issues on download command, and minor improvements.

- https://github.com/mfuentesg/SyncSettings/issues/115
- https://github.com/mfuentesg/SyncSettings/issues/113

## v3.0.2

Fix error when installed_packages key does not exists

- https://github.com/mfuentesg/SyncSettings/issues/112 

## v3.0.1

Are you behind a restricted network?

This version is for you, `http_proxy` and `https_proxy` properties were added to avoid those annoying network restrictions.

https://github.com/mfuentesg/SyncSettings/issues/87

## v3.0.0

I am happy to announce a new version of Sync Settings.
This version includes a lot of improvements and bug fixes

In the previous version of `Sync Settings`, all files are replaced automatically once completed the download,
causing errors like infinite sublime text alerts when a dependency is not installed in your computer.

In this version, Sync Settings will use `Package Control` commands, to ensure the installation of your packages,
before to update `Preferences.sublime-settings` and `Package Control.sublime-settings` files.


Improvements:

- Add `unix shell style` for `excluded_files` and `included_files` options, using `fnmatch` library (wildcard).
- Improve error messages due to connection error, or insufficient token permissions.
- Delete custom logger by builtin logger
- Delete stylized popups by status bar messages
- Add ability to retrieve a gist without an access token
- Better documentation

Bug fixes:

- Exclude `SyncSettings.sublime-settings` on sync (https://github.com/mfuentesg/SyncSettings/issues/80)
- Fix files priority (https://github.com/mfuentesg/SyncSettings/issues/82)
- Colour scheme needs to load first (https://github.com/mfuentesg/SyncSettings/issues/90)
- Fix utf-8 error (https://github.com/mfuentesg/SyncSettings/issues/83)


## 2.4.4

Solved issues:
- Not able to exclude arbitrary files (https://github.com/mfuentesg/SyncSettings/issues/51)


## 2.4.3

Solved issues:
- Syncing not works (https://github.com/mfuentesg/SyncSettings/issues/67)

## 2.4.2

Solved issues:
- Fails with Dev Channel, Build 3125 (https://github.com/mfuentesg/SyncSettings/issues/63)

## 2.4.0

- Rename cache file from `.sync_settings_cache` to `.sync-settings.cache` (~/.sync_settings_cache)
- New Command `Sync Settings: Edit User Settings` by @JohaWeber
- Bug Logging was improved

Issues:
- Remove SyncSettings references from download process (https://github.com/mfuentesg/SyncSettings/issues/50)
- Download doesn't work and clears Gist ID (https://github.com/mfuentesg/SyncSettings/issues/46)
- downloading append a newline in configfile (https://github.com/mfuentesg/SyncSettings/issues/45)
- sync_settings_cache links to wrong directory (https://github.com/mfuentesg/SyncSettings/issues/42)

## 2.3.1

* Fix encoding bug
* Allow special chars like 'ç'

## 2.3.0

* Check if your settings are up to date on startup
* Add PopUp support to ST Build 3070 or higher
* Auto upgrade your Settings if the auto_upgrade option is enabled
* auto_upgrade option was added
* Minor Enhancements
* MIT license was added


## 2.2.6

* included_files option was added
* Minor Fixes


## 2.2.5

* Minor Fixes

## 2.2.4

* Add Delete and Create Command
* Add Delete Command
* Enhancement on Excluded files filter
* Refactoring
* Minor Fixes

## 2.2.2

* Add Support to Python 2.7


## 2.2.1

This version has some bug fixes

* Restore base encoding to read the files
* Minor fixes

## 2.2.0

This version has some bug fixes

* Code 422 - Validation Failed
* Re-order file structure
* Enhance testing

##2.1.1

This version has some bug fixes

* Add base encoding to read the files
* When a file not exists in other host this file is not created
* Function enhancements

## 2.0.0

This version has some bug fixes found and new features

* All files inside on User folder will be included
* Enhancements on the excluded files list
  - Exclude by filename
  - Exclude by extension
  - Exclude by folder
* Show progress indicator on the status bar
* Error messages more descriptive
* Minor bug fixes

## 1.2.0

This version executes each command as a thread, allowing that the application is not lock.

* Added threading support

## 1.1.0

* Now your operations and errors are saved
* New commands added
* Custom Exception Added
* Fix minor errors

## 1.0.1

This version has some bug fixes found

* When files do not exist
* Remove the file repeated in the list of excluded files
* Include Default <platform>.sublime-keymap files and the User Settings
* Include Changelog file
