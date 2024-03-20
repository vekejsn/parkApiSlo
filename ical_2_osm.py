import re
from datetime import datetime

def convert_time_to_osm_format(time_str):
    try:
        return datetime.strptime(time_str, '%H:%M:%S').strftime('%H:%M')
    except ValueError:
        try:
            return datetime.strptime(time_str, '%H.%M').strftime('%H:%M')
        except ValueError:
            return time_str

def rrule_to_osm_days(rrule):
    day_map = {"MO": "Mo", "TU": "Tu", "WE": "We", "TH": "Th", "FR": "Fr", "SA": "Sa", "SU": "Su"}
    days = re.findall(r'BYDAY=([A-Z,]+)', rrule)
    if days:
        return ','.join(day_map[day] for day in days[0].split(','))
    return ""

def ical_to_osm(data):
    osm_formats = []

    for entry in data:
        rrule = entry.get('recurrence', '')
        start_time = entry.get('start_time', '')
        end_time = entry.get('end_time', '')
        exclude_holidays = entry.get('exclude_holidays', 0)

        days = rrule_to_osm_days(rrule)
        start_time_osm = convert_time_to_osm_format(start_time)
        end_time_osm = convert_time_to_osm_format(end_time)
        osm_format = ""

        if "FREQ=DAILY" in rrule:
            osm_format = "24/7"
        elif days:
            osm_format = f"{days} {start_time_osm}-{end_time_osm}"

        if exclude_holidays:
            osm_format += "; PH off"

        osm_formats.append(osm_format)
        
    if data[0].get('price') != None:
        return "; ".join(osm_formats), "; ".join(f'{entry["price"] / 100} {entry["currency"]}' for entry in data)
    else:
        return "; ".join(osm_formats)