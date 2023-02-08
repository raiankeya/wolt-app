from typing import Dict, List
from datetime import datetime

from .constants import EVENT_TYPE_OPEN


def format_time(timestamp: int) -> str:
    formatted_time = datetime.utcfromtimestamp(timestamp).strftime("%H:%M %p")
    return formatted_time


def format_time_range(opening_time: str, closing_time: str) -> str:
    return f"{opening_time} - {closing_time}"


def format_output(data: dict) -> str:
    """Returns the human readable string from the formatted dict."""
    lines = []
    for day, times in data.items():
        if times:
            lines.append(f'{day.title()}: {", ".join(times)}')
        else:
            lines.append(f"{day.title()}: Closed")
    formatted_output = "\n".join(lines)

    return formatted_output


def to_human_readable_times(data: dict) -> str:
    parsed_times_dict = parse_input_times(data)
    human_readable_times = format_output(parsed_times_dict)

    return human_readable_times


def parse_input_times(data: dict) -> Dict[str, List[str]]:
    """
    Parses the serialized data dict and convert it to a dict of human readable data
    in the format: {day: list_of_opening_hour_ranges_per_day}
    """
    opening_time = None
    day_of_opening_time = None
    overflowing_closing_time = None
    times_dict = {}
    for day, events_of_a_day in data.items():
        times_dict[day] = []
        for event in events_of_a_day:
            if event["type"] == EVENT_TYPE_OPEN:
                opening_time = format_time(event["value"])
                day_of_opening_time = day
            else:
                closing_time = format_time(event["value"])
                if opening_time is not None:
                    times_dict[day_of_opening_time].append(
                        format_time_range(opening_time, closing_time)
                    )
                else:
                    overflowing_closing_time = closing_time

    if overflowing_closing_time:
        times_dict[day].append(
            format_time_range(opening_time, overflowing_closing_time)
        )

    return times_dict
