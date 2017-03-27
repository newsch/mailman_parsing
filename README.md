# Mailman Archive Parsing

## Notes
### General
- txtgz archives downloaded with [philgyford/mailman-archive-scraper](https://github.com/philgyford/mailman-archive-scraper)
- format of archives is called mbox. Python module for these [here](https://docs.python.org/3.5/library/mailbox.html#mailbox.Message). This should be used instead of regex-ing everything.
- In-Reply-To and other headers are part of the [RFC 2822 standard](https://tools.ietf.org/html/rfc2822.html)
- Message-ID is explained more ^
- very helpful regex tool: <http://regexr.com/>

### Issues
- Current method of assigning parents and children doesn't work - some messages are assigned as children of multiple others that they definitely aren't. This may be related to the message-id problem.
- Some In-Reply-To IDs don't seem to match any Message-IDs - more research will have to be done.
  ```
  Subject: [Therapy] Mistake
  In-Reply-To: <d90bee34749c406c99ec65fd5943f6fd@EX03.olin.edu>
  References: <mailman.214.1488394958.1623.therapy@lists.olin.edu>
  	<d90bee34749c406c99ec65fd5943f6fd@EX03.olin.edu>
  Message-ID: <mailman.216.1488395441.1623.therapy@lists.olin.edu>
  ```
