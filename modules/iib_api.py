# -*- coding: utf-8 -*-
import subprocess


def run_iib_command(**kwargs):
    command_mapping = {
        'get_brokers_status': 'mqsilist | grep Broker',
        'get_broker_objects': 'mqsilist {0} -r',
    }
    broker = ''
    for arg_name, arg_value in kwargs.items():
        if arg_name == 'task':
            iib_command = command_mapping[arg_value]
        elif arg_name == 'broker_name':
            broker = arg_value
    if broker:
        command = iib_command.format(broker)
    else:
        command = iib_command
    proc = subprocess.Popen(command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True)
    output = proc.communicate()[0]
    return output
