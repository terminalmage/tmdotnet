Title: Clipboard Access from the Command Line with xsel/xclip
Date: 2011-10-18 09:04
Category: Blog
Tags: linux, command-line-fu
Slug: 2011/10/18/clipboard-access-from-the-command-line
Author: Erik Johnson
Summary: If you've ever found yourself wanting to copy the entire contents of a text file to the clipboard, you may end up doing something like the following...

If you've ever found yourself wanting to copy the entire contents of a text
file to the clipboard, you may end up doing something like the following:

1. Open the file in a text editor.
2. Select all text.
3. Copy to clipboard.

It can be a blow to your productivity to stop what you're doing and do the
above, especially if you were working at the command line (where I spend most
of my time). Another disadvantage to doing it this way is that, if you close
the program from which you copied the text, it clears the clipboard. If you
forget this (or you simply didn't know about this little quirk), then you may
end up wasting *more* time repeating those steps to get that text into your
clipboard.

**xsel** and **xclip** are two commands that allow you to interact with the X
clipboards. Before I explain how to use them though, a short overview of the X
clipboards is in order.

X11 has not one, not two, but *three* clipboards. They are called:

* **PRIMARY** - Also known as the "primary selection" or the "primary
  clipboard". This clipboard is populated whenever you highlight text with the
  mouse. If you've ever highlighted text and noticed that you can paste it by
  clicking the middle button on your mouse, this is the clipboard being used.
* **SECONDARY** - This clipboard is very rarely used anymore, but exists to
  provide a "secondary selection" clipboard to accompany the primary selection.
* **CLIPBOARD** - This is the clipboard you are likely most familiar with. It
  is the one used when you copy text from an application such as a web browser,
  or a GUI text editor like **gedit**.

For our demonstration, we'll use the **CLIPBOARD** selection as it is the
clipboard you're most likely to be using on a regular basis. To begin, let's
create a file we can use to test:

    :::bash
    $ echo "Hello world" >foo.txt

You can verify the file has been created using the **cat** command to print it
to standard output.

    :::bash
    $ cat foo.txt
    Hello world

So, say that we'd like to get the contents of foo.txt to the clipboard. With
**xsel**, you can do it like so:

    :::bash
    $ cat foo.txt | xsel -ib

The **-i** option tells **xsel** to read from standard input. In this case,
standard input is being piped in from the **cat** command. The **b** option
tells **xsel** to use the **CLIPBOARD** selection. To use the **PRIMARY**
selection, you'd replace the **b** with **p**, and to use **SECONDARY** you'd
replace it with **s**.

To copy the contents of the text file to the clipboard using **xclip**, you can
use the following:

    :::bash
    $ cat foo.txt | xclip -selection clipboard

To use the **PRIMARY** selection, you'd replace **clipboard** with **primary**,
and to use **SECONDARY** you'd replace it with **secondary**.

If you press **Ctrl-v** in another application, you'll notice that the words
"Hello world" were pasted.

In addition to copying standard input to the clipboards, **xsel** and **xclip**
both have the ability to print the contents of the clipboards to standard
output. Go ahead and select some text with your mouse and copy it to the
clipboard using **Ctrl-c**, then try the commands below. I will copy the first
several words from the previous sentence as an example, and use **xsel** and
**xclip** to paste them, like so:

    :::bash
    $ xsel -ob
    Go ahead and select some text
    $ xclip -o -selection clipboard
    Go ahead and select some text

In both cases, **-o** is used to tell the command to print the contents of the
specified clipboard to standard output.

The arguments to **xclip** can be abbreviated, so you don't have to type
**-selection clipboard** every time you want to use it. For example:

    :::bash
    $ xclip -o -sel clip
    Go ahead and select some text
    $ xclip -o -s c
    Go ahead and select some text

Both commands have additional features not described here, so check their man
pages for more ideas.

Hopefully these commands can help you save time and increase your productivity
when working from the command line. They've certainly done so for me.
