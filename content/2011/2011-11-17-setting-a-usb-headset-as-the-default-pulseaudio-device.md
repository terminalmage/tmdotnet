Title: Setting a USB Headset as the Default PulseAudio Device Automatically Using Udev
Date: 2011-11-17 01:35
Category: Blog
Tags: linux
Slug: 2011/11/17/setting-a-usb-headset-as-the-default-pulseaudio-device
Author: Erik Johnson
Summary: USB audio peripherals still don't "just work" in Linux, but they're starting to get a *little* easier to use.

USB audio peripherals still don't "just work" in Linux, but they're starting to
get a *little* easier to use.

The last time I tried using
[PulseAudio](http://en.wikipedia.org/wiki/Pulseaudio), a little over two years
ago, I experienced no end of frustration. This probably had as much to do with
a lack of understanding as anything else, but regardless, I have been using
[ALSA](http://en.wikipedia.org/wiki/Advanced_Linux_Sound_Architecture) since
then. However, ALSA's USB support is not very good. Changing the default audio
device requires an application to be restarted to recognize the new default
device. So, I figured I'd give PulseAudio another try and see if I could make
my USB headset "just work" this time around. To my surprise, it was quite easy
to do so, and in this post I will detail the steps I took. I did this on Arch
Linux, but the steps should apply in most Linux distributions.

Before we start, we need to ensure that PulseAudio is A) installed, and B)
running. Most distributions will take care of both of these for you, but due to
the do-it-yourself nature of Arch Linux, in my case it needed to be installed:

    :::
    # pacman -S pulseaudio pulseaudio-alsa
    pavucontrol

Notice that I also installed two other packages, **pulseaudio-alsa** and
**pavucontrol**. The former contains the ALSA plugin for PulseAudio, the latter
is a helpful application for configuring PulseAudio and visualizing your
PulseAudio configuration. Most Linux distributions will include the ALSA plugin
(and may name the package differently), but you may need to manually install
**pavucontrol**.

So, now that I have PulseAudio installed, it needs to be running. If you are
using a desktop environment like KDE, Gnome, etc., PulseAudio should be
automatically started when you login. To see if PulseAudio is running, check
for it in the process table.

    :::bash
    $ ps aux | grep pulseaudio | grep -q start && echo yes || echo no
    yes

OK, PulseAudio is both installed and running. Open **pavucontrol** and click on
the **Output Devices** tab. In the upper-right corner of each device will be a
few buttons. The green one with a check mark on it (outlined in red in the
example below, click for a full-size image) shows which device is the default
output device. The **Input Devices** tab contains its own default as well, but
for now we will focus on the output devices, for the sake of simplicity.

<div style='text-align: center' markdown='1'>
![Headset not plugged in](/images/pavucontrol_nousb.png 'Headset not plugged in')
</div>

Start playing something, preferably in a PulseAudio-compatible application. For
this example, I started a movie file in mplayer from the command-line, forcing
PulseAudio output using the **-ao** (audio output) option:

    :::bash
    $ mplayer -ao pulse foo.mp4

With something now generating audio output, plug in the USB headset, and you'll
notice a new device show up in the **Output Devices** tab. But you'll also
notice that the audio isn't going to the headset yet.

<div style='text-align: center' markdown='1'>
![MPlayer audio not going to headset](/images/pavucontrol_select_device.png 'MPlayer audio not going to headset')
</div>

This can be fixed by clicking the green button next to the headset device, back
on the Output Devices tab. Once clicked (see below), the USB headset will now
be the default audio device for PulseAudio.

<div style='text-align: center' markdown='1'>
![USB headset is now the default device](/images/pavucontrol_usb_default.png 'USB headset is now the default device')
</div>

However, this would have to be repeated every time the headset is plugged in,
which would be an inconvenience to say the very least.

The solution to this is to write a udev rule which will detect when this device
is plugged in, and then run a script to set the headset as the default input
and output device. I'll explain how to do this in a bit, but first we need to
understand what it is that we want to do with this script.

