#! /usr/bin/env python3
from datetime import datetime
import re
from message import Message


def get_raw_messages():
    '''Separates a txt.gz archive into a list of raw messages'''
    archive_path = '/home/lloyd/Documents/github/mailing_database/archives/therapy/2017-March.txt.gz'
    with open(archive_path, 'rb') as f:
        file_content = f.readlines()
        # split file into messages
        list_name = 'therapy'
        domain = 'lists.olin.edu'
        new_message_pattern = re.compile(
            'From %s at %s  (.*)' % (list_name, domain))
        raw_messages = []
        raw_message = ''
        for raw_line in file_content:
            line = raw_line.decode('utf-8')  # get out of byte literals
            if new_message_pattern.match(line):
                if raw_message != '':
                    raw_messages.append(raw_message)
                raw_message = line
            else:
                raw_message += line
    return raw_messages


def process_raw_message(raw_message, remove_quoted_emails=True):
    '''Returns a message object from raw emails'''
    patterns = {
        'subject': '^Subject: (.*)\n',
        'message_id': '^Message-ID: (.*)\n',
        'send_datetime': '^From therapy at lists.olin.edu  (.*)\n',
        'content': '^Message-ID: .*\n\n([\s\S]*)'
    }
    message_values = {}
    message_values['raw_message'] = str(raw_message)
    for key, pattern in patterns.items():
        pattern_match = re.search(pattern, raw_message, re.MULTILINE)
        if pattern_match:
            pattern_group = pattern_match.group(1)
        else:
            print('%s not found' % key)
            pattern_group = None

        # special cases
        if key == 'send_datetime':
            datetime_format = '%a %b  %d %H:%M:%S %Y'
            corrected_datetime = datetime.strptime(
                pattern_group, datetime_format)
            message_values[key] = corrected_datetime
        elif key == 'content' and remove_quoted_emails:
            quote_stripped_group = pattern_group
            quote_patterns = {
                'Original Message': '^-+Original Message-+\n',
                'On_,_wrote': '^On [^,\n]*, .*\n{0,1}.* wrote:\n',
                '> On_,_wrote': '^> On [^,\n]*, .*\n{0,1}.* wrote:\n',
                'From_Sent_Subject_To_': '^From: (.*)\nSent: (.*)\nSubject: (.*)\nTo: (.*)\n',
                '_': '^_+\n',
            }
            for quote_key, quote_pattern in quote_patterns.items():
                quote_pattern_match = re.search(quote_pattern, pattern_group, re.MULTILINE)
                if quote_pattern_match:
                    print('Found "{}" quote pattern.'.format(quote_key))
                    print(quote_pattern_match.group())
                    quote_stripped_group = pattern_group[:quote_pattern_match.start()]
            message_values[key] = quote_stripped_group.strip('\n')
        elif key == 'content':
            message_values[key] = pattern_group.strip('\n')
        else:
            message_values[key] = pattern_group
    # save to message object
    return Message(**message_values)


def process_raw_messages(raw_messages):
    '''Return a list of message objects'''
    return [process_raw_message(msg) for msg in raw_messages]


test_msg = '''
From therapy at lists.olin.edu  Wed Mar  1 14:24:41 2017
From: therapy at lists.olin.edu (Anonymous rants and raves.)
Date: Wed, 1 Mar 2017 19:24:41 +0000
Subject: [Therapy] Mistake
In-Reply-To: <mailman.219.1488396127.1623.therapy@lists.olin.edu>
References: <mailman.214.1488394958.1623.therapy@lists.olin.edu>
	<mailman.218.1488395986.1623.therapy@lists.olin.edu>
	<mailman.219.1488396127.1623.therapy@lists.olin.edu>
Message-ID: <mailman.220.1488396294.1623.therapy@lists.olin.edu>

Yo knobheads, this conversation is only going to get dangerously close to
naming names. Stop.

On Wed, Mar 1, 2017 at 2:22 PM Anonymous rants and raves. <
therapy at lists.olin.edu> wrote:

> Ooh, lets guess! Okay, going off of subtext, I'm assuming yuuuge is a
> Trump reference. So did the mistake person get into a political argument
> with OP in which they were very much pro Trump? Thoughts?
> -----Original Message-----
> From: Therapy [mailto:therapy-bounces at lists.olin.edu] On Behalf Of
> Anonymous rants and raves.
> Sent: Wednesday, March 1, 2017 2:20 PM
> To: Anonymous rants and raves. <therapy at lists.olin.edu>
> Subject: Re: [Therapy] Mistake
>
> Dear Therapy,
>
> I want to write a nasty anonymous email complaining about a single person.
> I can't name names on Therapy, because it is against the rules. Because I
> am a little bitch, my solution is to write my nasty email anyways, and
> instead of actually naming the person in question, just give vague hints.
> This will satisfy my desperate need to whine, while also inspiring
> everyone else to try and guess who I meant.
>
> Sincerely,
> Anonymous Douchecanoe
>
> On Wed, Mar 1, 2017 at 2:02 PM Anonymous rants and raves. <
> therapy at lists.olin.edu> wrote:
>
> > One of the class of 2017 was a yuuuge mistake by Olin admissions
> >
>
'''
print(process_raw_message(test_msg))
# test = get_raw_messages()
# print(process_raw_message(test[0]),)
# print(*process_raw_messages(test), sep='\n')
