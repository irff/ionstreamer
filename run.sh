#!/bin/bash
python router.py &
python streamer/tweet_streamer.py 0 &
python streamer/tweet_streamer.py 1 &
python streamer/tweet_streamer.py 2 &
python streamer/tweet_streamer.py 3 &
python streamer/tweet_streamer.py 4 &