import sys
import re

image_regex = re.compile(r'\.(png|jpg|gif|ico)$', re.IGNORECASE)
video_regex = re.compile(r'\.(mp4|flv)$', re.IGNORECASE)
audio_regex = re.compile(r'\.(mp3)$', re.IGNORECASE)
web_regex = re.compile(r'\.(html|css|js|php)$', re.IGNORECASE)

for line in sys.stdin:
    fields = line.strip().split()

    resource = fields[6]
    res_size = fields[9]

    if res_size == '-':
        res_size='0'

    try:
        if image_regex.search(resource):
            print("img\t%s" % (res_size))
        elif video_regex.search(resource):
            print("vid\t%s" % (res_size))
        elif audio_regex.search(resource):
            print("aud\t%s" % (res_size))
        elif web_regex.search(resource):
            print("web\t%s" % (res_size))
    except Exception as e:
        # Catch any exceptions that occur while searching for pattern and continue to the next iteration
        continue

