#!/bin/bash
clear
echo "╔═══════════════════════════════════════╗"
echo "║      TILTI VPS BOT V2.0               ║"
echo "║   made with ❤️ by UNKN0WN USER         ║"
echo "╚═══════════════════════════════════════╝"
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt 2>/dev/null || pip3 install -r requirements.txt
echo ""
echo "Launching bot..."
python3 TILTI-run.py
