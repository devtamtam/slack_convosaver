import slack_sdk
import json
import os
from datetime import datetime
import requests

def load_settings():
    """Load settings from settings.json file"""
    try:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            return settings
    except FileNotFoundError:
        print("Error: settings.json file not found")
        exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in settings.json")
        exit(1)

# Load settings from file
settings = load_settings()
SLACK_BOT_TOKEN = settings['SLACK_BOT_TOKEN']
channel_id = settings['CHANNEL_ID']

# Initialize the Slack client
slack_client = slack_sdk.WebClient(token=SLACK_BOT_TOKEN)

# Function to fetch conversation history
def get_conversation_history(channel_id):
    try:
        result = slack_client.conversations_history(channel=channel_id, limit=10)  # Limiting to 10 messages
        return result["messages"]
    except slack_sdk.errors.SlackApiError as e:
        print(f"Error fetching conversation history: {e}")
        return None

def format_message(message):
    """Format message for better readability"""
    formatted_msg = {
        'text': message.get('text', ''),
        'user': message.get('user', ''),
        'timestamp': datetime.fromtimestamp(float(message.get('ts', 0))).strftime('%Y-%m-%d %H:%M:%S'),
        'replies': message.get('reply_count', 0)
    }
    
    # Add files information if present
    if 'files' in message:
        formatted_msg['files'] = [{
            'id': file.get('id'),
            'name': file.get('name'),
            'filetype': file.get('filetype'),
            'url_private': file.get('url_private'),
            'size': file.get('size'),
            'mimetype': file.get('mimetype')
        } for file in message.get('files', [])]
    
    return formatted_msg

def download_file(file_info, download_dir):
    """Download a file from Slack"""
    try:
        # Create download directory if it doesn't exist
        os.makedirs(download_dir, exist_ok=True)
        
        # Get file from Slack using the url_private_download URL if available
        url = file_info.get('url_private_download', file_info['url_private'])
        
        headers = {
            'Authorization': f'Bearer {SLACK_BOT_TOKEN}',
            'User-Agent': 'SlackBot'
        }
        
        response = requests.get(
            url,
            headers=headers,
            stream=True,
            allow_redirects=True
        )
        
        # Check if request was successful
        if response.status_code == 200:
            # Create filename for downloaded file
            file_path = os.path.join(download_dir, file_info['name'])
            
            # Write file to disk in binary mode
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive chunks
                        f.write(chunk)
            
            print(f"Downloaded: {file_info['name']}")
            return file_path
        else:
            print(f"Failed to download {file_info['name']}: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading file {file_info['name']}: {e}")
        return None

def save_messages_to_json(messages, download_files=True):
    """Save messages to a JSON file with timestamp-based filename and download files"""
    # Create filename with current timestamp
    current_time = datetime.now()
    filename = f"{current_time.strftime('%Y%m%d%H%M')}.json"
    
    # Create download directory based on timestamp
    download_dir = f"slack_files_{current_time.strftime('%Y%m%d%H%M')}"
    
    # Format messages for better readability
    formatted_messages = [format_message(msg) for msg in messages]
    
    # Download files if requested
    if download_files:
        for message in formatted_messages:
            if 'files' in message:
                for file_info in message['files']:
                    file_path = download_file(file_info, download_dir)
                    if file_path:
                        # Update the file info with local path
                        file_info['local_path'] = file_path

    # Save messages to JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(formatted_messages, f, indent=4, ensure_ascii=False)  # ensure_ascii=False for proper character handling
    
    print(f"Messages saved to {filename}")

# Main function
def main():
    # Get conversation history
    messages = get_conversation_history(channel_id)
    
    if messages:
        # Save messages to JSON file and download files
        save_messages_to_json(messages, download_files=True)
        print("Retrieved and saved 10 most recent messages with files")

if __name__ == "__main__":
    main()