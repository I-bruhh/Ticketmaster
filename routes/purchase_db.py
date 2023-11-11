from flask import jsonify
import boto3

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the DynamoDB table name for Purchases
PURCHASES_TABLE_NAME = 'Purchase'
CONCERTS_TABLE_NAME = 'Purchase'


def get_all_purchases():
    try:
        # Access the DynamoDB table to list all purchases
        response = dynamodb.scan(
            TableName = PURCHASES_TABLE_NAME
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
            TableName = PURCHASES_TABLE_NAME,
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
        print('testing...')
        formatted_item = None
        # Add the purchase data to DynamoDB
        response = dynamodb.put_item(
            TableName=PURCHASES_TABLE_NAME,
            Item={k: {'S': str(v)} for k, v in purchase_data.items()}
        )

        # Update the remaining tickets for the corresponding concert
        concert_id = purchase_data.get('concert_id')
        quantity = int(purchase_data.get('quantity'))

        print('testing...')

        # Retrieve the current ticket count for the concert
        response = dynamodb.get_item(
            TableName=CONCERTS_TABLE_NAME,
            Key={
                'concert_id': {'N': str(concert_id)}
            }
        )
        item = response.get('Item')
        if item:
            formatted_item = {
                "concert_id": item["concert_id"]["N"],
                "name": item["name"]["S"],
                "dates": [date["S"] for date in item["dates"]["L"]],
                "venues": [venue["S"] for venue in item["venues"]["L"]],
                "categories": [int(category["N"]) for category in item["categories"]["L"]],
                "start_ticket_sale": item["start_ticket_sale"]["S"],
                "end_ticket_sale": item["end_ticket_sale"]["S"],
                "limit_per_person": int(item["limit_per_person"]["N"]),
                "available_tickets_for_sale": int(item["total_tickets_for_sale"]["N"]),
            }

        current_tickets = int(formatted_item['total_tickets_for_sale'])
        remaining_tickets = current_tickets - quantity

        print('testing...')

        # Update the concert with the new remaining ticket count
        dynamodb.update_item(
            TableName=CONCERTS_TABLE_NAME,
            Key={
                'concert_id': {'N': str(concert_id)}
            },
            ExpressionAttributeValues={
                ':available_tickets_for_sale': {'N': str(remaining_tickets)}
            }
        )

        return jsonify({'message': 'Purchase created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