PulseAudio has a command-line tool called **pacmd** which allows you to view
and change the PulseAudio configuration. Plug in the USB headset, and then run
**pacmd dump** to view the current configuration. There is quite a bit of
output, so I have cut out all but the relevant parts:

    :::bash
    $ pacmd dump
    Welcome to PulseAudio! Use "help" for usage information.
    >>> ### Configuration dump generated at Wed Nov 16 23:04:59 2011

    ...

    suspend-sink alsa_output.usb-Logitech_Logitech_USB_Headset-00-Headset.analog-stereo no

    ...

    suspend-source alsa_input.usb-Logitech_Logitech_USB_Headset-00-Headset.analog-mono no

    ...

    set-default-sink alsa_output.pci-0000_00_1b.0.analog-stereo
    set-default-source alsa_input.pci-0000_00_1b.0.analog-stereo

    ### EOF
    >>>

PulseAudio calls output devices "sinks", and input devices "sources". We can
see from this output that the default sink and source belong to the onboard
audio card. To set the headset as the default device, we can use **pacmd** to
set the default sink and source to the ones for the headset. This would be done
with the following two commands:

    :::bash
    $ pacmd set-default-sink alsa_output.usb-Logitech_Logitech_USB_Headset-00-Headset.analog-stereo
    $ pacmd set-default-source alsa_input.usb-Logitech_Logitech_USB_Headset-00-Headset.analog-mono

Try runnng these commands yourself (replacing the sink/source names with the
ones you observed when running **pacmd dump**), and you will notice that the
headset is now the default input and output device if you check the
**pavucontrol** window.

Now that we know how to set the headset as the default device via the command line, we can write a script that will do this for us. However, because this script will eventually be run as root by udev, we need to use the **su** command to run it as the user. The following script will check the process table and then, for each user who is running PulseAudio, will run the two commands needed to set the headset as the default input and output device.

    :::bash
    #!/bin/bash
    #
    # Name:        usb-headset-set-default
    # Description: invokes pacmd to set my Logitech usb headset as the default
    #              audio input and output device.
    #

    # Sleep a little to allow PulseAudio to notice the headset
    sleep 1

    # Check process table for users running PulseAudio
    #
    # ejohnson@tardis:~%  ps axc -o user,command | grep pulseaudio
    # ejohnson pulseaudio
    for user in `ps axc -o user,command | grep pulseaudio | cut -f1 -d' ' | sort | uniq`;
    do
        su $user -c "pacmd set-default-sink alsa_output.usb-Logitech_Logitech_USB_Headset-00-Headset.analog-stereo >/dev/null 2>&amp;1"
        su $user -c "pacmd set-default-source alsa_input.usb-Logitech_Logitech_USB_Headset-00-Headset.analog-mono >/dev/null 2>&amp;1"
        #su $user -c "pacmd dump >>/tmp/debug.log"
    done

    #echo matched at `date` >>/tmp/debug.log

Save this script to **/usr/local/bin/usb-headset-set-default**. It should be
executable, and owned by root. Of course, you should also make sure to replace
the sink and source in the script with the ones you observed when you ran
**pacmd dump**, if they differ. Unplug the headset and plug it back in, then
run the script as root, and in **pavucontrol** you should see that it has been
set as the default input and output device. Note that there are a couple
commands commented out in the script. These can be uncommented for debugging
later on, if needed.

Next, we need a way to detect when the headset is plugged in. We can do this
using **udev**.

