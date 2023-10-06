from validate_email_address import validate_email
from urllib.parse import urlparse
import validators
import os
import uuid
from datetime import datetime, timedelta


def is_valid_email(email):
    return validate_email(email)
    
def is_valid_url(text):
    # Check if the text starts with a valid URL scheme
    if validators.url(text):
        # Parse the URL using urlparse
        parsed_url = urlparse(text)
        # Check if the scheme and netloc are present
        if parsed_url.scheme and parsed_url.netloc == "www.amazon.de":
            return True
    return False

def is_photo_saved(photo):
    file_id = photo.file_id
    file_path = context.bot.get_file(file_id).file_path
            
    # Download the photo
    file = context.bot.download_file(file_path)
            
    # Create the save directory if it doesn't exist
    os.makedirs(SAVE_DIR, exist_ok=True)
    isSaved = save_buyer_info(update, context, "amazon_screenshot")

    # Save the photo with a unique name
    save_path = os.path.join(SAVE_DIR, f"{file_id}.jpg")
    with open(save_path, "wb") as f:
        f.write(file)


def unique_id():
    # Generate a UUID4 (random) ID
    unique_id = uuid.uuid4()
    
    # Convert the UUID to a string
    unique_id_str = str(unique_id)
    
    return unique_id_str

def is_older_than(date, weeks=0, days=0, hours=0):
    current_date = datetime.now()
    date_format = "%Y-%m-%d %H:%M:%S"
    # date = datetime.strptime(date, date_format)
    past_date = current_date - timedelta(weeks=weeks, days=days, hours=hours)
    
    if date < past_date:
        return True
    else:
        return False
