# listenbrainz-weekly-tops_over_time
A python script to get your top weekly artist from a specified time period
## Dependencies
- Python 3.7 >
- [liblistenbrainz](https://github.com/metabrainz/liblistenbrainz)
## Usage
```
$ python listenbrainz-weekly-tops.py -h
usage: listenbrainz-weekly-tops [-h] --token TOKEN --username USERNAME [--top_x TOPX] [--start_date STARTDATE] [--end_date ENDDATE]

options:
  -h, --help            show this help message and exit
  --token TOKEN         listenbrainz user token token (get yours from https://listenbrainz.org/profile/)
  --username USERNAME   the username of the user whose data you'd like to fetch
  --top_x TOPX          Top X Artists in week. Default is 1
  --start_date STARTDATE the ISO date (dd-mm-yyyy) to start from. Will "round" to closest start of week. Defaults to a year ago
  --end_date ENDDATE    the ISO date (dd-mm-yyyy) to end at. Will "round" to closest end of week. Defaults to now
```
You can get your listenbrainz token from [here](https://listenbrainz.org/profile)