# Android邮件客户端

基于Python + Kivy开发的轻量级Android邮件客户端。

## 功能特性

- ✅ 支持IMAP协议收取邮件
- ✅ 支持SMTP协议发送邮件
- ✅ 多邮箱服务商快速配置（QQ/163/126/Gmail/Outlook）
- ✅ 密码AES加密存储在本地设备
- ✅ 邮件列表查看
- ✅ 邮件详情查看
- ✅ 撰写和发送邮件
- ✅ 回复邮件
- ✅ SQLite本地缓存

## 安全说明

- **密码仅存储在用户设备本地**，使用AES加密
- 代码仓库和APK中不包含任何账户信息
- 用户需要在首次使用时输入邮箱密码
- 强制使用SSL/TLS加密连接

## 本地开发

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行应用

```bash
python main.py
```

## 打包APK

### 方法1: 使用GitHub Actions（推荐）

1. 将代码推送到GitHub
2. GitHub Actions会自动构建APK
3. 在Actions页面下载构建好的APK

### 方法2: 本地打包（需要Linux环境）

```bash
# 安装buildozer
pip install buildozer

# 初次构建（会下载Android SDK/NDK，需要较长时间）
buildozer android debug

# APK文件在 bin/ 目录
```

### 方法3: 使用Docker

```bash
docker run --rm -v "$PWD":/app kivy/buildozer android debug
```

## 使用说明

### 1. 登录

1. 安装APK到Android设备
2. 打开应用，选择邮箱服务商
3. 输入邮箱地址和密码
4. 点击登录

### 2. 查看邮件

- 登录成功后自动加载收件箱
- 点击邮件查看详情
- 点击"刷新"按钮更新邮件列表

### 3. 发送邮件

- 点击"写邮件"按钮
- 填写收件人、主题和正文
- 点击"发送"

### 4. 回复邮件

- 在邮件详情页点击"回复"
- 自动填充收件人和主题
- 编辑内容后发送

## 常见问题

### QQ邮箱/163邮箱登录失败？

需要在邮箱设置中开启IMAP/SMTP服务，并使用授权码而非登录密码。

**QQ邮箱**:
1. 登录QQ邮箱网页版
2. 设置 -> 账户 -> POP3/IMAP/SMTP服务
3. 开启服务并生成授权码
4. 使用授权码登录

**163邮箱**:
1. 登录163邮箱网页版
2. 设置 -> POP3/SMTP/IMAP
3. 开启服务并设置授权码
4. 使用授权码登录

### Gmail登录失败？

需要开启"应用专用密码"：
1. Google账户设置
2. 安全性 -> 两步验证
3. 应用专用密码
4. 生成密码并使用

### 发送邮件失败？

检查SMTP服务器配置是否正确，部分邮箱需要单独开启SMTP服务。

## 项目结构

```
email-client-py/
├── main.py                    # 应用入口
├── requirements.txt           # Python依赖
├── buildozer.spec            # Android打包配置
├── README.md                 # 使用说明
├── .gitignore                # Git忽略配置
├── .github/workflows/
│   └── build.yml             # 自动构建APK
├── docs/
│   └── 邮件客户端设计文档.md
└── src/
    ├── ui/
    │   ├── login.py          # 登录界面
    │   ├── maillist.py       # 邮件列表
    │   ├── maildetail.py     # 邮件详情
    │   └── compose.py        # 撰写邮件
    ├── core/
    │   ├── account.py        # 账户管理
    │   ├── imap_client.py    # IMAP客户端
    │   ├── smtp_client.py    # SMTP客户端
    │   └── storage.py        # 数据存储
    └── utils/
        ├── config.py         # 配置管理
        └── crypto.py         # 加密工具
```

## 技术栈

- **UI框架**: Kivy 2.3.0
- **邮件协议**: imaplib (IMAP), smtplib (SMTP)
- **加密**: PyCryptodome (AES)
- **数据库**: SQLite3
- **打包工具**: Buildozer

## 开发计划

- [x] Phase 1: 基础登录和邮件列表
- [x] Phase 2: 发送邮件功能
- [x] Phase 3: 邮件详情和回复
- [x] Phase 4: 本地缓存
- [ ] 未来: 附件支持、多账户切换、搜索功能

## 许可证

MIT License
