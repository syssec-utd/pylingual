from biobookshelf.main import *
from biobookshelf import PKG

def Recursively_stop_subprocesses(int_pid):
    if int_pid < 1000.0:
        (print('ERROR: given PID {} has less than 4 digits. For security reasons, this program failed'.format(int_pid)), sys.exit(2))
    df_processes = OS_Currently_running_processes()
    if int_pid in df_processes.PID.values:
        os.system('kill {}'.format(int_pid))
    df_subprocesses = PD_Select(df_processes, PPID=int_pid)
    for int_pid_subprocess in df_subprocesses.PID.values:
        Recursively_stop_subprocesses(int_pid_subprocess)

def Stop_a_job(pid=None):
    """
    # 2022/04/05
    Stop a process with a given PID and all subprocess belonging to the PID.
    
    'pid' : pid to recursively terminates
    """
    flag_entry_point = PKG.Detect_Entry_Point('biobook')
    if flag_entry_point:
        parser = argparse.ArgumentParser(description='Stop a process with a given PID and all subprocess belonging to the PID. This program has been developed by Hyunsu An (2021/06/03).')
        parser.add_argument('-i', '--pid', help='PID of a job to be terminated. (required)', type=int)
        args = parser.parse_args()
        int_pid = args.pid
    ' [parse arguments] '
    if int_pid is None:
        print('required arguments are not given, exiting')
        if flag_entry_point:
            sys.exit()
        else:
            return -1
    Recursively_stop_subprocesses(int_pid)

def Server_Status():
    """
    # 2022/04/05
    Print CPU and MEMORY usage of the FGL server for each program for each user.
    """
    flag_entry_point = PKG.Detect_Entry_Point('biobook')
    if flag_entry_point:
        parser = argparse.ArgumentParser(description='Print CPU and MEMORY usage of the FGL server for each program for each user. This program has been developed by Hyunsu An.')
        args = parser.parse_args()
    df = Parse_Printed_Table('\n'.join(os.popen('top -bn 1').read().split('\n')[6:])).rename(columns={'%CPU': 'CPU', '%MEM': 'MEM'})
    df = df[(df.CPU > 0) | (df.MEM > 0)]
    print(' ----- Usage Total ----- \n')
    print(df[['CPU', 'MEM']].sum())
    print('\n\n ----- Usage by each user ----- \n')
    print(df[['USER', 'CPU', 'MEM']].groupby('USER').sum().sort_values('MEM', ascending=False))
    print('\n\n ----- Usage by each program of each user ----- \n')
    print(df[['USER', 'COMMAND', 'CPU', 'MEM']].groupby(['USER', 'COMMAND']).sum().sort_values('MEM', ascending=False))
    print()