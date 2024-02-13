import re


class DurationUtils:

    # For if we have feature add new urgency
    def parse_urgency_duration(self, duration: str) -> float:
        # Match patterns like "5 min", "30 min", "1 hr", etc.
        # TODO: Regex for thai language
        match = re.match(r'(\d+)-?(\d+)?\s*(min|hrs?)', duration)
        if match:
            # Extract the minimum time value from the match groups
            min_time = int(match.group(1))
            time_unit = match.group(3)
            # Convert hours to minutes if necessary
            if 'hr' in time_unit:
                min_time *= 60
            return min_time
        # Return a high number for unknown or less urgent durations
        return float('inf')
