#! /usr/bin/env python3
# coding:utf-8

import time
from pymongo import MongoClient

def main():
    db = MongoClient().get_database('mumian')
    col = db.get_collection('articles')

    cursor = col.find({'status': 'fetched'})
    total = cursor.count()
    i = 1
    exist_emails = []
    for doc in cursor:
        contact = doc['contact']

        # email
        emails = contact.get('email')
        if emails:
            emails = [email.split()[0] for email in emails if email]
            remaining_emails = []
            for email in emails:
                if email in exist_emails:
                    continue
                else:
                    remaining_emails.append(email)
                    exist_emails.append(email)
        else:
            continue
        if remaining_emails:
            email_str = '/'.join(remaining_emails)
        else:
            continue

        # phone
        phones = contact.get('phone')
        if phones:
            phone_str = '/'.join(phones)
        else:
            phone_str = None

        # title
        title = doc['title'].replace(' ', '').replace('\n', ',').replace('\r', '')

        # publish_time
        publish_time = '20' + doc['publishTime']

        # href
        href = doc['href']

        data_str = '{}\t{}\t{}\t{}\n'.format(
            email_str, phone_str, publish_time, title
        )
        print(data_str)
        print('{} / {}, {:.2f}%'.format(i, total, 100*i/total))
        i += 1
        with open('./format_data.txt', 'a+') as f:
            f.write(data_str)

if __name__ == '__main__':
    main()
