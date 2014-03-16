Title: How I Read HTML E-mail with Mutt
Date: 2014-03-16 14:57:00
Category: Blog
Tags: linux, mutt
Slug: 2014/03/16/how-i-read-html-email-with-mutt
Author: Erik Johnson
Summary: I am not a fan of HTML email, but it has become pretty much a standard for business correspondence, invoices, etc. Worse still, many companies...

I am not a fan of HTML email, but it has become pretty much a standard for
business correspondence, invoices, etc. [Mutt](http://www.mutt.org)'s ability
to utilize a
[mailcap](https://www.gnu.org/software/emacs/manual/html_node/emacs-mime/mailcap.html)
file is a good solution, allowing you to open an HTML email in an external
browser, but it does not account for the lazy and/or clueless companies that
distribute email in HTML-only messages, instead of doing The Right Thing™ and
sending a multi-part message with plaintext and html parts. Getting these
messages to play nicely in [Mutt](http://www.mutt.org) takes a bit of work, but
is not that difficult. With a few minor configuration tweaks, the following
setup can be achieved:

1. Multi-part messages with both **text/plain** and **text/html** parts will
   display the **text/plain** message part.
2. Single-part **text/html** messages will be passed through a text web browser
   to be rendered to plaintext.

In either case, it will still be possible to go to the Attachments view and
open the message in an external browser.


The first thing that must be done is to add the following to your .muttrc:

    :::bash
    # Sanely handle multi-part messages (prefer text part, but yield to
    # mailcap-configured rendering for html-only)
    alternative_order text/plain text/html
    auto_view text/html

The **alternative\_order** option tells [Mutt](http://www.mutt.org) to prefer
the **text/plain** part when rendering a multi-part message, while the
**auto\_view** option will make [Mutt](http://www.mutt.org) pass **text/html**
message parts to the command defined in your mailcap file to render them to
plaintext.


The next part is to setup mailcap entries. If you don't already have a file
called **.mailcap** in your home directory, create one and add the following
lines:

    :::
    text/html;  /usr/bin/firefox %s >/dev/null 2>&1; needsterminal
    text/html;  elinks -dump %s; nametemplate=%s.html; copiousoutput

The first of those two entries will be used for viewing the message in an
external program (in this case [Firefox](http://www.firefox.com)). The second
entry will be invoked by [Mutt](http://www.mutt.org)'s **auto\_view** to render
the message and display it in plaintext. I'm using
[elinks](http://elinks.or.cz/index.html) here, but other text web browsers are
capable of performing the same "dump" action as well.


And that's really all you need to do. With these tweaks, even HTML-only email
will look nice in [Mutt](http://www.mutt.org), and you'll still have the
flexibility of opening the message in a GUI web browser if you desire.
