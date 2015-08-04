Sync Settings
===============

**Sync Settings**, is a way of keeping the **Sublime Text** synchronized between different operating systems, the synchronization to uses Github Gist allowing you to use all the technologies that this service provides for example to see the history of your configuration file.

##Installation:

Open Package Control and looks for **Sync Settings**, creates an access token in the github (https://github.com/settings/tokens) page, copy and paste this code into the plugin configuration file

```Preferences > Packages Settings > Sync Settings > Settings - User```

##You can set some parameters:

* access_token: refers to the access provided by GitHub token
* gist_id: identifies to the id of the gist that is to be used for synchronization
* excluded_files: are the files that are to be ignored at the time of synchronization, by default files that contain information with your editor license is found in this list.
