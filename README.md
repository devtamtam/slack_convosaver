# Slack Conversation Saver

A Python script to archive Slack conversations and download associated files.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install slack_sdk requests
```

3. Create a `settings.json` file with your Slack credentials:
```json
{
    "SLACK_BOT_TOKEN": "your-slack-bot-token",
    "CHANNEL_ID": "your-channel-id"
}
```

## Usage

Run the script:
```bash
python convo_saver.py
```

The script will:
- Fetch the 10 most recent messages from the specified Slack channel
- Save messages to a timestamped JSON file (YYYYMMDDHHMM.json)
- Download any attached files to a timestamped directory
- Properly handle binary files and Japanese text

## To See the BackUP

Check **slack-backup-viewer**

https://github.com/devtamtam/slack-backup-viewer.git

## Note

Make sure not to commit your `settings.json` file as it contains sensitive information.
