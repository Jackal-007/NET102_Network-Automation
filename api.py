from flask import Flask, render_template, jsonify, request
from flask_cors import CORS  # <--- THIS MUST BE HERE
from netmiko import ConnectHandler

app = Flask(__name__)
CORS(app)  # <--- THIS MUST BE HERE

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/api/run-commands', methods=['POST'])
def run_commands():
    router_device = {
        'device_type': 'cisco_ios_telnet',
        'host': '192.168.10.41',  # <--- Make sure this is HOST, not IP
        'port': 32770,
        'username': 'admin',
        'password': 'eve123',
        'secret': 'eve123',
    }

    commands_to_run = [
        "show version",
        "show ip interface brief",
        "show running-config"
    ]

    try:
        net_connect = ConnectHandler(**router_device)
        net_connect.enable()

        results = {}
        for cmd in commands_to_run:
            results[cmd] = net_connect.send_command(cmd)

        net_connect.disconnect()
        return jsonify({"success": True, "results": results})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)