import requests

base_url = "http://192.168.1.101"

logs_response = requests.get(f"{base_url}/logs")
logs_list = logs_response.json()

def download_binlog(logname, output_path):
    response = requests.get(f"{base_url}/logs/{logname}/binlog")
    if response.status_code == 200:
        with open(output_path, "wb") as file:
            file.write(response.content)
        print(f"Log {logname} has been saved as {output_path}")
    else:
        raise Exception(f"Failed to download log {logname}")

desired_logs = ["BYEDP220037_ee68b38d092149d4_00068"]

for log_info in logs_list:
    logname = log_info["name"]
    if logname in desired_logs:
        output_path = f"API_{logname}.bez"
        download_binlog(logname, output_path)
