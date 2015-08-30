#!/bin/bash
python streamer/tweet_streamer.py &
sleep 4
python streamer/tweet_streamer.py &
sleep 4
python streamer/tweet_streamer.py &