[Udev](http://en.wikipedia.org/wiki/Udev) is what handles setting up device
nodes for Linux. When you insert a USB flash drive, and it gets assigned a
device name (like **/dev/sdb**), udev is what takes care of allocating this
device name. Plugging in the headset will generate a number of device nodes. We
can use **udevadm** to see each of them. Unplug the USB headset, then run the
command below. After running it, plug in the USB headset and you should see
some output appear.

    :::bash
    # udevadm monitor --environment | fgrep 'DEVNAME=/dev'
    DEVNAME=/dev/bus/usb/002/118
    DEVNAME=/dev/snd/pcmC1D0c
    DEVNAME=/dev/hidraw0
    DEVNAME=/dev/snd/pcmC1D0p
    DEVNAME=/dev/input/event9
    DEVNAME=/dev/mixer1
    DEVNAME=/dev/dsp1
    DEVNAME=/dev/audio1
    DEVNAME=/dev/snd/controlC1

Note: **udevadm** must be run as root.

Using another **udevadm** command, we can find the udev attributes for one of
these device nodes. I have chosen **/dev/audio1**.

    :::bash
    # udevadm info --attribute-walk --name /dev/audio1

Udevadm info starts with the device specified by the devpath and then walks up
the chain of parent devices. It prints for every device found, all possible
attributes in the udev rules key format. A rule to match, can be composed by
the attributes of the device and the attributes from one single parent device.

    :::bash
      looking at device '/devices/pci0000:00/0000:00:1d.0/usb2/2-1/2-1:1.0/sound/card1/audio1':
        KERNEL=="audio1"
        SUBSYSTEM=="sound"
        DRIVER==""

      looking at parent device '/devices/pci0000:00/0000:00:1d.0/usb2/2-1/2-1:1.0/sound/card1':
        KERNELS=="card1"
        SUBSYSTEMS=="sound"
        DRIVERS==""
        ATTRS{id}=="Headset"
        ATTRS{number}=="1"

      looking at parent device '/devices/pci0000:00/0000:00:1d.0/usb2/2-1/2-1:1.0':
        KERNELS=="2-1:1.0"
        SUBSYSTEMS=="usb"
        DRIVERS=="snd-usb-audio"
        ATTRS{bInterfaceNumber}=="00"
        ATTRS{bAlternateSetting}==" 0"
        ATTRS{bNumEndpoints}=="00"
        ATTRS{bInterfaceClass}=="01"
        ATTRS{bInterfaceSubClass}=="01"
        ATTRS{bInterfaceProtocol}=="00"
        ATTRS{supports_autosuspend}=="1"

      looking at parent device '/devices/pci0000:00/0000:00:1d.0/usb2/2-1':
        KERNELS=="2-1"
        SUBSYSTEMS=="usb"
        DRIVERS=="usb"
        ATTRS{configuration}=="G8 v3.0.0.0"
        ATTRS{bNumInterfaces}==" 4"
        ATTRS{bConfigurationValue}=="1"
        ATTRS{bmAttributes}=="80"
        ATTRS{bMaxPower}=="100mA"
        ATTRS{urbnum}=="663416"
        ATTRS{idVendor}=="046d"
        ATTRS{idProduct}=="0a0b"
        ATTRS{bcdDevice}=="1013"
        ATTRS{bDeviceClass}=="00"
        ATTRS{bDeviceSubClass}=="00"
        ATTRS{bDeviceProtocol}=="00"
        ATTRS{bNumConfigurations}=="1"
        ATTRS{bMaxPacketSize0}=="8"
        ATTRS{speed}=="12"
        ATTRS{busnum}=="2"
        ATTRS{devnum}=="118"
        ATTRS{devpath}=="1"
        ATTRS{version}==" 2.00"
        ATTRS{maxchild}=="0"
        ATTRS{quirks}=="0x0"
        ATTRS{avoid_reset_quirk}=="0"
        ATTRS{authorized}=="1"
        ATTRS{manufacturer}=="Logitech"
        ATTRS{product}=="Logitech USB Headset"

      looking at parent device '/devices/pci0000:00/0000:00:1d.0/usb2':
        KERNELS=="usb2"
        SUBSYSTEMS=="usb"
        DRIVERS=="usb"
        ATTRS{configuration}==""
        ATTRS{bNumInterfaces}==" 1"
        ATTRS{bConfigurationValue}=="1"
        ATTRS{bmAttributes}=="e0"
        ATTRS{bMaxPower}=="  0mA"
        ATTRS{urbnum}=="2640"
        ATTRS{idVendor}=="1d6b"
        ATTRS{idProduct}=="0001"
        ATTRS{bcdDevice}=="0301"
        ATTRS{bDeviceClass}=="09"
        ATTRS{bDeviceSubClass}=="00"
        ATTRS{bDeviceProtocol}=="00"
        ATTRS{bNumConfigurations}=="1"
        ATTRS{bMaxPacketSize0}=="64"
        ATTRS{speed}=="12"
        ATTRS{busnum}=="2"
        ATTRS{devnum}=="1"
        ATTRS{devpath}=="0"
        ATTRS{version}==" 1.10"
        ATTRS{maxchild}=="2"
        ATTRS{quirks}=="0x0"
        ATTRS{avoid_reset_quirk}=="0"
        ATTRS{authorized}=="1"
        ATTRS{manufacturer}=="Linux 3.1.0-4-ARCH uhci_hcd"
        ATTRS{product}=="UHCI Host Controller"
        ATTRS{serial}=="0000:00:1d.0"
        ATTRS{authorized_default}=="1"

      looking at parent device '/devices/pci0000:00/0000:00:1d.0':
        KERNELS=="0000:00:1d.0"
        SUBSYSTEMS=="pci"
        DRIVERS=="uhci_hcd"
        ATTRS{vendor}=="0x8086"
        ATTRS{device}=="0x27c8"
        ATTRS{subsystem_vendor}=="0x1028"
        ATTRS{subsystem_device}=="0x02f4"
        ATTRS{class}=="0x0c0300"
        ATTRS{irq}=="23"
        ATTRS{local_cpus}=="ff"
        ATTRS{local_cpulist}=="0-7"
        ATTRS{dma_mask_bits}=="32"
        ATTRS{consistent_dma_mask_bits}=="32"
        ATTRS{enable}=="11"
        ATTRS{broken_parity_status}=="0"
        ATTRS{msi_bus}==""

      looking at parent device '/devices/pci0000:00':
        KERNELS=="pci0000:00"
        SUBSYSTEMS==""
        DRIVERS==""

Wow, that's a lot of output. Before proceeding to write a udev rule, we need to
know how to utilize the attributes above to come up with a unique rule. [This
page](http://reactivated.net/writing_udev_rules.html) contains an excellent
walkthrough on how to write a udev rule, so go ahead and read it before
continuing. The information about the udev commands is a little outdated (for
instance, most of the commands referenced are now part of **udevadm**), but the
information on rule syntax is very good.

So, we need to come up with a set of attributes that will match, but we also
would like to find a set of attributes that are unique. Multiple matches will
result in the script being run multiple times. In this case, where we're just
running a couple commands to set the default audio devices, there aren't really
any consequences to running the script multiple times, but it's still a good
idea to come up with a unique set of attributes. The rule I came up with was:

    :::bash
    # Set the USB headset as default sink/source when it is plugged in
    KERNEL=="audio?", SUBSYSTEM=="sound", SUBSYSTEMS=="usb", ATTRS{idVendor}=="046d", ATTRS{idProduct}=="0a0b", ACTION=="add", RUN+="/usr/local/bin/run-script-in-background /usr/local/bin/usb-headset-set-default"

I saved this rule to **/etc/udev/rules.d/85-usb-headset.rules**. Notice that
the **RUN** parameter is set to **/usr/local/bin/run-script-in-background
/usr/local/bin/usb-headset-set-default**. In the process of debugging this
rule, I noticed that the script was running, but the headset wasn't being set
as the default sink/source. This is where the commented-out debugging lines
come in. With the debugging commands uncommented, I noticed in the log file
that the headset wasn't showing up in the **pacmd dump** output. It turns out
that PulseAudio doesn't know anything about the headset until udev completes
setting up all the device nodes. This makes perfect sense. However, if udev has
matched the rule and is running the script, this suspends further udev
processing until the script completes. So, what will happen is that the script
tries to set devices that don't yet exist, and in effect nothing happens. To
get around this, we need a way for the command executed by udev to exit
quickly, but allow for a short delay so that udev can finish doing it's thing
before **pacmd** is invoked. So, I created the following script and saved it to
**/usr/local/bin/run-script-in-background**:

    :::bash
    #!/bin/bash
    #
    # Name:        run-script-in-background
    # Description: takes all command-line arguments and runs them as a background command
    #

    $@ &

This script simply takes the arguments fed to it and runs them as a separate
process, in the background. This allows **run-script-in-background** to quickly
exit so that udev can finish.

With the rule and scripts now in place, plug in the USB headset again and you
should notice in **pavucontrol** that the headset is now the default device. If
this is not the case, then use the debugging lines in the
**usb-headset-set-default** script while tailing the log file to determine the
problem. If the headset doesn't show up in the **pacmd dump** output, then you
might need to increase the sleep time at the beginning of the script.

I've been using this udev rule and script for several days now and the headset
is working flawlessly. Hopefully, my instructions can help you get it working
for yourself. All in all, I am very impressed with how well PulseAudio is
working for me, given the nightmares I experienced in the past.
