from data import PREFIX, SUFIX, CONTENT, PREFIX_FAKE, SUFIX_FAKE
import requests
import random
import socket
from colorama import Fore, Back, Style


class Main:
    def main(self, username, ip, message):
        self.username = username
        self.ip = ip
        self.message = message
        self.crypto_section()

    def crypto_section(self):
        url = "https://www.pickrandom.app/api/v1/word"
        message_length = len(self.message.split())
        signal = random.randint(0, 6)

        alphabet = [
            "A", "B", "C", "Č", "Ć", "D", "Dž", "Đ", "E", "F",
            "G", "H", "I", "J", "K", "L", "Lj", "M", "N", "Nj",
            "O", "P", "R", "S", "Š", "T", "U", "V", "Z", "Ž"
        ]

        crypto_map = dict(zip(alphabet, CONTENT))
        crypto_map[" "] = "SPC01"

        prefix = random.choice(PREFIX)
        sufix = random.choice(SUFIX)
        prefix_fake = random.choice(PREFIX_FAKE)
        sufix_fake = random.choice(SUFIX_FAKE)

        content = []

        def encrypt(text):
            return "".join(crypto_map.get(char, char) for char in text.upper())

        for j in range(7):
            if signal == j:
                encrypted = encrypt(self.message)

                real_content = (
                    f"{prefix}"
                    f"{Back.RED}{Fore.WHITE}"
                    f"{encrypted}"
                    f"{Style.RESET_ALL}"
                    f"{sufix}"
                )

                content.append(real_content)

            fake_info = ""

            for _ in range(message_length):
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    word = response.json()["results"][0]
                    fake_info += f" {word}"
                except Exception:
                    fake_info += " random"

            fake_content = (
                f"{prefix_fake}"
                f"{encrypt(fake_info)}"
                f"{sufix_fake}"
            )

            content.append(fake_content)

        server_ip = "127.0.0.1"
        port = 5500

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            print(f"\n{Fore.GREEN}Connecting to {server_ip}:{port}...{Style.RESET_ALL}")
            client.connect((server_ip, port))
            print(f"{Fore.GREEN}Connected.{Style.RESET_ALL}\n")

            for message in content:
                print(f"{Fore.WHITE}{message}{Style.RESET_ALL}")
                client.sendall(message.encode("utf-8") + b"\n")

            print(f"\n{Fore.GREEN}Messages sent.{Style.RESET_ALL}")

        except ConnectionRefusedError:
            print(f"{Fore.RED}Connection refused.{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

        finally:
            client.close()
            print(f"{Fore.YELLOW}Connection closed.{Style.RESET_ALL}")


if __name__ == "__main__":
    app = Main()
    app.main(
        "Penis",
        "192.168.1.10",
        "content"
    )
