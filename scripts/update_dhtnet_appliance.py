import requests
import json
import time

url_image = "ghcr.io/savoirfairelinux/dhtnet/dhtnet:master"

##################################################
# update the dhtnet image in the dhtnet template #
##################################################


# delete old dhtnet template
templates = requests.get("http://192.168.56.1:3080/v2/templates").json()
for template in templates:
    if template["name"] == "dhtnet":
        requests.delete("http://192.168.56.1:3080/v2/templates/" + template["template_id"])
        break

# add new dhtnet template
# POST http://192.168.56.1:3080/v2/templates {'default_name_format': '{name}-{0}', 'usage': '', 'symbol': ':/symbols/docker_guest.svg', 'category': 'guest', 'start_command': '', 'name': 'dhtnet', 'image': 'ghcr.io/amnasnene/dhtnet/dhtnet:master', 'adapters': 1, 'custom_adapters': [], 'environment': '', 'console_type': 'telnet', 'console_auto_start': False, 'console_resolution': '1024x768', 'console_http_port': 80, 'console_http_path': '/', 'extra_hosts': '', 'extra_volumes': [], 'compute_id': 'vm', 'template_id': '94c57326-02ef-410d-ac35-2fa67ce00e2a', 'template_type': 'docker'}
dhtnet_data = {'default_name_format': '{name}-{0}', 'usage': '', 'symbol': ':/symbols/docker_guest.svg', 'category': 'guest', 'start_command': '', 'name': 'dhtnet', 'image': f'{url_image}', 'adapters': 1, 'custom_adapters': [], 'environment': '', 'console_type': 'telnet', 'console_auto_start': False, 'console_resolution': '1024x768', 'console_http_port': 80, 'console_http_path': '/', 'extra_hosts': '', 'extra_volumes': [], 'compute_id': 'vm', 'template_type': 'docker'}
response_template = requests.post(url = "http://192.168.56.1:3080/v2/templates", data = json.dumps(dhtnet_data))
template_id = response_template.json()["template_id"]


##################################################
# create a new dhtnet instance to pull the image #
##################################################

# create a new project
response_project = requests.post(url = "http://192.168.56.1:3080/v2/projects", data = json.dumps({"name": f"dhtnet{int(time.time())}"}))
project_id = response_project.json()["project_id"]
if response_project.status_code != 201:
    print(response_project.text)
else:
    print("Project created successfully")


# create a new instance

response_instance = requests.post(url = f"http://192.168.56.1:3080/v2/projects/{project_id}/templates/{template_id}"
                        , data = json.dumps({"name": "dhtnet", "compute_id": "vm", "x": 0, "y": 0}))


if response_instance.status_code != 201:
    print(response_instance.text)
else:
    print("Image pulled successfully")

# wait for the instance to be created

# delete the project
response_delete = requests.delete(f"http://192.168.56.1:3080/v2/projects/{project_id}")

if response_delete.status_code != 204:
    print(response_delete.text)
else:
    print("Project deleted successfully")
