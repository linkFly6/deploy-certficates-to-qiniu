> 原项目不支持多域名，本项目修改为支持多域名（主要是 `upload_cert.py`），并完善了 README.MD 和自动化教程。非常感谢原作者 [@lxkaka](https://github.com/lxkaka/deploy-certficates-to-qiniu/tree/main) 提供的项目基础

# 上传证书到七牛云

这个项目的主要功能是定期根据阿里云的域名，更新 SSL 证书并将证书上传到七牛云：
- 通过 [acme.sh](https://github.com/acmesh-official/acme.sh) 自动化操作阿里云的域名，自动申请免费证书（`Let's Encrypt` / `ZeroSSL` / `Buypass` 等等），默认 90~180 天不等
- 将申请下来的证书上传到七牛云
- 通过 Github Actions 自动化定期续约证书


## Github Actions 自动化

这个项目使用 GitHub Actions 来自动化证书的更新和部署。GitHub Actions 会在每两个月的第二十天自动执行这个任务，可以在 `.github/workflows/action.yml` 文件中查看详细的配置。

1. Fork 这个项目
2. 打开项目设置 `Settings` -> `Secrets and variables` -> `Actions` -> `New respository secret`
          <img alt="image" src="https://github.com/user-attachments/assets/22821538-b20d-4458-9560-49ba4d05ebcd" />

3. 配置 Secert

   > Secert 在（[.github/workflows/action.yml](https://github.com/linkFly6/deploy-certficates-to-qiniu/blob/main/.github/workflows/action.yml) 中读取， e.g. `${{ secrets.DOMAINS }}`）：

   - `DOMAINS` : 域名、或域名列表(用 `,` 号分割)
     > 示例：单域名 `example.com`、泛域名 `*.example.com`、多域名 `example.com,static.example.com`
   - `EMAIL` : 邮箱账号，`acme.sh` 申请对应 CA 证书需要
     > 示例：`example@live.com`
   - `ALIYUN_ACCESS_KEY_ID` : 阿里云鉴权账号，在 [RAM 访问控制](https://ram.console.aliyun.com/users) 里，对应用户下的 `AccessKey ID`
     <details open>
          
     <summary>阿里云创建 RAM 用户流程：</summary>
  
     <br />     
     
     > - 进入 [RAM 访问控制](https://ram.console.aliyun.com/users)，创建用户：
     >   <img alt="image" src="https://github.com/user-attachments/assets/fe74261c-900a-4966-a9f8-d66a392295c3" />
     > - 勾选 **使用永久 AccessKey 访问**
     >   <img alt="image" src="https://github.com/user-attachments/assets/36c35919-6838-4db7-bf78-49b6e2f6f063" />
     > - 创建完成以后注意保管记录好 `AccessKey Secret`，**只有第一次创建才能复制 `AccessKey Secret`，关闭后就再也访问不了了**
     >   <img width="1459" alt="image" src="https://github.com/user-attachments/assets/9f7fc092-4280-4b4e-a555-398d03b0bc9a" />
     > - 进入对应用户下, 进行授权，授予 `AliyunDNSFullAccess` 和 `AliyunDomainFullAccess` 权限：
     >   <img width="1161" alt="image" src="https://github.com/user-attachments/assets/4f9490fd-6b33-48fc-bf13-b10c642c3912" />

     <br />
     </details>
  

   - `ALIYUN_ACCESS_KEY_SECRET` : 阿里云鉴权账号，在 [RAM 访问控制](https://ram.console.aliyun.com/users) 里，对应用户下的 `AccessKey Secert`
     > 注意，**RAM用户的 `AccessKey Secret` 只在创建时显示，不支持查看，请妥善保管**，如果错过了第一个创建的保存，需要删除用户再重新创建一个

   - `QINIU_ACCESS_KEY` : 七牛云账号 AK，在 [七牛云个人中心](https://portal.qiniu.com/developer/user/key)，`秘钥管理` 里；用来上传七牛云证书、和绑定到域名
   - `QINIU_ACCESS_SECRET`: 七牛云账号 SK，在 [七牛云个人中心](https://portal.qiniu.com/developer/user/key)，`秘钥管理` 里；用来上传七牛云证书、和绑定到域名


<br />

--------------
> 原项目 README 👇

## 安装

首先，你需要安装项目的依赖。你可以使用以下命令来安装：

```bash
pip install -r requirements.txt
```

## 使用   
你可以使用以下命令来运行这个项目：
```
python upload_cert.py
```
在运行这个命令之前，你需要确保你的证书文件已经放在了正确的位置，并且你已经设置了正确的环境变量。
包含如下环境变量
**QINIU_ACCESS_KEY**  
**QINIU_ACCESS_SECRET**  
**QINIU_DOMAIN** 

### 证书生成
#### 安装 acme   
`curl https://get.acme.sh | sh`
#### 阿里云 ak 和 as 写入配置文件  
vim ～/.acme.sh/acme.sh.env     
修改后acme.sh.env文件变成:    
```bash
export LE_WORKING_DIR="/${用户目录}/.acme.sh"  
alias acme.sh="/${用户目录}/.acme.sh/acme.sh"  
export Ali_Key="*****“
export Ali_Secret=”*******"
```
#### 生成
``` bash
mkdir -p ~/certs/${domain}
acme.sh --issue --dns dns_ali -d ${domain} \
          --key-file ~/certs/${domain}/privkey.pem --fullchain-file ~/certs/${domain}/fullchain.pem
```

