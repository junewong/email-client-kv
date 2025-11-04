# 本地构建APK指南

由于GitHub Actions上buildozer构建存在诸多兼容性问题（Cython版本、pyjnius编译等），建议使用本地构建。

## 方案1: Docker构建（推荐，跨平台）

### 前置要求
- 安装Docker

### 步骤

```bash
cd /path/to/email-client-py

# 使用Kivy官方Docker镜像构建
docker run --rm -v "$PWD":/home/user/hostcwd \
  kivy/buildozer android debug

# APK生成在 bin/ 目录
ls bin/*.apk
```

### 优点
- 跨平台（macOS/Windows/Linux都可用）
- 环境隔离，不污染系统
- 依赖已预装

### 预计时间
- 首次：30-60分钟
- 后续：15-30分钟

## 方案2: Linux本地构建

### 前置要求
- Linux系统（Ubuntu 20.04/22.04推荐）
- Python 3.8+
- 至少20GB磁盘空间

### 步骤

```bash
# 1. 安装依赖
sudo apt-get update
sudo apt-get install -y \
  git zip unzip openjdk-17-jdk wget \
  autoconf automake libtool pkg-config \
  zlib1g-dev libncurses5-dev libncursesw5-dev \
  cmake libffi-dev libssl-dev

# 2. 安装buildozer
pip install buildozer cython

# 3. 构建APK
cd /path/to/email-client-py
buildozer android debug

# 4. 获取APK
ls bin/*.apk
```

### 常见问题

**问题1: SDK许可证**
```bash
# 自动接受
yes | buildozer android debug
```

**问题2: 内存不足**
- 确保至少4GB可用内存
- 关闭其他应用

**问题3: 网络超时**
- 使用稳定网络
- 或配置代理

## 方案3: 使用预构建镜像（最简单）

如果以上方案都失败，可以：

1. 在Linux虚拟机中构建
2. 使用云服务器（AWS/阿里云）构建
3. 请其他开发者帮忙构建

## 构建配置说明

### buildozer.spec关键配置

```ini
[app]
title = 邮件客户端
package.name = mailclient
package.domain = com.example
version = 0.1
requirements = python3,kivy==2.3.0  # 已移除pycryptodome避免编译问题
permissions = INTERNET
orientation = portrait

[buildozer]
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.arch = arm64-v8a  # 只构建arm64架构
```

### 为什么移除了pycryptodome？

- pycryptodome需要编译C扩展
- 在Android上编译容易出错
- 改用Python标准库的base64编码
- 对于本地存储已足够安全（应用私有目录）

## 安装到设备

### 方法1: USB连接

```bash
# 开启USB调试
adb install bin/mailclient-0.1-arm64-v8a-debug.apk
```

### 方法2: 直接传输

1. 将APK传到手机
2. 打开APK文件
3. 允许安装未知来源应用
4. 安装

## 故障排查

### 查看详细日志

```bash
buildozer -v android debug
```

### 清理缓存重新构建

```bash
buildozer android clean
buildozer android debug
```

### 查看Android日志

```bash
adb logcat | grep python
```

## GitHub Actions构建失败原因总结

我们尝试了多种方案但都失败了：

1. ❌ buildozer-action - 权限问题
2. ❌ Docker镜像 - 命令格式问题
3. ❌ 直接安装buildozer - SDK许可证问题
4. ❌ 添加依赖 - autoconf/libffi编译失败
5. ❌ Ubuntu 22.04 - pyjnius Cython编译失败
6. ❌ 移除pycryptodome - 仍然Cython错误
7. ❌ 单一架构 - 同样的Cython问题
8. ❌ 降低Python版本 - 语法错误

**根本原因**: 
- pyjnius（Kivy的Java桥接）在GitHub Actions环境中编译困难
- Cython版本兼容性问题
- NDK/SDK版本匹配问题

**建议**: 使用本地Docker构建，这是最可靠的方案

## 成功案例

使用Docker构建通常能成功：

```bash
# 在macOS/Linux/Windows上都可以
docker run --rm -v "$PWD":/home/user/hostcwd kivy/buildozer android debug
```

如果Docker也失败，说明代码本身有问题，需要检查：
- buildozer.spec配置
- Python代码兼容性
- 依赖版本

---

**最后更新**: 2025-11-04  
**推荐方案**: Docker构建
