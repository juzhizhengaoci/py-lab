"""webserver1.py 的自测脚本。

用 subprocess 在 127.0.0.1:8899 启动服务器，再用 socket 发一个
真正的 HTTP 请求（GET /），断言返回 200 和 Hello, World!。
成功退出码为 0，失败为非 0。

用法：python toy-webserver/selftest.py
"""

import socket
import subprocess
import sys
import time
from pathlib import Path

HOST = '127.0.0.1'
PORT = 8899
SERVER = Path(__file__).with_name('webserver1.py')
STARTUP_TIMEOUT = 10.0
READ_TIMEOUT = 5.0


def ensure_port_available():
    """先确认 8899 没被别的程序占着，否则测到的可能不是我们起的服务器。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            probe.bind((HOST, PORT))
        except OSError as exc:
            raise RuntimeError(f'{HOST}:{PORT} is not available: {exc}') from exc


def fetch_root():
    """向服务器发 GET /，返回完整响应字节。"""
    request = (
        f'GET / HTTP/1.1\r\n'
        f'Host: {HOST}:{PORT}\r\n'
        f'Connection: close\r\n'
        f'\r\n'
    ).encode('ascii')
    with socket.create_connection((HOST, PORT), timeout=READ_TIMEOUT) as sock:
        sock.sendall(request)
        chunks = []
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            chunks.append(chunk)
    return b''.join(chunks)


def fetch_when_ready(process):
    """等服务器开始监听后再请求，避免服务器还没 bind 好就连接失败。"""
    deadline = time.monotonic() + STARTUP_TIMEOUT
    last_error = None
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError('server exited before accepting a connection')
        try:
            return fetch_root()
        except (ConnectionRefusedError, TimeoutError) as exc:
            last_error = exc
            time.sleep(0.05)
    raise TimeoutError(f'server not ready within {STARTUP_TIMEOUT:.0f}s: {last_error}')


def stop(process):
    """结束子进程，返回它已输出的内容（失败时用于打印现场）。"""
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
    return process.stdout.read() if process.stdout else b''


def main():
    try:
        ensure_port_available()
    except Exception as exc:
        print(f'FAILED: {exc}', file=sys.stderr)
        return 1

    process = subprocess.Popen(
        [sys.executable, str(SERVER), '--host', HOST, '--port', str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    try:
        raw = fetch_when_ready(process)
    except Exception as exc:
        output = stop(process)
        print(f'FAILED: {exc}', file=sys.stderr)
        if output:
            print(output.decode('utf-8', errors='replace'), file=sys.stderr)
        return 1

    stop(process)

    status_line, separator, body = raw.partition(b'\r\n\r\n')
    if not separator:
        print(f'FAILED: response has no header/body separator: {raw!r}', file=sys.stderr)
        return 1
    if status_line.split(b'\r\n')[0] != b'HTTP/1.1 200 OK':
        print(f'FAILED: unexpected status line: {status_line!r}', file=sys.stderr)
        return 1
    if body != b'Hello, World!':
        print(f'FAILED: unexpected body: {body!r}', file=sys.stderr)
        return 1

    print(f'OK: GET http://{HOST}:{PORT}/ -> 200 Hello, World!')
    return 0


if __name__ == '__main__':
    sys.exit(main())
