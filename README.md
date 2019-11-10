# audiscogs
I have a number of vinyl records and recording the records with Audacity works great, but there are still a lot of manual steps to take in order to finish the process. Two of the most tedious to me are creating the labels and typing in the metadata. As such, I set out to create tooling to reduce the level of effort required on these two steps.

audiscogs is a script that allows you to generate:

* XML for Importing Album Metadata
* Label Track with Track Times and Labels

This script does not have a lot of bells and whistles at the moment, but it does the basics. 

To run this script, you will need:

* A Discogs Token
* A Discogs Release ID

To get a Discogs Token, go here: <https://www.discogs.com/settings/developers> and click on the button labeled "Generate new token". You will take the token and edit audiscogs.conf and change this line:

~~~
discogs_token="<Your access token>"
~~~
  
So that \<Your access token\> is no longer there and your token from Discogs is there. (Note: audiscogs expects audiscogs.conf to live in the same directory.)
  
Now go to https://www.discogs.com/ and search for the album that you are working on. In this case, we'll search for "Ben Folds Five Live". Once I have found what looks like the album and click the link, I am taken to this page:

<https://www.discogs.com/Ben-Folds-Five-Ben-Folds-Five-Live/master/573909>

This is a **master** link as indicated by master in the URL. We now need to find a release in the list of versions and click that. I have the 2xLP version and so I have clicked the link for that and it is:

<https://www.discogs.com/Ben-Folds-Five-Ben-Folds-Five-Live/release/4722337>

You will notice that this is a **release** link (indicated by release in the URL) and the integer ID at the end of the URL, 4722337, is the release ID.

Once you have that, you can run:

~~~
[karl1@tux-linux Audacity]$ ./audiscogs 4722337
Writing out Ben_Folds_FiveBen_Folds_-4722337-tags.xml for importing into metadata.
Writing out Ben_Folds_FiveBen_Folds_-4722337-label.txt for importing as a label track.
~~~

At any time during your recording / editing, you can go to Edit->Metadata in Audacity and there is a Load button in the "Template" box on that page. Click it and you can browse to the tags.xml for your release and successfully import the metadata.

Once you have stripped out the parts of your recording that you don't want in your final output, you are ready to import the label track. To do this, click File->Import->Label Track in Audacity and select the label.txt for your release. Once this loads, the labels will be in roughly the right place and you can easily move the labels to the correct place at this point.

If a release does not have track times, audiscogs will place the labels every 5 minutes apart and you will have to figure out where they go. (At least the labels have been entered and you don't have to type them!)

So there you have it. I will likely update this project with some more improvements in the coming days and weeks. 

