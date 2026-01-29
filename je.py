import socket, json, time
import numpy as np

MAC_IP = "192.168.100.80"   # 改成你的 Mac IP
MAC_PORT = 5006
JETSON_PORT = 5005

sock_rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_rx.bind(("0.0.0.0", JETSON_PORT))

sock_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 示例控制器（你后面换成自己的）
Kp, Kd = 2.0, 0.8

print("[Jetson] controller listening on", JETSON_PORT)

while True:
    data, addr = sock_rx.recvfrom(65535)
    msg = json.loads(data.decode())

    seq = msg["seq"]
    x = np.array(msg["x"], dtype=float)  # 例如 x=[x1,x2,...]
    t_sent = msg["t"]

    # ---- 控制律示例：u = -Kp*x1 - Kd*x2 ----
    x1, x2 = x[0], x[1]
    u = np.array([-Kp*x1 - Kd*x2], dtype=float)

    reply = {
        "seq": seq,
        "u": u.tolist(),
        "t": time.time(),      # Jetson发送时间
        "t_sent": t_sent       # 原始状态发送时间（方便算延迟）
    }
    sock_tx.sendto(json.dumps(reply).encode(), (MAC_IP, MAC_PORT))

    print(f"[Jetson] seq={seq} x={x} -> u={u}")
