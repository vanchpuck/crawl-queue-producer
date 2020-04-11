import boto3
import json
import argparse

QUEUE_URL = "queueUrl"
BUCKET = "bucket"
KEY = "key"
TYPE = "type"


def lambda_handler(event, context):
    sqs = boto3.client('sqs')
    s3 = boto3.client('s3')
    key = event[KEY]
    s3.download_file(event[BUCKET], key, '/tmp/'+key)
    with open('/tmp/'+key, 'r') as f:
        for row in f.read().splitlines():
            record = json.dumps({"url": row, "urlType": event[TYPE]})
            print("Sending to sqs: " + record)
            msg = sqs.send_message(
                QueueUrl=event[QUEUE_URL],
                MessageBody=record
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(QUEUE_URL)
    parser.add_argument(BUCKET)
    parser.add_argument(KEY)
    parser.add_argument(TYPE)
    args = parser.parse_args()
    lambda_handler({QUEUE_URL: args.queueUrl, BUCKET: args.bucket, KEY: args.key, TYPE: args.type}, None)


if __name__ == "__main__":
    main()
