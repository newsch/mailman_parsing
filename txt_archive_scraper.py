#! /usr/bin/env python3
from datetime import datetime
import re
from message import Message


def get_raw_messages(archive_path='sample_thread_text.txt'):
    '''Separates a txt.gz archive into a list of raw messages'''
    with open(archive_path, 'rb') as f:
        file_content = f.readlines()
        # split file into messages
        list_name = 'therapy'
        domain = 'lists.olin.edu'
        new_message_pattern = re.compile(
            '^From %s at %s  (.*)' % (list_name, domain), re.MULTILINE)  # apparently this should work with only '^From (.*)\n' or something similar
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
                'Original Message': '^-+ *Original Message *-+\n',
                '  >> Original Message': '^    >> \n    >> -+Original Message-+\n',
                'On_,_wrote': '^On [^,\n]*, .*\n{0,1}.*wrote:\n',
                '> On_,_wrote': '^> On [^,\n]*, .*\n{0,1}.* wrote:\n',
                'From_Sent_Subject_To_': '^From: (.*)\nSent: (.*)\nSubject: (.*)\nTo: (.*)\n',
                '_': '^_+\n',
                # '>': '^\s*>+\s*.*\n'
            }
            for quote_key, quote_pattern in quote_patterns.items():
                quote_pattern_match = re.search(quote_pattern, pattern_group, re.MULTILINE | re.IGNORECASE)
                if quote_pattern_match:
                    print('Found "{}" quote pattern.'.format(quote_key))
                    print(quote_pattern_match.group())
                    quote_stripped_group = quote_stripped_group[:quote_pattern_match.start()]
            message_values[key] = quote_stripped_group.strip('\n')
        elif key == 'content':
            message_values[key] = pattern_group.strip('\n')
        else:
            message_values[key] = pattern_group
    # save to message object
    # check values
    content_check_patterns = {
        'is only whitespace': re.compile('\s+'),
        'contains >': re.compile('[\s\S]*^\s*>+[\s\S]*'),
    }
    for content_check_type, content_check_pattern in content_check_patterns.items():
        if content_check_pattern.match(message_values['content']):
            print('warning: message {} content {}').format(message_values['message_id'], content_check_type)
    return Message(**message_values)


def process_raw_messages(raw_messages):
    '''Return a list of message objects'''
    return [process_raw_message(msg) for msg in raw_messages]


def link_messages(messages):
    '''set parents and children of messages for a list of messages'''
    # set parents based on In-Reply-To: field
    reply_to_pattern = re.compile('^In-Reply-To: (.*)\n', re.MULTILINE)
    for message in messages:
        reply_to_match = reply_to_pattern.search(message.raw_message)
        if reply_to_match:
            reply_id = reply_to_match.group(1)
            if reply_id != message.message_id:
                for potential_parent in messages:
                    if potential_parent.message_id == reply_id:
                        message.add_parent(potential_parent)
                        print('Found parent {} for message {}'.format(potential_parent.message_id, message.message_id))
                        potential_parent.add_child(message)
        else:
            print('No "In-Reply-To" field found for message ' + message.message_id)
    print('Finished finding parents')
    # set children based on new parents
    # for message in messages:
    #     if message.parent and message not in message.parent.children:
    #         message.parent.add_child(message)
    #         print('Added child {} to message {}'.format(message.message_id, message.parent.message_id))


# test = get_raw_messages()
# # print(process_raw_message(test[0]),)
# print(*process_raw_messages(test), sep='\n')

test_messages = process_raw_messages(get_raw_messages(archive_path='sample_thread_text_2.txt'))
link_messages(test_messages)
# test_message = test_messages[1]
for test_message in test_messages:
    print('MESSAGE: {}PARENT: {}CHILDREN:\n{}'.format(test_message, test_message.parent, (*test_message.children)))
# test_messages[8].get_thread()
