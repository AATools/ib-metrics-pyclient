# -*- coding: utf-8 -*-
"""Various functions for client api."""
import subprocess


def run_iib_command(**kwargs):
    """Calls predefined commands and returns their result."""
    command_mapping = {
        'get_brokers_status': 'mqsilist | grep Broker',
        'get_integration_nodes_status': 'mqsilist | grep "Integration node"',
        'get_broker_objects': 'mqsilist {0} -r',
    }
    broker = str()
    for arg_name, arg_value in kwargs.items():
        if arg_name == 'task':
            iib_command = command_mapping[arg_value]
        elif arg_name == 'broker_name':
            broker = arg_value
    if broker:
        command = iib_command.format(broker)
    else:
        command = iib_command
    output = execute_command(command=command)
    return output


def execute_command(command):
    """Executes in shell."""
    proc = subprocess.Popen(command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True)
    result = proc.communicate()[0]
    return result


def get_status(status):
    """Returns a numeric status value."""
    status_map = {
        'running': 1,
        'stopped': 0}
    return status_map[status]


def get_platform_params_for_commands(iib_ver):
    """Returns parameters for internal functions depending on Integration Bus version."""
    mqsilist_brokers = "get_brokers_status"
    mqsilist_integration_nodes = "get_integration_nodes_status"
    # https://www.ibm.com/support/knowledgecenter/en/SSMKHH_9.0.0/com.ibm.etools.mft.bipmsgs.doc/ay_bip1.htm
    bip_codes_broker = {
        # BIPCode: [broker_name_position, qm_name_position, status_position, trim_last_dot_in_qm_name]
        'BIP1284I': [2, 6, 8, 'false'],
        'BIP1285I': [2, 6, 8, 'false'],
        'BIP1293I': [2, 14 ,7, 'true'],
        'BIP1294I': [2, 14 ,7, 'true'],
        'BIP1295I': [2, 17, 13, 'true'],
        'BIP1296I': [2, 22, 4, 'true'],
        'BIP1297I': [2, 14, 7, 'true'],
        'BIP1298I': [2, 17, 4, 'true']
    }
    # https://www.ibm.com/support/knowledgecenter/en/SSMKHH_10.0.0/com.ibm.etools.mft.bipmsgs.doc/ay_bip1.htm
    bip_codes_integration_nodes = {
        # BIPCode: [broker_name_position, qm_name_position, status_position, trim_last_dot_in_qm_name]
        'BIP1284I': [3, 8, 14, 'false'],
        'BIP1285I': [3, 7, 9, 'false'],
        'BIP1295I': [3, 19, 15, 'true'],
        'BIP1296I': [3, 24 ,5, 'true'],
        'BIP1298I': [3, 18, 5, 'true'],
        'BIP1325I': [3, None, 9, 'false'],
        'BIP1326I': [3, None, 5, 'false'],
        'BIP1340I': [3, None, 5, 'false'],
        'BIP1353I': [3, 8, 10, 'false'],
        'BIP1366I': [3, 19, 15, 'true'],
        'BIP1376I': [3, 19, 15, 'true'],
        'BIP1377I': [3, 24, 5, 'true']
    }
    if iib_ver == "9":
        return mqsilist_brokers, bip_codes_broker
    if iib_ver == "10":
        return mqsilist_integration_nodes, bip_codes_integration_nodes
