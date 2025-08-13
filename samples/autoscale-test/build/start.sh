#!/bin/bash

# 백그라운드에서 stress-ng 실행 (4개의 CPU 코어에 스트레스)
stress-ng -c 2 --timeout 0 --cpu-load 90 &

# Flask 애플리케이션 실행
python3 /app/app.py
