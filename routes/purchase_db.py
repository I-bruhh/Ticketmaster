from flask import jsonify
import boto3

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the DynamoDB table name for Purchases
purchases_table_name = 'Purchases'

def get_all_purchases():
    try:
        # Access the DynamoDB table to list all purchases
        response = dynamodb.scan(
            TableName=purchases_table_name
        )
        items = response.get('Items', [])
        purchases = [dict((k, v['S']) for k, v in item.items()) for item in items]
        return jsonify(purchases)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_purchase(purchase_id):
    try:
        # Access the DynamoDB table to get a specific purchase by purchase_id
        response = dynamodb.get_item(
            TableName=purchases_table_name,
            Key={
                'purchase_id': {'N': str(purchase_id)}
            }
        )
        item = response.get('Item')
        if item:
            purchase = dict((k, v['S']) for k, v in item.items())
            return jsonify(purchase)
        else:
            return jsonify({'message': 'Purchase not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_purchase(purchase_data):
    try:
        # Add the purchase data to DynamoDB
        response = dynamodb.put_item(
            TableName=purchases_table_name,
            Item={k: {'S': str(v)} for k, v in purchase_data.items()}
        )
        return jsonify({'message': 'Purchase created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
