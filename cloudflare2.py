import requests
import json

# 在这里填入你的 Cloudflare API Key 和账户 Email
api_key = "YOUR_API_KEY"
email = "YOUR_EMAIL"

# 填入你的域名和子域名（如果有）
domain = "example.com"  # 你的域名
subdomain = "subdomain"  # 子域名，如果不需要子域名，可以留空

# 获取你的当前公共 IP 地址（可以使用一个 IP 查询服务）
def get_current_ip():
    response = requests.get("https://api64.ipify.org?format=json")
    data = response.json()
    return data["ip"]

# 构建 API 请求的 URL
url = f"https://api.cloudflare.com/client/v4/zones?name={domain}"

# 构建请求头
headers = {
    "X-Auth-Email": email,
    "X-Auth-Key": api_key,
    "Content-Type": "application/json"
}

# 发送请求以获取 Zone ID
response = requests.get(url, headers=headers)
data = response.json()
zone_id = data["result"][0]["id"]

# 获取当前 IP 地址
current_ip = get_current_ip()

# 构建更新 DNS 记录的 URL
update_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=A&name={subdomain}.{domain}"

# 构建请求体
data = {
    "type": "A",
    "name": f"{subdomain}.{domain}",
    "content": current_ip,
    "ttl": 1,  # 可以根据需要设置 TTL
    "proxied": False  # 是否启用 Cloudflare 的代理
}

# 发送更新 DNS 记录的请求
response = requests.put(update_url, json=data, headers=headers)
result = response.json()

if response.status_code == 200:
    print(f"DNS 记录已成功更新为当前 IP 地址: {current_ip}")
else:
    print(f"更新 DNS 记录失败，错误信息: {result['errors'][0]['message']}")
