def parse_number_with_suffix(s):
    suffixes = {"K": 10**3, "M": 10**6, "B": 10**9, "T": 10**12}

    s = s.upper()
    if s[-1] in suffixes:
        return int(float(s[:-1]) * suffixes[s[-1]])
    return int(float(s))

from datetime import timedelta

def timedelta_to_str(td: timedelta) -> str:
    # Extract days, hours, minutes, and seconds
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Estimate years and months (simplified)
    years = days // 365
    months = (days % 365) // 30  # Rough approximation of months as 30 days each
    days_remaining = (days % 365) % 30

    # Format as "YYYY-MM-DD HH:MM:SS"
    formatted_str = f"{years:04}-{months:02}-{days_remaining:02} {hours:02}:{minutes:02}:{seconds:02}"
    
    return formatted_str