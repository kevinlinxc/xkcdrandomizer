# xkcdrandomizer
Randomly generates xkcd comics and posts them to the twitter account [@xkcdrandomizer](https://twitter.com/xkcdrandomizer)

The pipeline is as follows:

1. I use the [xkcd](https://pypi.org/project/xkcd/) package to randomly choose xkcd comics.
2. I cut the comic into panels using a modified [Kumiko](https://github.com/njean42/kumiko)
3. I remove any cut panels that have too large/too small of an area/a bad aspect ratio
4. I resize, append, and repeat until I have the width of an average comic
5. I use Serverless with Docker to package Kumiko, other requirements, and my source code
6. I deploy to AWS Lambda, which has a generous free tier allowing my bot to run until the heat death of the universe

The **src** directory has xkcdRoulette.py, which can be run locally. 
The **serverless** directory is where I set up serverless config files and copied the code base from **src** so that it would be compatible with Lambda (adding a handler).

I mostly followed this guide for using Serverless/Lambda: https://read.iopipe.com/the-right-way-to-do-serverless-in-python-e99535574454

