import requests

# 在这里填入你的 Cloudflare API Key 和账户 Email
api_key = "YOUR_API_KEY"
email = "YOUR_EMAIL"

# 用户输入要更改的域名
domain = input("请输入要修改的域名：")

# 用户输入要更改的子域名
subdomain = input("请输入要修改的子域名（如果没有，请留空）：")

# 用户输入新的 IP 地址
new_ip = input("请输入新的 IP 地址：")

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

# 构建更新 DNS 记录的 URL
update_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?type=A&name={subdomain}.{domain}"

# 构建请求体
data = {
    "type": "A",
    "name": f"{subdomain}.{domain}",
    "content": new_ip,
    "ttl": 1,  # 可以根据需要设置 TTL
    "proxied": False  # 是否启用 Cloudflare 的代理
}

# 发送更新 DNS 记录的请求
response = requests.put(update_url, json=data, headers=headers)
result = response.json()

if response.status_code == 200:
    print(f"DNS 记录已成功更新为 {new_ip}")
else:
    print(f"更新 DNS 记录失败，错误信息: {result['errors'][0]['message']}")
