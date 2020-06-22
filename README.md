# Sync Settings
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-5-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

[![SyncSettings](https://img.shields.io/packagecontrol/dt/Sync%20Settings.svg?maxAge=2592000)](https://packagecontrol.io/packages/Sync%20Settings)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)
[![SyncSettings release](https://img.shields.io/github/release/mfuentesg/SyncSettings.svg)](https://img.shields.io/github/release/mfuentesg/SyncSettings.svg?maxAge=2592000)
[![Build Status](https://travis-ci.org/mfuentesg/SyncSettings.svg?branch=master)](https://travis-ci.org/mfuentesg/SyncSettings)
[![Coverage](https://img.shields.io/codecov/c/github/mfuentesg/SyncSettings.svg?style=flat)](https://codecov.io/gh/mfuentesg/SyncSettings)


[![Become a backer](https://opencollective.com/syncsettings/tiers/backer/badge.svg?label=backer&color=brightgreen)](https://opencollective.com/syncsettings)
[![Become a sponsor](https://opencollective.com/syncsettings/tiers/sponsor/badge.svg?label=sponsor&color=brightgreen)](https://opencollective.com/syncsettings)

With [Sync Settings](https://packagecontrol.io/packages/Sync%20Settings), you are able to synchronize your [Sublime Text](http://sublimetext.com/) settings among multiple devices, and keep them updated.

Being powered by GitHub-Gists, [Sync Settings](https://packagecontrol.io/packages/Sync%20Settings) provides you a reliable cross-platform solution to keep your backups secure.

Please, follow the steps below to getting started with [Sync Settings](https://packagecontrol.io/packages/Sync%20Settings).

> [Sync Settings](https://packagecontrol.io/packages/Sync%20Settings) works on Windows, Linux, macOS and [Sublime Text 3](http://sublimetext.com/3).


## Getting Started

1. Run `Package Control: Install Package` command, and looks for [Sync Settings](https://packagecontrol.io/packages/Sync%20Settings)
2. Run `Sync Settings: Edit User Settings`
3. **if** *Do you already have a gist?*
    1. Copy `gist id` and put it in config file (`https://gist.github.com/<username>/<gist id>`) (`gist_id` property)
    2. Run `Sync Settings: Download` command to retrieve your backup.
4. **else**
    1. Create an access token [here](https://github.com/settings/tokens/new) with `gist` scope checked.
    2. Put the token in the config file (`access_token` property)
    3. Run `Sync Settings: Create and Upload` command
    
### File Format

Please note - the config file uses the JSON format. A simplified example may look like the following.

```
{
	"access_token": "xxxxxxxxxxxxxxxxxxxxxxxxx",
	"gist_id": "xxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

## Options

By default this plugin operates over [Sublime Text](http://www.sublimetext.com) packages folder (i.e `/Users/marcelo/Library/Application Support/Sublime Text 3/Packages/User`), which means, `excluded_files` and `included_files` will looks for files inside that folder.

| name | type | description |
|---|---|---|
| `access_token`  | `string` | Brings write permission to [Sync Settings](https://packagecontrol.io/packages/Sync%20Settings), over your gists (edit, delete and create). *(This option is not required, if you only want to download your backups)* | 
| `gist_id`  | `string` | Identifier of your backup on [gist.github.com](gist.github.com). |
| `auto_upgrade`  | `boolean` | If is `true`, your settings will be synced with the latest settings on [gist.github.com](gist.github.com) when [Sublime Text](http://www.sublimetext.com) startup |
| `http_proxy`  | `string` | An HTTP proxy server to use for requests. |
| `https_proxy`  | `string` | An HTTPS proxy server to use for requests. |
| `excluded_files`  | `[]string` | In simple words, this option is a black list. Which means, every file that match with the defined pattern, will be ignored on sync. |
| `included_files`  | `[]string` | In simple words, this option is a white list. Which means, every file that match with the defined pattern, will be included on sync, even if it was included on `excluded_files` option. |

> Note: `excluded_files` and `included_files` are patterns defined as [unix shell style](http://tldp.org/LDP/GNU-Linux-Tools-Summary/html/x11655.htm).


## Commands

| command | description |
|---|---|
|**Sync Settings: Create and Upload**|Creates a new backup on `gist.github.com` from your local files|
|**Sync Settings: Delete and Create**|Deletes the remote reference of your gist and then, creates a new backup from your local files to `gist.github.com`|
|**Sync Settings: Upload**|Upload a backup from your local files to `gist.github.com`|
|**Sync Settings: Download**|Retrieves the latest version of your backup, using as reference the `gist_id` property defined in your settings file.|
|**Sync Settings: Delete**|Deletes the remote version of your gist, using as reference the `gist_id` property defined in your settings file. (This action is irreversible)|
|**Sync Settings: Show Logs**|Open a new view, with `Sync Settings` log file|
|**Sync Settings: Edit User Settings**|Open a new view, with `Sync Settings` user settings.|

## Contributors

Thank you for contribute to this project:
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://ferronrsmith.github.io/"><img src="https://avatars2.githubusercontent.com/u/159764?v=4" width="100px;" alt=""/><br /><sub><b>Ferron H</b></sub></a><br /><a href="https://github.com/mfuentesg/SyncSettings/commits?author=ferronrsmith" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/tomahl"><img src="https://avatars0.githubusercontent.com/u/1665481?v=4" width="100px;" alt=""/><br /><sub><b>tomahl</b></sub></a><br /><a href="https://github.com/mfuentesg/SyncSettings/commits?author=tomahl" title="Code">💻</a></td>
    <td align="center"><a href="http://nachvorne.de"><img src="https://avatars3.githubusercontent.com/u/2073401?v=4" width="100px;" alt=""/><br /><sub><b>Johannes Weber</b></sub></a><br /><a href="https://github.com/mfuentesg/SyncSettings/commits?author=JohaWeber" title="Code">💻</a></td>
    <td align="center"><a href="http://mwilliammyers.com"><img src="https://avatars1.githubusercontent.com/u/2526129?v=4" width="100px;" alt=""/><br /><sub><b>William Myers</b></sub></a><br /><a href="https://github.com/mfuentesg/SyncSettings/commits?author=mwilliammyers" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/TheSecEng"><img src="https://avatars1.githubusercontent.com/u/32599364?v=4" width="100px;" alt=""/><br /><sub><b>Terminal</b></sub></a><br /><a href="https://github.com/mfuentesg/SyncSettings/commits?author=TheSecEng" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

## Issues

If you are experimenting an error, or an unusual behavior. Please let me know,  creating a [new issue](https://github.com/mfuentesg/SyncSettings/issues/new) appending the logs provided by the  `Sync Settings: Show logs` command.

## Development

You are welcome to contribute to this project, whenever you want.

**Install dependencies**

This project uses pipenv as environment and package manager, follow the instructions below and start contribute.

```
$ pipenv --python 3.7
$ pip install -r requirements.txt
```

**Run tests**

```
$ pip install nose
$ nosetests tests
```


## License

Sync Settings is licensed under the MIT license.

All of the source code, is under the license:

```
Copyright (c) since 2015, Marcelo Fuentes <marceloe.fuentes@gmail.com>.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Help me keep making awesome stuff

Contribute with me, supporting this project through

[![Become a backer](https://opencollective.com/syncsettings/tiers/backer.svg?avatarHeight=50)](https://opencollective.com/syncsettings)

[![Become a backer](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/PayPal.svg/100px-PayPal.svg.png)](https://opencollective.com/syncsettings)
