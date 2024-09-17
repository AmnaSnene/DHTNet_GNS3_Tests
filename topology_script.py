import requests
import random
import telnetlib
import time
import re
url_server = "http://192.168.56.1:3080"


# Function to send REST API requests to the GNS3 server with the requests library
def send_request(method, url, data=None):
    if method == "GET":
        response = requests.get(url)
    elif method == "POST":
        response = requests.post(url, json=data)
    elif method == "PUT":
        response = requests.put(url, json=data)
    elif method == "DELETE":
        response = requests.delete(url)
    else:
        raise ValueError("Invalid method")
    return response

def get_projects():
    url = f"{url_server}/v2/projects"
    response = send_request("GET", url)
    return response.json()

def open_project(project_id, path):
    url = f"{url_server}/v2/projects/load"
    data = {"path": path}
    response = send_request("POST", url, data)
    if response.status_code == 404:
        raise ValueError("Project not found")
    else:
        print(f"Project {project_id} opened")
    return response.json()

def open_project_by_name(project_name):
    projects = get_projects()
    project = next((project for project in projects if project["name"] == project_name), None)
    if project is None:
        raise ValueError("Project not found")
    return open_project(project["project_id"])

def get_project_by_name(project_name):
    projects = get_projects()
    project = next((project for project in projects if project["name"] == project_name), None)
    if project is None:
        raise ValueError("Project not found")
    return project

def duplicate_project(project_id, new_project_name):
    url = f"{url_server}/v2/projects/{project_id}/duplicate"
    data = {"name": new_project_name}
    response = send_request("POST", url, data)
    if response.status_code == 409:
        print(f"error: {response.json()}")
    else:
        print(f"Project {project_id} duplicated")
    return response.json()

def create_project(name):
    url = f"{url_server}/v2/projects"
    data = {"name": name}
    response = send_request("POST", url, data)
    if response.status_code == 409:
        raise ValueError("Project already exists")
    else:
        print(f"Project {name} created")
    return response.json()
def get_project_by_id(project_id):
    url = f"{url_server}/v2/projects/{project_id}"
    response = send_request("GET", url)
    return response.json()

def delete_project(project_id):
    url = f"{url_server}/v2/projects/{project_id}"
    response = send_request("DELETE", url)
    if response.status_code == 404:
        raise ValueError("Project not found")
    else:
        print(f"Project {project_id} deleted")

def create_node_from_appliance(project_id, node_name, appliance_id, compute_id=None):
    url = f"{url_server}/v2/projects/{project_id}/templates/{appliance_id}"
    data = {
        "compute_id": compute_id,
        "x": random.randint(0, 100),
        "y": random.randint(0, 100)
    }
    response = send_request("POST", url, data)
    if response.status_code == 404:
        raise ValueError("Appliance not found")
    else:
        print(f"Node {node_name} created")
    return response.json()

def get_appliance_templates():
    url = f"{url_server}/v2/templates"
    response = send_request("GET", url)
    return response.json()


def create_link(project_id, node1_id, node2_id, node1_interface_id, node2_interface_id):
    url = f"{url_server}/v2/projects/{project_id}/links"
    data = {
        "nodes": [
            {"adapter_number": 0, "node_id": node1_id, "port_number": node1_interface_id},
            {"adapter_number": 0, "node_id": node2_id, "port_number": node2_interface_id}
        ]
    }
    response = send_request("POST", url, data)
    if response.status_code == 409:
        raise ValueError("Link already exists")
    else:
        print(f"Link created between {node1_id} and {node2_id}")
    return response.json()

def nodes_start(project_id):
    url = f"{url_server}/v2/projects/{project_id}/nodes/start"
    response = send_request("POST", url, data={})

def get_node_by_name(project_id, node_name):
    url = f"{url_server}/v2/projects/{project_id}/nodes"
    response = send_request("GET", url)
    return next((node for node in response.json() if node["name"] == node_name), None)
# def enable_dhcp(project_id, node_id, interface ,hostname):
#     url = f"{url_server}/v2/projects/{project_id}/nodes/{node_id}/files/\/etc/network/interfaces"
#     data =f"""auto {interface}\niface {interface} inet dhcp\n\thostname {hostname}"""
#     response = requests.post(url, data=data)

def command_to_node(console_host, console_port, commands, prompt=[b"#", b">"]):
    """
    Send commands to a node using telnet
    :param console_host: The console host
    :param console_port: The console port
    :param commands: A list of commands to send
    :param prompt: The prompt to wait for
    :return: None
    """

    try:
        # Connect to the console
        tn = telnetlib.Telnet(console_host, console_port)
        # tn.read_until(b"#")  # Adjust prompt as necessary
        outputs = []
        # Send each command
        for command in commands:
            # print(f"Sending command: {command}")
            tn.write(command.encode() + b"\n")
            items = tn.expect(prompt) # Blocking call
            leftover = tn.read_very_eager().decode('utf-8')  # To make sure we get all the output
            if leftover != "":
                outputs.append(items[2].decode('utf-8') + leftover)
        # Close the connection
        tn.close()
        return outputs
    except Exception as e:
        print(f"An error occurred: {e}")

