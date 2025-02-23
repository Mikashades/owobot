# Discord Owo Bot

A simple OwO bot for automating message sending in Discord with captcha detection.

## Features

- Send multiple messages with custom intervals
- Dark theme interface
- Captcha detection system
- Sound and visual alerts
- Message logging
- Auto-stop on captcha

## Requirements

```
pip install pyautogui
pip install pywin32
```

## Usage

1. Enter message text and time interval (in seconds) for each message
2. Set copy count (1-5, recommended: 3)
3. Click "Start" button
4. Click on Discord message input area
5. Bot will automatically:
   - Send messages at specified intervals
   - Check for captcha
   - Stop if captcha detected
   - Show alerts and notifications

## Important Notes
- Bot requires Windows OS
- Keep mouse cursor above message area
- Bot will stop automatically if captcha detected
- Available in both English (main_en.py) and Turkish (main_tr.py)
- At least one message and time interval must be filled
- Time intervals must be positive numbers
- Copy count must be between 1-5
- Invalid inputs will trigger error messages
- Bot stops automatically on any critical error

## Warning

Use at your own risk. This bot is for educational purposes only.

Made by Mikashades©
