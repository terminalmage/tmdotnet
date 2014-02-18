Title: WeeChat - Error: unknown command "znc" (type /help for help)
Date: 2014-02-17 00:41:00
Category: Blog
Tags: weechat, znc, linux
Slug: 2014/02/17/weechat-error-unknown-command-znc
Author: Erik Johnson
Summary: The [ZNC Wiki](http://wiki.znc.in/) references a **/znc** command often (**/znc detach**, **/znc \*modname help,**, etc.). When I initially set up ZNC a while back, I kept getting an error when trying to use this command...

The [ZNC Wiki](http://wiki.znc.in/) references a **/znc** command often (**/znc detach**, **/znc \*modname help**, etc.). When I initially set up ZNC a while back, I kept getting an error when trying to use this command:

    :::
    15:19:42 weechat =!= Error: unknown command "znc" (type /help for help)

<br>
I eventually gave up and went back to running [WeeChat](http://weechat.org/)
from within a [tmux]([WeeChat](http://weechat.org/)) session.

<br>
This past weekend, I gave ZNC another go. After a bit of troubleshooting, I
found that support for this command seems to be implemented on a
client-by-client basis, and [WeeChat](http://weechat.org/) simply did not
support it. However, the usage of **/znc** is simply a shortcut for **/quote
znc**. Therefore, it is a simple matter of creating an alias in
[WeeChat](http://weechat.org/) (and saving the configuration so the alias is
available next time [WeeChat](http://weechat.org/) starts):

<br>

    :::
    /alias znc quote znc
    /save

<br>
After doing this, it is possible to detach from a channel using
**/znc detach #channel\_name**.
