#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# 脚本功能：上传从Let"s Encrypt申请的 cdn.xxxx.com 的SSL证书到七牛云存储并启用。
# 使用方法: python qiniu_letssl.py
#
# pip install qiniu

import qiniu
from qiniu import DomainManager
import os
import time

def main():
    # 七牛云API相关的AccessKey和SecretKey.
    # access_key = os.getenv("ACCESS_KEY", "")
    access_key = os.getenv("QINIU_ACCESS_KEY")
    secret_key = os.getenv("QINIU_ACCESS_SECRET")
    if not access_key or not secret_key:
        raise Exception("请设置七牛云的AccessKey和SecretKey")
    
    # domain = os.getenv("QINIU_DOMAIN")

    # 操作的域名，多个域名用逗号分隔
    domains_str = os.getenv("QINIU_DOMAINS")
    if not domains_str:
        raise Exception("请设置 QINIU_DOMAINS 环境变量")
    
    # 将域名字符串分割为列表
    domain_list = [d.strip() for d in domains_str.split(",")]

    auth = qiniu.Auth(access_key=access_key, secret_key=secret_key)
    domain_manager = DomainManager(auth)

    for domain in domain_list:
      print(f"开始上传 SSL 证书: {domain}")
      # Let"s Encrypt申请的证书公钥和私钥文件所在的目录
      ca = os.path.expanduser(f"~/certs/{domain}/fullchain.pem")
      privatekey = os.path.expanduser(f"~/certs/{domain}/privkey.pem")

      # 检查证书文件是否存在
      if not os.path.exists(ca) or not os.path.exists(privatekey):
          print(f"证书文件 「{domain}」 不存在. 跳过进入下一循环...")
          continue
      # 读取证书文件内容
      with open(privatekey, "r") as f:
          privatekey_str = f.read()
      with open(ca, "r") as f:
          ca_str = f.read()

      # 证书名
      cert_name = f"{domain}/{time.strftime('%Y%m%d_%H%M%S', time.localtime())}"
      # 上传证书
      ret, info = domain_manager.create_sslcert(cert_name, domain, privatekey_str, ca_str)
      cert_id = ret["certID"]
      print(">>>>>>>>>>>>>>> 证书上传完成")
      print(f"证书上传完成 「{domain}」, certID: {cert_id}")


      # 配置域名使用 SSL 证书
      if domain.startswith("*"):
          domain = domain[1:]
      ret, info = domain_manager.put_httpsconf(domain, cert_id, False)
      print(">>>>>>>>>>>>>>> 配置 SSL 证书完成")
      print(info)

if __name__ == "__main__":
    main()
