#!/bin/bash
python router.py &
python streamer/tweet_streamer.py &
python streamer/tweet_streamer.py &
