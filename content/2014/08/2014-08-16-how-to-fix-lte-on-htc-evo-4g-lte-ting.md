Title: How to Fix LTE on HTC EVO 4G LTE (Ting)
Date: 2014-08-16 15:17:56
Category: Blog
Tags: linux, mutt
Slug: 2014/08/16/how-to-fix-lte-on-htc-evo-4g-lte-ting
Author: Erik Johnson
Summary: I recently switched to [Ting](https://ting.com/) in order to save about $120/month on our family's cell phone bill...

I recently switched to [Ting](https://ting.com/) in order to save
about $120/month on our family's cell phone bill. I purchased a used HTC EVO 4G
LTE and and promptly rooted it, installing a recent nightly of
[CyanogenMod](http://www.cyanogenmod.org/) 11. Once I got up and running,
however, I noticed that I could no longer connect to the Sprint LTE network.

After some searching, I found [this
post](http://forum.xda-developers.com/showpost.php?p=53502055&postcount=16) on
XDA Developers which explains how to point your phone at an LTE access point.

Before making any changes, I strongly recommend booting into recovery and
making a nandroid backup. Also, instead of modifying an existing APN
configuration, I just made a new one by hitting the plus sign.

Lastly, there is no need to install a search app to find where the access point
names are configured. If you are running CM 11, they can be found under
**Settings\ ->\ Mobile Networks\ ->\ Access Point Names**.
