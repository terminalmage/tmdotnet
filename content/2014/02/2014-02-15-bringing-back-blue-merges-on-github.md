Title: Bringing "Blue Merges" Back to GitHub
Date: 2014-02-15 23:57:12
Category: Blog
Tags: programming, github
Slug: 2014/02/15/bringing-blue-merges-back-to-github
Author: Erik Johnson
Summary: I <3 GitHub. I spend a lot of time there, as evidenced by my current 226-day activity streak. A few weeks ago, while I was in Utah for [SaltConf](http://saltconf.com), GitHub rolled out a significant redesign...

<div style='float: right; margin-left: 5px; margin-bottom: 5px;' markdown='1'>
<img src='/images/github_streak_226.png' alt='226-day activity streak' title='226-day activity streak' style='width: 400px; height: 276px;' />
</div>

I <3 GitHub. I spend a lot of time there, as evidenced by my current
226-day activity streak. A few weeks ago, while I was in Utah for
[SaltConf](http://saltconf.com), GitHub rolled out a [significant
redesign](https://github.com/blog/1767-redesigned-conversations). The new
conversation views are great, and the ability to tag pull requests is also a
fantastic touch. But one change that didn't sit well with me is the fact that
the color for merged pull requests was changed to an ugly dark purple.

I gave the change a couple weeks to see if I'd grow accustomed to it. I did
not. So, I set out to see what I could do about it. Luckily, there is a Firefox
extension called
[Stylish](https://addons.mozilla.org/en-US/firefox/addon/stylish/), which is
designed for the purpose of inserting custom CSS into webpages. But first, I
needed to figure out the CSS elements which needed to be overridden. I did this
using
[Firebug](https://addons.mozilla.org/en-US/firefox/addon/firebug/?src=search).
When enabled, if you click a design element, it is highlighted and its CSS
configuration is displayed on the far right pane of the Firebug area. I
scrolled until I found an element with a **background** parameter. Hovering
your mouse over a hex color code in Firebug will display the corresponding
color. Below, you can see that ugly purple:

<br><br>
<div style='text-align: center' markdown='1'>
![Firebug CSS Inspector](/images/github_firebug.png 'Firebug CSS Inspector')
</div>

<br><br>
Clicking on the CSS filename (shown in dark blue) above that block of CSS takes
you to the left-side pane of Firebug and switches to the CSS tab, displaying a
nicely-formatted representation of the selected block of CSS code which can be
copied and pasted. From here, it was a simple matter of finding each of these
on both of the pages that display that purple color (my profile page, as well
as a page with a merged pull request), and copying them to a text file for
safe-keeping. Once I had found them all, I created the following simple
[Stylish](https://addons.mozilla.org/en-US/firefox/addon/stylish/) theme:

<br><br>

    :::css
    @namespace url(http://www.w3.org/1999/xhtml);
    @-moz-document regexp("https:\/\/(?:www\.)?github\.com\/.*") {

        .simple-conversation-list > li .state-merged {
            background: none repeat scroll 0 0 #7AADDE;
        }

        .overall-summary .graphs .mini-bar-graph a.merged-pulls {
            background: none repeat scroll 0 0 #7AADDE;
        }

        ul.summary-stats li .octicon-git-pull-request {
            color: #7AADDE;
        }
        
        .branch-action-state-merged .branch-action-icon {
            background-color: #7AADDE;
        }

        .new-discussion-timeline .discussion-event-status-merged .discussion-item-icon {
            background-color: #7AADDE;
            padding-left: 2px;
        }

        .gh-header-status.merged {
            background-color: #7AADDE;
        }

    }

<br><br>
The
[@-moz-document](https://developer.mozilla.org/en-US/docs/Web/CSS/@document)
rule at the top restricts this rule to GitHub only, using a regular expression.
For the replacement color, I chose
[#7AADDE](http://www.color-hex.com/color/7aadde), which was the closest I could
find to a match for the old blue color, according to my memory. The results are
very nice:

<div style='text-align: center' markdown='1'>
**BEFORE**
<br><br>
![Before](/images/github_before.png 'Before')
</div>

<div style='text-align: center' markdown='1'>
**AFTER**
<br><br>
![After](/images/github_after.png 'After')
</div>

<br><br>
Ahhhh... much better...
