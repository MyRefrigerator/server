#!/usr/bin/env python3

import sys
import email
import re

name_map = {
    'root': 'unchaptered',
}

email_map = {
   'root@ip-172-31-3-247.ap-northeast-2.compute.internal': 'workstation19961002@gmail.com',
}

def fixup(name, email_address):
    new_name = name_map.get(name)
    new_email = email_map.get(email_address)

    if new_name is None and new_email is None:
        return None
    else:
        return new_name or name, new_email or email_address

def fix_name_email(line):
    decoded = line.decode('utf-8')
    match = re.match('^(author|committer|tagger) (.*) <(.*)>', decoded)
    if not match:
        return line

    old_name old_email = match.group(2), match.group(3)
    new = fixup(old_name, old_email)
    if not new:
        return line

    new_name, new_email = new
    replacement = f"{match.group(1)} {new_name} <{new_email}>"

    return decoded.replace(f"{match.group(1)} {old_name} <{old_email}>", replacement).encode('utf-8')

for line in sys.stdin.buffer:
    sys.stdout.buffer.write(fix_name_email(line))
