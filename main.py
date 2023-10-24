from flask import Flask, jsonify
from ticketFairnessDistributionAlgoPlusBlockchain import blockchain  # Import your existing blockchain code

app = Flask(__name__)

@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    blockchain_data = []

    for block in blockchain.chain:
        block_data = {
            'index': block.index,
            'timestamp': block.timestamp,
            'data': block.data,
            'previous_hash': block.previous_hash,
            'hash': block.hash
        }
        blockchain_data.append(block_data)

    return jsonify(blockchain_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the Flask web service on port 5000
