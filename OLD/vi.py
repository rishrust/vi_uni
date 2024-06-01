
import os
from datetime import datetime

#Chnge To your Pc credentials
pc_ip   = "192.168.0.108"
pc_pass = "777111"
pc_usr = "rish"


def compare_times(time1, time2):
    # Convert strings to datetime objects
    datetime1 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
    datetime2 = datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")
    
    # Compare datetime objects
    if datetime1 > datetime2:
        return "ph"
    elif datetime2 > datetime1:
        return "pc"
    else:
        return "Both times are equal"

def capture_command_output(command):
    stream = os.popen(command)
    output = stream.read().strip()
    return output



remote_dir=f"/home/{pc_usr}/.local/share/waydroid/data/data/it.vfsfitvnm.vimusic/databases/"
local_dir= "/data/data/it.vfsfitvnm.vimusic/databases/"
local_tmp_file=" /data/data/com.termux/files/home/vimusic/"


def fetch_data(data):
    fetch_data_command = f"sudo sshpass -p {pc_pass} scp -p -r  {pc_usr}@{pc_ip}:"+ remote_dir+data+" "+local_dir+data
    os.system(fetch_data_command)

remote_command=f"sshpass -p {pc_pass} ssh {pc_usr}@{pc_ip} stat "+remote_dir+"exoplayer_internal.db"
local_command = "sudo stat "+local_dir+"exoplayer_internal.db"


pc_upd= capture_command_output( remote_command+" | grep Modify")[8:-16]
ph_upd= capture_command_output( local_command +" | grep Modify")[8:-16]

print(pc_upd + " pc ")
print(ph_upd + " ph ")

opcode=compare_times(ph_upd, pc_upd)

if opcode=="pc": 
    fetch_data("data.db")
    fetch_data("data.db-wal")
    fetch_data("data.db-shm")
    #os.system('sudo cp data.db '+local_dir)
    print("updated from pc to android")
    

else:
    os.system(f"sshpass -p {pc_ip} sudo scp "+local_dir+f"data.db {pc_usr}@{pc_ip}:"+remote_dir)
    os.system(f"sshpass -p {pc_pass} sudo scp "+local_dir+f"data.db-wal {pc_usr}@{pc_ip}:"+remote_dir)
    os.system(f"sshpass -p {pc_pass} sudo scp "+local_dir+f"data.db-shm {pc_usr}@{pc_ip}:"+remote_dir)
    print('updated from andorid to pc')
           

