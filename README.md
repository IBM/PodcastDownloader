Podcast_Downloader
========================================================

The Podcast Downloader is a simple app, to provide a easy and reliable
way of parsing podcast RSS and download them in a timely manner.

The Scheduler module is reponsible for parsing the RSS provided by user, and
post the URLs needs to be downloaded to the Downloader.

The Downloader is simple HTTP server responsible for downloading the URls provided by
Scheduler.

The Cli module is to help user configure databases to manage the users, RSS, URL links etc.
