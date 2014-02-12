Title: Printing to PDF in Mutt
Date: 2011-10-12 18:05
Category: Blog
Tags: linux, mutt
Slug: 2011-10-12-printing-to-pdf-in-mutt
Author: Erik Johnson
Summary: When using my netbook, I don't typically have a printer available. My printer is connected to my wife's desktop computer which doesn't stay on all the time...

When using my netbook, I don't typically have a printer available. My printer
is connected to my wife's desktop computer which doesn't stay on all the time,
so I can't rely on sharing the printer to the network and sending documents to
it through her computer. Moreover, I'm not all that fond of printing things
when saving as a PDF will do.

My email client of choice is [Mutt](http://www.mutt.org/). By default, Mutt
uses the **lpr** command to print, which sends the message to the
default printer. But I don't want to actually print the message, I'd like a PDF
instead. Luckily for me, as with pretty much anything in Mutt, it is possible
to change the default behavior and supply a different command to print
messages. Below you can see a short shell script I wrote which will create a
PDF from the message contents:

    :::bash
    #!/usr/bin/env sh
    INPUT="$1" PDIR="$HOME/tmp/mutt_print" OPEN_PDF=zathura

    # check to make sure that enscript and ps2pdf are both installed
    if ! command -v enscript >/dev/null || ! command -v ps2pdf >/dev/null; then
        echo "ERROR: both enscript and ps2pdf must be installed" 1>&2
        exit 1
    fi

    # create temp dir if it does not exist
    if [ ! -d "$PDIR" ]; then
        mkdir -p "$PDIR" 2>/dev/null
        if [ $? -ne 0 ]; then
            echo "Unable to make directory '$PDIR'" 1>&2
            exit 2
        fi
    fi

    tmpfile="`mktemp $PDIR/mutt_XXXXXXXX.pdf`"
    enscript --font=Courier8 $INPUT -G2r -p - 2>/dev/null | ps2pdf - $tmpfile
    $OPEN_PDF $tmpfile >/dev/null 2>&1 &
    sleep 1
    rm $tmpfile


The body of the email will be passed to the script by Mutt as the first
argument, or **$1**, which I store in the **INPUT** variable. Notice that I'm
also defining a couple other variables at the top of the script. The first,
**PDIR**, is a directory where the created PDF should be located<span
style='color: red;'>\*</span>. Secondly, I'm defining a command which should
be executed to open the PDF once it has been created. I prefer a lightweight
PDF viewer called [zathura](http://pwmt.org/projects/zathura/) but any PDF
viewer (evince, okular, etc.) can be substituted here.

Just below these variable definitions, I make sure that the commmand-line tools
I'm using to create the PDF, (**enscript** and
**ps2pdf**), are installed. There's not much of a reason to try
creating the PDF if they're not present, so a helpful reminder printed to
stderr will notify you in the event that they are not installed. In most Linux
distributions, these tools are found in the **enscript** and
**ghostscript** packages, respectively.

You may have noticed that I am not using the **which** command to determine if
these commands are in my **$PATH**. A recent [blog
entry](http://pthree.org/2011/09/26/avoid-using-which1/) by Aaron Toponce
alerted me to the fact that **which** is not consistently implemented across
platforms, and may not set a proper exit status or write error messages to
stderr. POSIX provides a command named *command* (what else?), which is
consistent across platforms. Running it with -v will print the path of the
first matching executable in your **$PATH** and set an exit status of 0. If
there is no match, a non-zero (or false) exit status is set. I don't care about
the path to the executable, so this output is redirected to **/dev/null**.

If you would rather use a different font for the PDF, you can find a list of
PostScript font names
[here](http://en.wikipedia.org/wiki/PostScript_fonts#Core_Font_Set)

When opening the PDF using the pre-defined command, all output is redirected to
/dev/null. This is because GUI apps, when run from the command line, will
typically print diagnostic messages, warnings, or errors to stdout/stderr.
While these messages can be useful for troubleshooting purposes, any output
from the script will be displayed in your Mutt window, which will look very
ugly. So, this output is discarded.

In order to get Mutt to call the script in place of **lpr**, you will need to
add the following line to your **.muttrc** file (use the path where you saved
the script, of course):

    :::bash
    set print_command="$HOME/bin/mutt_print.sh"

Below is an example of how the result will look. If you do not like the layout,
you can alter it by passing different parameters to the **enscript** command.
Check the manpage and experiment to find what works best for you.

![Example PDF](/images/mutt_print.png 'Example PDF')

So, by replacing the print command with this script, instead of printing the
message directly, your PDF viewer of choice will display the message for you.
If you want to print it out from there, you can do so. I rarely have a need or
desire to print, but this at least leaves me that option. If you want to keep
the message, you'll need to use your PDF viewer to save a copy of it, because
it will be gone once you close the window. Again, choosing to remove the PDF is
a personal preference of mine, so the last two lines of the script can be
commented out or removed if you'd rather keep the PDFs.

<span style='color: red;'>\*</span> I could just place it under /tmp, but since
emails tend to have sensitive or personally-identifiable information, I prefer
to have the temp files located within my home directory, where I can manage
directory permissions and keep these files private.
