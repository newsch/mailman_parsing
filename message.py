#! /usr/bin/env python3
# from datetime import datetime


class Message:
    def __init__(self,
                 subject,
                 message_id,
                 send_datetime,
                 content,
                 raw_message):
        self.subject = subject
        self.message_id = message_id
        self.send_datetime = send_datetime
        self.content = content
        self.raw_message = raw_message
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def __str__(self):
        return ('ID: {message_id}\n'
                'Subject "{subject}" on {formatted_datetime}\n'
                '{content}\n'
                'EOM\n'
                ).format(**{'formatted_datetime':
                            self.send_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                            **self.__dict__})
