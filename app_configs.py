# SIMS_API_BASEURL="http://172.16.1.254:8051"
from ip import get_device_hostname, get_device_ip


# SIMS_API_BASEURL="http://192.168.200.94:8051"
SIMS_API_BASEURL="http://192.168.100.35:8051"
SIMS_API_DATA_CREATE_ENDPOINT="/create/scraped-data?platform=X"

# --------------SOURCE-API--------------------------

SIMS_API_SOURCE_BASEURL="http://192.168.100.35:8056"
SIMS_API_SOURCE_ENDPOINT="/api/admin-features/worker_node_management/workers/assignment/"
HEADERS = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0OTEwNzEyLCJpYXQiOjE3MzkzNTg3MTIsImp0aSI6IjBhYzU4ZTAwNTQyMDQ1MzJiZWU3YjU5NjFiMmMxYWNlIiwidXNlcl9pZCI6MX0.zzhQUl6fre-4lP2YBtNQGK8-tpbNbKqR7Hnz1u6tfyM"
    }
PARAMS = {
        "hostname": get_device_hostname(),
        "device_ip": get_device_ip(),  
    }
