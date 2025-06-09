from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
from zenutils.sixutils import *
__all__ = ['get_current_thread_id', 'get_worker_id', 'get_random_script_name', 'execute_script', 'default_timeout_kill', 'psutil_timeout_kill', 'get_node_ip']
import os
import uuid
import time
import signal
import socket
import subprocess
import threading
try:
    import queue
except ImportError:
    import Queue as queue

def get_current_thread_id():
    """Get current thread id.

    @Returns:
        (int): Current thread's id.
    
    @Parameters:

    """
    return threading.current_thread().ident

def get_worker_id(prefix=None):
    """Get a unique name for a worker. The name template is `{prefix}:{hostname}:{process-id}:{thread-id}`.

    In [32]: from fastutils import sysutils

    In [33]: sysutils.get_worker_id('testapp')
    Out[33]: 'testapp:DESKTOP-MO5DJHQ:1896:9192'
    """
    worker_inner_id = '{}:{}:{}'.format(socket.gethostname(), os.getpid(), get_current_thread_id())
    if prefix:
        return prefix + ':' + worker_inner_id
    else:
        return worker_inner_id

def get_random_script_name(suffix=None):
    """Generate a random script name. For windows add .bat suffix.

    In [1]: import os

    In [2]: os.name
    Out[2]: 'nt'

    In [3]: from fastutils import sysutils

    In [4]: sysutils.get_random_script_name()
    Out[4]: '9b99d890-0b96-436d-9b1a-d70e9289e245.bat'
    """
    if suffix is None:
        if os.name == 'nt':
            suffix = '.bat'
        else:
            suffix = ''
    name = str(uuid.uuid4())
    return name + suffix

class NonBlockReader(object):
    """
    When we read from a stream, 
    but not sure if it will block or not-block, 
    so we read it from a new thread that will not block the main thread.

    Mostly you need to close the stream after your read,
    so that the created thread can got the read failed exception and end itself.
    """

    def __init__(self, stream, wait_time=1, autostart=True):
        self.stream = stream
        self.wait_time = wait_time
        self.lines = queue.Queue()
        self.started = False
        if autostart:
            self.start()

    def start(self):
        if self.started:
            return
        self.started = True
        self.read_thread = threading.Thread(target=self._read)
        self.read_thread.setDaemon(True)
        self.read_thread.start()

    def _read(self):
        while True:
            line = ''
            try:
                line = self.stream.readline()
            except Exception as error:
                self.lines.put('')
                break
            self.lines.put(line)
            if not line:
                break

    def readlines(self):
        results = []
        stime = time.time()
        while True:
            line = ''
            try:
                timeleft = self.wait_time - (time.time() - stime)
                if timeleft < 0:
                    break
                line = self.lines.get(timeout=timeleft)
            except queue.Empty:
                break
            if not line:
                break
            results.append(line)
        return results

    def read(self):
        return '\n'.join(self.readlines())

def default_timeout_kill(pid, sig=signal.SIGINT):
    """Kill the process.

    @Returns:
        (None): Nothing.
    
    @Parameters:
        pid(int): The process's pid to be killed.
        sig(SIGNAL, default to signal.SIGINT): The SIGNAL to be send to the process.
    """
    os.kill(pid, sig)

def psutil_timeout_kill(pid, sig=signal.SIGINT):
    """Kill the process and it's all subprocesses. psutil is required which may not be installed whiling installing zenutils.

    @Retruns:
        (None): Nothing.
    
    @Parameters:
        pid(int): The process's pid to be killed.
        sig(SIGNAL, default to signal.SIGINT): The SIGNAL to be send to the process and it's all subprocesses.
    """
    import psutil
    mainp = psutil.Process(pid)
    for subp in mainp.children(recursive=True):
        os.kill(subp.pid, sig)
    os.kill(mainp.pid, sig)

def execute_script(script, workspace=None, script_name=None, timeout=0, timeout_kill=None, timeout_kill_wait=1, non_block_read_timeout=2, delete_script=True):
    """Execute a shell script under special workspace.

    @Returns:
        (int, str, str): Returns script exitcode, std output and std error.
    
    @Parameters:
        script(str): Script source code.
        workspace(str, optional): Workspace path. If not given, a random template folder will be used.
        script_name(str, optional): A name used for creating the temporary script file. If not given, a random name will be used.
        timeout(int, optional): Script run time limit. 0 means no time limit.
        kill_sig(SIGNAL): Send the signal to the subprocess if it's running time is exceeded.
        kill_wait(int): Wait for some seconds after send kill signal to the subprocess.

    @Examples:
        sysutils.execute_script('#!/bin/bash
hostname
') --> Result maybe (0, 'testPc.local
', '')
    """
    from zenutils import fsutils
    from zenutils import strutils
    workspace = workspace or fsutils.get_temp_workspace()
    if not os.path.exists(workspace):
        os.makedirs(workspace, exist_ok=True)
    script_name = script_name or get_random_script_name()
    script_path = os.path.join(workspace, script_name)
    fsutils.write(script_path, script)
    os.chmod(script_path, 493)
    normally_finished_flag = False
    p = subprocess.Popen(script_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=workspace, shell=True, universal_newlines=True, bufsize=0)
    if timeout > 0:
        try:
            p.wait(timeout)
            normally_finished_flag = True
        except subprocess.TimeoutExpired:
            timeout_kill = timeout_kill or default_timeout_kill
            try:
                timeout_kill(p.pid)
            except Exception as error:
                pass
            time.sleep(timeout_kill_wait)
            pr = p.poll()
            if pr == 0:
                normally_finished_flag = True
            if pr is None:
                p.terminate()
    else:
        p.wait()
        normally_finished_flag = True
    c = 0
    while p.poll() is None:
        c += 1
        if c > 20:
            break
        time.sleep(0.1)
    if normally_finished_flag:
        (code, stdout, stderr) = (p.returncode, p.stdout.read(), p.stderr.read())
        stdout = strutils.force_text(stdout)
        stderr = strutils.force_text(stderr)
        result = (code, stdout, stderr)
    else:
        stdout_reader = NonBlockReader(p.stdout, wait_time=non_block_read_timeout)
        stderr_reader = NonBlockReader(p.stderr, wait_time=non_block_read_timeout)
        result = (p.returncode, force_text(stdout_reader.read()), force_text(stderr_reader.read()))
        try:
            p.stdout.close()
            p.stderr.close()
        except Exception:
            pass
    if delete_script:
        try:
            os.unlink(script_path)
        except Exception:
            pass
    return result

def get_node_ip():
    """get node's main ip address.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip