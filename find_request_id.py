#!/usr/bin/env python3
import argparse
import gzip

import boto3
from clint import arguments
from clint.textui import colored, columns, puts, prompt
from cloudfront_log_parser import parse


def find_request_id(profile, bucket, request_id):
    # pick a file to inspect
    session = boto3.Session(profile_name=profile)
    s3_client = session.client('s3')
    files = s3_client.list_objects_v2(Bucket=bucket, Prefix='cloudfront-log')
    args = arguments.Args()
    logs = [k['Key'] for k in files['Contents']]
    logs.reverse()
    for log in logs:
        s3obj = s3_client.get_object(Bucket=bucket, Key=log)
        with gzip.open(s3obj['Body'], 'rt') as f:
            responses = parse(f.readlines())
            for r in responses:
                if r.request_id == request_id:
                    puts("Found!")
                    puts(
                        columns(
                            [colored.green(r.http_method), 6],
                            [colored.red(r.status_code), 6],
                            [colored.red(r.edge_result_type), 10],
                            [colored.yellow(r.request_id), 56],
                            [colored.magenta(str(r.timestamp)), 20],
                            [colored.blue(r.path), None],
                        )
                    )
                    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', '-p', action='store', default="default")
    parser.add_argument('--bucket', '-b', action='store', required=True)
    parser.add_argument('request_id', action='store',
                       help='request-id to search the logs for')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()
    find_request_id(args.profile, args.bucket, args.request_id)
