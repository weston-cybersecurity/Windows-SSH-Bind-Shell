# Windows-SSH-Bind-Shell
A secure Windows bind shell implemented in Python using Paramiko (SSHv2) for encrypted communication.


## How to using

When connecting for the first time, you will be asked to trust the RSA key. Follow the prompts to enter your username and password:

Default Username: windows-bind-shell


Default Password: windows-bind-shell (It's not will show you anything, like enter password to the Kali Linux)
<img width="1517" height="745" alt="螢幕擷取畫面 2026-05-13 125146" src="https://github.com/user-attachments/assets/b73a6d56-c508-4f6d-984a-48035b4db35a" />

<img width="1517" height="745" alt="螢幕擷取畫面 2026-05-13 125317" src="https://github.com/user-attachments/assets/34e0c549-e518-465f-8152-d4b11f7a3f55" />

<img width="1517" height="745" alt="螢幕擷取畫面 2026-05-13 125423" src="https://github.com/user-attachments/assets/d55970c7-4cca-4781-8426-cf95f54da2c7" />

## 🔒 All traffic is encrypted using SSHv2

As shown in the Wireshark capture below, all communication between the client and server is encapsulated within the SSHv2 protocol. Any attempt to sniff the network will only yield encrypted packets, ensuring that sensitive commands and data remain confidential.
<img width="1517" height="745" alt="螢幕擷取畫面 2026-05-13 125517" src="https://github.com/user-attachments/assets/6f4dbfbb-3998-47f8-a0a2-e97bf42b8679" />
