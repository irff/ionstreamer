#!/bin/bash
python router.py &
python streamer/tweet_streamer.py 0 &
sleep 1
python streamer/tweet_streamer.py 1 &
sleep 1
python streamer/tweet_streamer.py 2 &
sleep 1
python streamer/tweet_streamer.py 3 &
sleep 1
python streamer/tweet_streamer.py 4 &