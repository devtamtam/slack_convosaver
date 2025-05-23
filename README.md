# Slack Conversation Saver **ConvoSaver**

A Python script to archive Slack conversations and download associated files.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install -r requirements.txt
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

Check **slack-backup-viewer** :: user firendly GUI

https://github.com/devtamtam/slack-backup-viewer.git

![image](https://github.com/user-attachments/assets/588ec4a5-1849-49be-aebb-ec116a2868b7)


## Note

- Make sure not to commit your `settings.json` file as it contains sensitive information.
- This script is designed for use with public channels and private channels (group chats). It does not support retrieving message history from direct messages (DMs). This is due to privacy limitations enforced by the Slack API, which prevent bots from being added to existing DMs between users