def get_node(project_id):
    url = f"{url_server}/v2/projects/{project_id}/nodes"
    response = send_request("GET", url)
    return response.json()

def delete_link(project_id, link_id):
    url = f"{url_server}/v2/projects/{project_id}/links/{link_id}"
    response = send_request("DELETE", url)
    if response.status_code == 404:
        raise ValueError("Link not found")
    else:
        print(f"Link {link_id} deleted")

def get_value_from_output(output_str, pattern):
    match = re.search(pattern, output_str)
    if match:
        return match.group(1)
    else:
        return None

def stop_node(project_id, node_id):
    url = f"{url_server}/v2/projects/{project_id}/nodes/{node_id}/stop"
    response = send_request("POST", url)
    return response.json()

def get_node_links(project_id, node_id):
    url = f"{url_server}/v2/projects/{project_id}/nodes/{node_id}/links"
    response = send_request("GET", url)
    return response.json()

if __name__ == "__main__":

    project_name = "dhtnet+1721140869.0285344"
    project_origin = get_project_by_name(project_name)
    # project = duplicate_project(project_origin["project_id"], f"Project{time.time_ns()}")
    project_id = project_origin["project_id"]
    path = project_origin["path"] + '/' + project_origin["filename"]
    print(path)
    open_project(project_id, path)
    appliance_templates = get_appliance_templates()

    dhtnet_template = next(template for template in appliance_templates if template["name"] == "dhtnet")

    # opendht_template = next(template for template in appliance_templates if template["name"] == "opendht-alpine")
    # switch_template = next(template for template in appliance_templates if template["name"] == "Ethernet switch")
    # cloud_template = next(template for template in appliance_templates if template["name"] == "Cloud")
    # nat_template = next(template for template in appliance_templates if template["name"] == "NAT")

    """
    Network Structure:
        LAN2:
            - Two DHTNet nodes are connected to a switch.
            - This switch is connected to the pfsense router node via interface em2.
            - The pfsense router node is connected to the cloud node via interface em1.
        LAN1:
            - The same topology as LAN2.
            - This switch is connected to the pfsense router node via interface em1.
        WAN:
            - The pfsense router node is connected to the cloud node via interface em0.

    Scenario:
        - Test Peer Discovery between DHTNet nodes in LAN1 and LAN2: dht1LAN1 should be able to connect to dht2LAN1 and dht1LAN2 should be able to connect to dht2LAN2.
        - One node in LAN1 will be moved to LAN2, eg, dht1LAN1 to LAN2: delete link between dht1LAN1 and switch1, create link between dht1LAN1 and switch2.
        - Test connectivity between dht1LAN1 and dht2LAN1.
    """


    node1LAN1 = create_node_from_appliance(project_id, "dht1LAN1", dhtnet_template["template_id"])
    # node2LAN1 = create_node_from_appliance(project_id, "dht2LAN1", dhtnet_template["template_id"])

    # nodes = get_node(project_id)
    # console_host = "192.168.56.101"

    # for i in range(5):
    #     nodes_start(project_id)

    #     for node in nodes:
    #         # if node["name"] == "dht1LAN1A":
    #         #     dht1LAN1 = node
    #         #     command_to_node(console_host, node["console"], ["./renew_dhcp.sh &"])
    #         if node["name"] == "dhtnet-gdb-1":
    #             dht1LAN2 = node
    #             command_to_node(console_host, node["console"], ["./renew_dhcp.sh &"])
    #         # elif node["name"] == "dht2LAN1A":
    #         #     dht2LAN1 = node
    #         #     command_to_node(console_host, node["console"], ["./renew_dhcp.sh &"])
    #         elif node["name"] == "dhtnet-gdb-2":
    #             dht2LAN2 = node
    #             command_to_node(console_host, node["console"], ["./renew_dhcp.sh &"])
    #         elif node["name"] == "SwitchLAN1":
    #             switchLAN1 = node
    #         elif node["name"] == "SwitchLAN2":
    #             switchLAN2 = node

    #     # Start peerDiscovery tool (dht node)
    #     # id = command_to_node(console_host, dht1LAN1["console"], ["peerDiscovery"], prompt=[b"Identity:([a-f0-9]+)"])
    #     # output_str = ''.join(id)
    #     # dht1LAN1["dhtId"] = get_value_from_output(output_str, r"Identity:([a-f0-9]+)")

    #     id = command_to_node(console_host, dht1LAN2["console"], ["peerDiscovery"], prompt=[b"Identity:([a-f0-9]+)"])
    #     output_str = ''.join(id)
    #     dht1LAN2["dhtId"] = get_value_from_output(output_str, r"Identity:([a-f0-9]+)")
    #     print("dht1LAN2:" + dht1LAN2["dhtId"] + "\n")

    #     # id = command_to_node(console_host, dht2LAN1["console"], ["peerDiscovery"], prompt=[b"Identity announced true"])
    #     # output_str = ''.join(id)
    #     # dht2LAN1["dhtId"] = get_value_from_output(output_str, r"Identity:([a-f0-9]+)")

    #     id = command_to_node(console_host, dht2LAN2["console"], ["peerDiscovery"], prompt=[b"Identity:([a-f0-9]+)"])
    #     output_str = ''.join(id)
    #     dht2LAN2["dhtId"] = get_value_from_output(output_str, r"Identity:([a-f0-9]+)")
    #     print("dht2LAN2:" + dht2LAN2["dhtId"] + "\n")
    #     # Test Peer Discovery between DHTNet nodes

    #     # print(command_to_node(console_host, dht1LAN1["console"], [f"connect {dht2LAN1['dhtId']}"]))
    #     # print(command_to_node(console_host, dht1LAN2["console"], [f"connect {dht2LAN2['dhtId']}"]))

    #     # Move dht1LAN1 to LAN2
    #     # get link id
    #     # link_id = get_node_links(project_id, dht1LAN1["node_id"])[0]["link_id"]
    #     # delete_link(project_id, link_id)
    #     # delete_link(project_id, link_id)
    #     # create link between dht1LAN1 and switchLAN2
    #     # link = create_link(project_id, dht1LAN1["node_id"], switchLAN2["node_id"], 0, 6)
    #     link2 = create_link(project_id, dht1LAN2["node_id"], switchLAN2["node_id"], 0, 5)
    #     link3 = create_link(project_id, dht2LAN2["node_id"], switchLAN2["node_id"], 0, 4)

    #     command_to_node(console_host, dht1LAN2["console"], ["cc"])
    #     # # Test connectivity between dht1LAN1 and dht1LAN2
    #     time.sleep(1)
    #     print(command_to_node(console_host, dht2LAN2["console"], [f"connect {dht1LAN2['dhtId']}"] + ["\n"]))
    #     # # time.sleep(8)
    #     # stop_node(project_id, dht1LAN1["node_id"])
    #     time.sleep(5)
    #     stop_node(project_id, dht1LAN2["node_id"])
    #     # stop_node(project_id, dht2LAN1["node_id"])
    #     stop_node(project_id, dht2LAN2["node_id"])

    #     # # get link id
    #     # link_id = get_node_links(project_id, dht1LAN1["node_id"])[0]["link_id"]
    #     delete_link(project_id, link2["link_id"])
    #     delete_link(project_id, link3["link_id"])
    #     # # create link between dht1LAN1 and switchLAN1
    #     # link = create_link(project_id, dht1LAN1["node_id"], switchLAN1["node_id"], 0, 6)




    # delete_project(project_id)
    # enable_dhcp(project_id, node1["node_id"], "eth0", "dht1")
    # enable_dhcp(project_id, node2["node_id"], "eth0", "dht2")

    # link = create_link(project_id, node1["node_id"], switch["node_id"], 0, 0)

    # link1 = create_link(project_id, node2["node_id"], switch["node_id"], 0, 1)

    # # use the second interface of the cloud node (NAT interface)
    # link2 = create_link(project_id, cloud["node_id"], switch["node_id"], 1, 2)
    # nodes_start(project_id)

    # commands = ["dhclient"]
    # command_to_node(node1["console_host"], node1["console"], commands)
    # command_to_node(node2["console_host"], node2["console"], commands)
    # # ##############################################
    # # # Topology: DHT node is linked to a switch,
    # # # the switch is linked to a NAT node
    # # ##############################################

    # # node3 = create_node_from_appliance(project_id, "dht3", opendht_template["template_id"])
    # # switch2 = create_node_from_appliance(project_id, "switch2", switch_template["template_id"], compute_id="vm")
    # # nat = create_node_from_appliance(project_id, "nat", nat_template["template_id"], compute_id="vm")

    # # enable_dhcp(project_id, node3["node_id"], "eth0", "dht3")
    # # link3 = create_link(project_id, node3["node_id"], switch2["node_id"], 0, 0)
    # # link4 = create_link(project_id, nat["node_id"], switch2["node_id"], 0, 1)
