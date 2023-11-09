import boto3
from flask import jsonify

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the DynamoDB table name for the User model
user_table_name = 'User'

def get_user_by_username(username):
    try:
        response = dynamodb.get_item(
            TableName=user_table_name,
            Key={'username': {'S': username}
                 }
        )
        item = response.get('Item')
        if item:
            user = dict((k, v['S']) for k, v in item.items())
            return jsonify(user), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def create_user(user_data):
    try:
        dynamodb.put_item(
            TableName=user_table_name,
            Item={k: {'S': str(v)} for k, v in user_data.items()}
        )
        return jsonify({'message': 'User created successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add more authentication-related routes
