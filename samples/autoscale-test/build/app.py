from flask import Flask, request, jsonify, render_template
import psutil,os

app = Flask(__name__)

@app.route('/')
def index():
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    server_hostname = os.getenv('HOSTNAME', '알 수 없음')
    return render_template('index.html',ip_address=ip_address,server_hostname=server_hostname)

@app.route('/api/cpu')
def get_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    return jsonify(cpu_percent=cpu_percent)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
