from flask import Flask, render_template
from pyathena import connect
import pandas as pd

app = Flask(__name__)

@app.route('/')
def dashboard():

    conn = connect(
        s3_staging_dir='s3://bucket-lks2026/transactions-athena/',
        region_name='ap-southeast-1',
        schema_name='ecommers'
    )

    query = "SELECT * FROM transaction"

    df = pd.read_sql(query, conn)

    total_transaction = len(df)

    total_amount = 0

    if not df.empty:
        total_amount = df['amount'].sum()

    transaction = df.to_dict(orient='records')

    return render_template(
        "index.html",
        total_transaction=total_transaction,
        total_amount=total_amount,
        transaction=transaction
    )

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
