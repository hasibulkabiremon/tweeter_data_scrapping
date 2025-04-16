from datetime import datetime

import pytz


def timeChange(t):
    original_timestamp = t

    # Convert to datetime object
    dt_object_utc = datetime.fromisoformat(original_timestamp.replace("Z", "+00:00"))

    # Convert to Bangladeshi time
    bangladesh_timezone = pytz.timezone("Asia/Dhaka")
    dt_object_bangladesh = dt_object_utc.astimezone(bangladesh_timezone)

    # Convert to desired format
    formatted_timestamp = dt_object_bangladesh.strftime("%Y-%m-%d %H:%M:%S")

    print(formatted_timestamp)
    return formatted_timestamp
