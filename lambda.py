import json
import uuid
import boto3
from datetime import datetime

s3 = boto3.client('s3')
sns = boto3.client('sns')
bucket_name = "bucket-lks2026"
SNS_ARN = "arn:aws:sns:ap-southeast-1:363852138648:Transaction-allert"
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('transactions')

def lambda_handler(event, context):
    body = event
    if "body" in event:
        if isinstance(event['body'], str):
            body = json.loads(event['body'])
        else:
            body = event['body']

    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "amount": body["amount"],
        "item": body['item'],
        "currency": body["currency"],
        "customer": body["customer"],
        "payment_method": body["payment_method"],
        "timestamp": datetime.now().isoformat(),
        "status": "completed"
    }

    table.put_item(Item=transaction)

    filename = f"transactions-athena/{transaction['transaction_id']}.json"
    print(f"Uploading transaction {transaction['transaction_id']} to {filename}")

    s3.put_object(
            Bucket=bucket_name,
            Key=filename,
            Body=json.dumps(transaction),
            ContentType='application/json'
        )

    try:
        print(f"Transaksi berhasil dengan Nama pelanggan {transaction['customer']}\nMembeli {transaction['item']}\nDengan harga {transaction['amount']}\nDengan metode pembayaran {transaction['payment_method']}\nDan menggunakan Mata uang {transaction['currency']}")
        sns.publish(
            TopicArn=SNS_ARN,
            Message=f"Transaksi berhasil dengan Nama pelanggan {transaction['customer']}\nMembeli {transaction['item']}\nDengan harga {transaction['amount']}\nDengan metode pembayaran {transaction['payment_method']}\nDan menggunakan Mata uang {transaction['currency']}",
            Subject="Berhasil Transaksi"
        )
        print("Transaksi Berhasil")
    except Exception as e:
        print(f"Error sending SNS notification: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Transaksi Berhasil',
            'transaction': transaction
        })
    }
