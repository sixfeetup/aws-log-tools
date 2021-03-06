#!/usr/bin/env python3
import argparse
import gzip

import boto3
import arrow
import click
from clint.textui import colored, columns, puts, prompt
from cloudfront_log_parser import parse

#boto3.set_stream_logger('botocore', level='DEBUG')


@click.command()
@click.option('--profile', '-p', default="default")
@click.option('--bucket', '-b', required=True)
@click.option('--distribution', required=True)
@click.option('--prefix', default="prod-cf-logs")
@click.option('--year', prompt=True)
@click.option('--month', prompt=True)
@click.option('--day', prompt=True)
@click.version_option()
def opencfl_log(profile, bucket, distribution, prefix, year, month, day):
    session = boto3.Session(profile_name=profile)
    s3_client = session.client('s3')
    # create a prefix based on distribution, year and month
    prefix = prefix + '/' + distribution
    if year:
        prefix += '.' + str(year)
    if month:
        prefix += '-' + str(month)
    if day:
        prefix += '-' + str(day)
    files = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    options = [k['Key'] for k in files['Contents']]
    try:
        filename = prompt.options('Pick log to view', [o.split('/')[1] for o in options])
    except KeyboardInterrupt:
        quit(0)
    s3obj = s3_client.get_object(Bucket=bucket, Key=options[filename-1])
    with gzip.open(s3obj['Body'], 'rt') as f:
        responses = parse(f.readlines())
        puts(
            columns(
                [colored.yellow('method'), 6],
                [colored.yellow('status'), 6],
                [colored.yellow('result'), 10],
                [colored.yellow('timestamp'), 20],
                [colored.yellow('request_id'), 56],
                [colored.yellow('path'), None],
            )
        )
        for r in responses:
            puts(
                columns(
                    [colored.green(r.http_method), 6],
                    [colored.red(r.status_code), 6],
                    [colored.red(r.edge_result_type), 10],
                    [colored.cyan(arrow.get(r.timestamp).to('US/Eastern').humanize()), 20],
                    [colored.yellow(r.request_id), 56],
                    [colored.blue(r.path), None],
                )
            )


if __name__ == '__main__':
    opencfl_log()
