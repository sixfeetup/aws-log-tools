# AWS Log Tools

Tools for dealing with AWS logs like CloudFront

## Getting Started

1. Create and activate a fresh `virtualenv` using Python 3.6
1. `pip install -r requirements.txt`

## The Scripts

### opencfl.py

```console
$  python opencfl.py -h
usage: opencfl.py [-h] [--profile PROFILE] --bucket BUCKET [--version]

optional arguments:
  -h, --help            show this help message and exit
  --profile PROFILE, -p PROFILE
  --bucket BUCKET, -b BUCKET
  --version             show program's version number and exit
```

This only requires the name of the bucket that you have enabled for CloudFront logging. It will give you a nice menu to pick the most recent logs and then displays a subset of the entries from each request in beautiful colorized text.

### find_request_id.py

```console
$ python find_request_id.py
usage: find_request_id.py [-h] [--profile PROFILE] --bucket BUCKET [--version]
                          request_id
find_request_id.py: error: the following arguments are required: --bucket/-b, request_id
```

Given a specific `request-id` and `bucket`, it will search them for the entry that matches and display a summary of that request as CloudFront saw it.
