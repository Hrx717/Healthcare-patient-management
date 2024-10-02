import os
import platform
import socket
import json

from modules import lnxCmnds, winxCmnds

def netInfo():
    # if os is not Linux: Then read from ifcfg.conf file in the same directory
    # else from etc/system/network
    file_path = ''
    
    if os.name == 'nt': #windows
        file_path = 'ifcfg.conf'
    elif os.name == 'posix': #Unix-like (linux)
        file_path = '/etc/network/'

    try:
        with open(file_path, 'r') as conf:
            lines = conf.readlines()
    except FileNotFoundError:
        print("The file 'ifcfg.conf' does not exist.")
        return

    # store file data in dictonary
    # Create a dictionary from the file
    config_dict = {}
    for line in lines:
        if '=' in line:
            key, value = line.split('=')
            config_dict[key.strip()] = value.strip()

    print()
    print('1. Intial ifcfg.conf file data stored in dictionary: ')
    print(config_dict)
    

    # modifying some network paremeters:

    # ONBOOT parameter from 'no' to 'yes'
    if config_dict['ONBOOT'] == '"no"':
        config_dict['ONBOOT'] = '"yes"'

    # BOOTPROTO parameter from dynamic to static
    config_dict['BOOTPROTO'] = '"static"'

    # defroute parameter from 'yes' to 'no'
    if config_dict['DEFROUTE'] == '"yes"':
        config_dict['DEFROUTE'] = '"no"'
    
    print()
    print('2. Dictionary after modifying parameters:')
    print(config_dict)


    # adding new entries to the dictionary like IPAddress (IPADDR) and subnet (PREFIX) value

    # ip-address of device
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # subnet prefix of device
    least_bit = ip_address.split('.')[3]
    sub_prefix = str(int(least_bit) - 7)
    
    config_dict['IPADDR'] = ip_address
    config_dict['PREFIX'] = sub_prefix

    print()
    print('3. Dictionary after adding IP-Address and Subnet-Prefix')
    print(config_dict)

    # writing updated dictionary to a new network file called net_ifcfg.conf file. 
    with open('net_ifcfg.conf', 'w') as f:
        for key, value in config_dict.items():
            f.write(f"{key}={value}\n")
    
    # writing updated dictionary to a new json file called net_ifcfg.json file. 
    with open('net_ifcfg.json', 'w') as json_file:
        json.dump(config_dict, json_file, indent=4)

    # checking os 
    os_name = platform.system().lower()
    cmd_rslt = ''
    name = ''
    netInfo_dict = {}

    if os_name == 'linux':
        name = 'lnxux'
        cmd_rslt = lnxCmnds.getLinuxCommandResult()
    elif os_name == 'windows':
        name = 'winx'
        cmd_rslt = winxCmnds.getWindowsCommandResult()

    output_str = ''
    for rslt in cmd_rslt:
        output_str += rslt

    netInfo_dict[name] = output_str
    print()
    print('Commands result based on os is appended on net_ifcfg.conf file\n')
    # print(netInfo_dict[name])

    # Appending commands result to net_ifcfg.cof file
    try:
        with open('net_ifcfg.conf', 'a') as f:
            f.write("\n Network Information\n")
            for key in netInfo_dict.items():
                f.write(f"{key}:\n")
                f.write(output_str)
    except FileNotFoundError:
        print("ERROR: File not found")
        return
    

    

netInfo()