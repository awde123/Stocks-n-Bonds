#! /bin/bash
./.music >/dev/null 2>&1 &
python .main.py
killall -9 afplay
