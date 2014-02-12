Title: HOWTO: play radio stations' online streams in your media player
Date: 2012-05-13 18:23
Category: Blog
Tags: linux
Slug: 2012-05-13-howto-play-radio-stations-online-streams-in-your-media-player
Author: Erik Johnson
Summary: I like to listen to streaming radio while I work. However, sometimes having a web browser open is too much of a temptation to just start browsing and ignore the work that needs to be done...

I like to listen to streaming radio while I work. However, sometimes having a
web browser open is too much of a temptation to just start browsing and ignore
the work that needs to be done. So, I recently figured out how to play
streaming radio stations in my media player of choice. This post will walk you
through the process so that you can do the same.

You will need the following:

* Firefox
* [Firebug (Firefox extension)](https://addons.mozilla.org/en-US/firefox/addon/firebug/)
* Flash plugin (needed for most stations' stream players)
* Any media player capable of playing media URLs

Before we start, understand that this walkthrough won't work for every kind of
streaming radio station. You won't get it to work for things like Pandora,
Last.FM, etc. This covers streams for local radio stations which allow you to
listen through their website.

To start, open Firefox, go to the radio station's website, and start up the
radio stream. This is to make sure that you are on the correct page. Next, hit
**Ctrl+Shift+C** to bring up the Firebug control panel, which will appear at
the bottom of your browser window. Firebug has several different panels
(Console, HTML, etc.), and we will be using the **Net** panel to grab the radio
stream's URL, but first we need to make sure that it is enabled. Click where it
says "Net", and if the panel is disabled, you'll see a message saying so, with
instructions on enabling it.

<div style='text-align: center' markdown='1'>
![Firebug 'Net' Panel](/images/firebug_netpanel_enabled.png "Firebug 'Net' Panel")
</div>

Now that the **Net** panel is enabled, refresh the page and you'll start seeing
items appear below. These are all of the HTML GET and POST requests, one of
which will (hopefully) be the radio stream. **NOTE:** when reloading the page,
sometimes Firebug will go back to the **HTML** panel. If it does this, just
click on the **Net** panel to go back to it.

Let the radio stream load and let it play for a few seconds. The far right of
the net panel will show the access times for the GETs and POSTs. Most will be
represented in terms of milliseconds (ms) and will be split into different
colors representing the time spent on DNS lookups, connecting, waiting for a
response, etc. What we are looking for here is a GET which should have an
all-grey bar, with the access time continuing to count up as the stream
continues to run.

<div style='text-align: center' markdown='1'>
![Copy the stream URL](/images/get_stream_url.png 'Copy the stream URL')
</div>

Right-click on that line and select **Copy Location**, and you will have the
stream's URL in your clipboard. You can then play the URL in your media player.
For instance, in VLC this is done by clicking **Media**, then **Open Network
Stream**.

Most stream URLs contain a bunch of querystring data, which in most cases (at
least in my experience) is not needed to play the stream. You can try removing
everything starting with the question mark and see if the stream still plays.

Since I prefer doing most things in a terminal instead of a GUI, my preference
is to use mplayer to play the stream from the command line. To keep from having
to remember the URL, I use an alias:

    :::bash
    alias wscr='mplayer -cache 128 "http://2343.live.streamtheworld.com:80/WSCRAMDIALUPCMP3"'

The **-cache 128** parameter will make mplayer buffer the stream so that a
temporary slowdown or loss of connection will be less likely to make the stream
stop playing.
