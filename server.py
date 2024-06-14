from flask import Flask, request, jsonify
import json
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed

app = Flask(__name__)
data_file = 'data.json'
webhook_url = 'https://discordapp.com/api/webhooks/1251115853416632363/HNAJHN3zBD7MZ1PyZHXDjadwxWzfqGOVckLJP8VINF4EEyoXHbOVUCYTO32OgTuCN51n'

# Load data from JSON file
def load_data():
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save data to JSON file
def save_data(data):
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

# Function to send embedded message to Discord
def send_embedded_message(username, title, description, fields, color):
    webhook = DiscordWebhook(url=webhook_url)
    embed = DiscordEmbed(title=title, description=description, color=color)
    embed.set_author(name=username)
    embed.set_footer(text='Earnings Logger')
    embed.set_timestamp()
    for name, value, inline in fields:
        embed.add_embed_field(name=name, value=value, inline=inline)
    webhook.add_embed(embed)
    response = webhook.execute()
    return response

@app.route('/add_user', methods=['POST'])
def add_user():
    data = load_data()
    user_id = request.json.get('user_id')
    if user_id in data:
        return jsonify({'message': 'User already exists'}), 400
    data[user_id] = {'earnings': 0}
    save_data(data)
    return jsonify({'message': 'User added successfully'}), 200

@app.route('/add_username', methods=['POST'])
def add_username():
    data = load_data()
    user_id = request.json.get('username')
    if user_id in data:
        return jsonify({'message': 'Username already exists'}), 400
    data[user_id] = {'earnings': 0}
    save_data(data)
    return jsonify({'message': 'Username added successfully'}), 200

@app.route('/modify_earnings', methods=['POST'])
def modify_earnings():
    data = load_data()
    user_id = request.json.get('user_id')
    amount = request.json.get('amount')
    if user_id not in data:
        return jsonify({'message': 'User not found'}), 404
    data[user_id]['earnings'] += amount
    save_data(data)
    return jsonify({'message': 'Earnings updated successfully'}), 200

@app.route('/cashout', methods=['POST'])
def cashout():
    data = load_data()
    user_id = request.json.get('user_id')
    if user_id not in data:
        return jsonify({'message': 'User not found'}), 404
    earnings = data[user_id]['earnings']
    if earnings <= 0:
        return jsonify({'message': 'No earnings to cashout'}), 400
    data[user_id]['earnings'] = 0
    save_data(data)
    fields = [
        ('User ID', user_id, False),
        ('User ID', user_id, False),
        ('Amount', f'${earnings}', False),
        ('Status', 'Successful', True)
    ]
    send_embedded_message('Earnings Bot', 'Cashout Notification', 'A user has cashed out!', fields, 0x00ff00)
    return jsonify({'message': 'Cashout successful'}), 200

@app.route('/get_earnings', methods=['GET'])
def get_earnings():
    data = load_data()
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True)
