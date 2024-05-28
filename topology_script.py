import requests
import random
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
    return response.json()

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

# def create_node(project_id, node_name, compute_id, node_type):
#     url = f"{url_server}/v2/projects/{project_id}/nodes"
#     data = {
#         "name": node_name,
#         "compute_id": compute_id,
#         "node_type": node_type,
#         "properties": {}
#     }
#     response = send_request("POST", url, data)
#     return response.json()

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

def enable_dhcp(project_id, node_id, interface ,hostname):
    url = f"{url_server}/v2/projects/{project_id}/nodes/{node_id}/files/\/etc/network/interfaces"
    data =f"""auto {interface}\niface {interface} inet dhcp\n\thostname {hostname}"""
    response = requests.post(url, data=data)


if __name__ == "__main__":
    project_name = "Project"
    project = create_project(project_name)
    project_id = project["project_id"]

    appliance_templates = get_appliance_templates()

    opendht_template = next(template for template in appliance_templates if template["name"] == "opendht-alpine")
    switch_template = next(template for template in appliance_templates if template["name"] == "Ethernet switch")
    cloud_template = next(template for template in appliance_templates if template["name"] == "Cloud")
    nat_template = next(template for template in appliance_templates if template["name"] == "NAT")

    ##############################################
    # Topology: 2 DHT nodes are linked to a switch,
    # the switch is linked to a cloud node
    ##############################################

    node1 = create_node_from_appliance(project_id, "dht1", opendht_template["template_id"])
    node2 = create_node_from_appliance(project_id, "dht2", opendht_template["template_id"])
    switch = create_node_from_appliance(project_id, "switch", switch_template["template_id"], compute_id="vm")
    cloud = create_node_from_appliance(project_id, "cloud", cloud_template["template_id"], compute_id="vm")



    enable_dhcp(project_id, node1["node_id"], "eth0", "dht1")
    enable_dhcp(project_id, node2["node_id"], "eth0", "dht2")

    link = create_link(project_id, node1["node_id"], switch["node_id"], 0, 0)

    link1 = create_link(project_id, node2["node_id"], switch["node_id"], 0, 1)

    # use the second interface of the cloud node (NAT interface)
    link2 = create_link(project_id, cloud["node_id"], switch["node_id"], 1, 2)

    # ##############################################
    # # Topology: DHT node is linked to a switch,
    # # the switch is linked to a NAT node
    # ##############################################

    # node3 = create_node_from_appliance(project_id, "dht3", opendht_template["template_id"])
    # switch2 = create_node_from_appliance(project_id, "switch2", switch_template["template_id"], compute_id="vm")
    # nat = create_node_from_appliance(project_id, "nat", nat_template["template_id"], compute_id="vm")

    # enable_dhcp(project_id, node3["node_id"], "eth0", "dht3")
    # link3 = create_link(project_id, node3["node_id"], switch2["node_id"], 0, 0)
    # link4 = create_link(project_id, nat["node_id"], switch2["node_id"], 0, 1)

    nodes_start(project_id)