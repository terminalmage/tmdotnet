Title: Using WeeChat Filters to Suppress IRC "WHO" Command Output
Date: 2014-10-12 19:48:00
Category: Blog
Tags: weechat
Slug: 2014/10/12/using-weechat-filters-to-suppress-irc-who-command-output
Author: Erik Johnson
Summary: This past week my [employer](http://saltstack.com/) has been trying out [Slack](https://slack.com/) for internal communication...

This past week my [employer](http://saltstack.com/) has been trying out
[Slack](https://slack.com/) for internal communication. I'm a huge fan of its
Android app, as it beats connecting to my IRC bouncer and typing commands into
an IRC client. Let's face it, IRC was not made for smartphones.

However, during the work day I don't use my smartphone to chat. Being the
stubborn guy I am, I do not like chatting in a web interface, as nice as
[Slack](https://slack.com/)'s may be. Luckily for me,
[Slack](https://slack.com/) provides both IRC and
[XMPP](http://en.wikipedia.org/wiki/XMPP) gateways.

I set up the IRC gateway on my bouncer, but was annoyed to find that
[Slack](https://slack.com/) seemed to be running a lot of **WHO** commands.

    :::
    18:26:13    znc_slack  -- | [:End] of WHO list
    18:26:15    znc_slack  -- | [:End] of WHO list
    18:29:07    znc_slack  -- | [:End] of WHO list
    18:29:09    znc_slack  -- | [:End] of WHO list
    18:29:12    znc_slack  -- | [:End] of WHO list

This would result in activity being logged in the core buffer, which would trip
the activity monitor I have set in [tmux](http://tmux.sourceforge.net/),
falsely making me think there was chat activity in WeeChat.

Fortunately, WeeChat has an excellent [filter
system](http://www.weechat.org/files/doc/stable/weechat_user.en.html#command_weechat_filter).
The way it works is by looking at each message's tags, and filtering messages
matching the tags you specify. To see which tags are assigned, you can run
**/debug tags**. This changes the output to the following:

    :::
    18:26:13    znc_slack  -- | [:End] of WHO list [irc_315,irc_numeric,log3]
    18:26:15    znc_slack  -- | [:End] of WHO list [irc_315,irc_numeric,log3]
    18:29:07    znc_slack  -- | [:End] of WHO list [irc_315,irc_numeric,log3]
    18:29:09    znc_slack  -- | [:End] of WHO list [irc_315,irc_numeric,log3]
    18:29:12    znc_slack  -- | [:End] of WHO list [irc_315,irc_numeric,log3]

In this case, we are going to filter messages with the **irc_315** tag which,
as we can see from [RFC 1459](http://tools.ietf.org/html/rfc1459#page-50) is a
reply to a **WHO** command (exactly what we want to filter).

Running **/debug tags** again will remove the debugging output.

Now that we know what we want to filter, building a filter command is easy:

    :::irc
    /filter add slack_who irc.server.znc_slack irc_315 *

Let's unpack this to understand it better:

* **/filter** - The WeeChat [filter
  command](http://www.weechat.org/files/doc/stable/weechat_user.en.html#command_weechat_filter)
* **add** - We're adding a new filter
* **slack\_who** - The name for the filter (user-provided, can be anything)
* **irc.server.znc\_slack** - Limits this filter to the core buffer (a.k.a. the
  **server** buffer), and only for the **znc\_slack** server. In this case,
  **znc\_slack** was the name I gave my [Slack](https://slack.com/) connection.
  If you're not sure what to put here, it can be found right next to the
  timestamp.
* **irc\_315** - The tag on which we are filtering
* __\*__ - Filter all messages that match the specified buffer(s) and tag(s).
  In place of this asterisk, a regular expression can be substituted to filter
  only messages which match the buffer(s), tag(s), and regex. But I want to
  filter all matching messages, so the asterisk is sufficient for my needs.

<br>
And that's all there really is to it. This method can be applied to any kind of
content you wish to filter.
