#!/bin/bash

if hash python3 2>/dev/null; then
    ./halite -t -d "20 20" "python3 overmind.py" "python3 feyleynck.py"
else
    ./halite -d "30 30" "python MyBot.py" "python RandomBot.py"
fi
