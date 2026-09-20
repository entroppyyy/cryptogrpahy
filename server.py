import socket
import re
from data import PREFIX, SUFIX, CONTENT, PREFIX_FAKE, SUFIX_FAKE


HOST = "0.0.0.0"
PORT = 5500
SPACE_CODE = "SPC01"

alphabet = [
    "A", "B", "C", "Č", "Ć", "D", "Dž", "Đ", "E", "F",
    "G", "H", "I", "J", "K", "L", "Lj", "M", "N", "Nj",
    "O", "P", "R", "S", "Š", "T", "U", "V", "Z", "Ž"
]

decrypt_map = dict(zip(CONTENT, alphabet))
decrypt_map[SPACE_CODE] = " "

codes = sorted(decrypt_map.keys(), key=len, reverse=True)


def remove_ansi(text):
    return re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", text)


def is_fake(message):
    for prefix in PREFIX_FAKE:
        if not message.startswith(prefix):
            continue

        for suffix in SUFIX_FAKE:
            if message.endswith(suffix):
                return True

    return False


def get_real_content(message):
    for prefix in PREFIX:
        if not message.startswith(prefix):
            continue

        for suffix in SUFIX:
            if not message.endswith(suffix):
                continue

        start = len(prefix)
        end = len(message) - len(suffix)

        if end >= start:
            return message[start:end]

    return None


def decrypt(text):
    result = []
    position = 0

    while position < len(text):
        for code in codes:
            if text.startswith(code, position):
                result.append(decrypt_map[code])
                position += len(code)
                break
        else:
            result.append(text[position])
            position += 1

    return "".join(result)


def process_message(message):
    message = remove_ansi(message)

    if is_fake(message):
        return

    encrypted = get_real_content(message)

    if encrypted is None:
        return

    clean_message = decrypt(encrypted)

    print(f"REAL: {clean_message}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)

print(f"{HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"conn: {addr}")

    with conn:
        buffer = b""

        while True:
            data = conn.recv(4096)

            if not data:
                break

            buffer += data

            while b"\n" in buffer:
                raw_message, buffer = buffer.split(b"\n", 1)

                if not raw_message:
                    continue

                message = raw_message.decode(
                    "utf-8",
                    errors="replace"
                )

                process_message(message)

    print(f"deconn: {addr}")
