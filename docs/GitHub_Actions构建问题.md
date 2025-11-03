# GitHub Actions构建问题备忘录

## 遇到的问题及解决方案

### 1. Actions版本过期
**问题**: `actions/upload-artifact: v3` 已弃用

**解决**:
```yaml
- uses: actions/upload-artifact@v4  # v3 -> v4
- uses: actions/checkout@v4         # v3 -> v4
```

### 2. buildozer-action权限问题
**问题**: 
```
chown: invalid user: 'user'
subprocess.CalledProcessError: Command '['sudo', 'chown', '-R', 'user', '/github/workspace']'
```

**解决**: 不使用`ArtemSBulgakov/buildozer-action`，改用官方Docker镜像或直接安装

### 3. Docker镜像命令格式错误
**问题**: 
```
Unknown command/target bash
Unknown command/target sh
```

**原因**: `kivy/buildozer`镜像的ENTRYPOINT已经是buildozer命令

**解决**:
```yaml
# 错误
docker run kivy/buildozer bash -c "buildozer android debug"

# 正确
docker run kivy/buildozer android debug
```

### 4. Android SDK许可证未接受
**问题**:
```
Accept? (y/N): Skipping following packages as the license is not accepted:
Android SDK Build-Tools 36.1
```

**原因**: Docker环境中无法交互式接受许可证

**解决**: 改用直接在Ubuntu上安装buildozer，使用`yes`命令自动接受
```yaml
- name: Build APK
  run: |
    yes | buildozer android debug || buildozer android debug
```

### 5. autoconf编译libffi失败
**问题**:
```
configure.ac:418: error: possibly undefined macro: LT_SYS_SYMBOL_USCORE
autoreconf: error: /usr/bin/autoconf failed with exit status: 1
```

**原因**: 缺少必要的构建工具

**解决**: 安装完整的构建依赖
```yaml
- name: Install dependencies
  run: |
    sudo apt-get update
    sudo apt-get install -y git zip unzip openjdk-17-jdk wget \
      autoconf automake libtool pkg-config \
      zlib1g-dev libncurses5-dev libncursesw5-dev \
      libtinfo5 cmake libffi-dev libssl-dev
```

## 最终可用配置

```yaml
name: Build APK

on:
  push:
    branches: [ main ]
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-17-jdk wget \
          autoconf automake libtool pkg-config \
          zlib1g-dev libncurses5-dev libncursesw5-dev \
          libtinfo5 cmake libffi-dev libssl-dev
    
    - name: Install Buildozer
      run: pip install buildozer cython
        
    - name: Build APK
      run: |
        yes | buildozer android debug || buildozer android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: mailclient-debug
        path: bin/*.apk
```

## 构建时间

- 首次构建: 30-60分钟（下载SDK/NDK/依赖）
- 后续构建: 15-30分钟（有缓存）

## 常见错误排查

### 查看日志
```bash
# 使用GitHub CLI
gh run list --limit 1
gh run view <run-id> --log

# 或直接访问
https://github.com/用户名/仓库名/actions
```

### 清理缓存重新构建
删除`.buildozer`目录后重新构建

### 内存不足
GitHub Actions提供7GB内存，通常足够。如果不够，考虑：
- 减少并行架构（只构建arm64-v8a）
- 使用自托管runner

## 替代方案

### 方案1: 本地构建
```bash
# Linux环境
pip install buildozer
buildozer android debug
```

### 方案2: Docker本地构建
```bash
docker run --rm -v "$PWD":/home/user/hostcwd kivy/buildozer android debug
```

### 方案3: 使用其他CI服务
- GitLab CI
- CircleCI
- Travis CI

## 优化建议

1. **缓存依赖**: 使用`actions/cache`缓存`.buildozer`目录
2. **只构建单架构**: 减少构建时间
3. **定时构建**: 避免每次push都构建
4. **使用matrix**: 并行构建多个版本

## 参考资料

- [Buildozer文档](https://buildozer.readthedocs.io/)
- [Kivy Android打包](https://kivy.org/doc/stable/guide/packaging-android.html)
- [GitHub Actions文档](https://docs.github.com/en/actions)
- [python-for-android](https://python-for-android.readthedocs.io/)

---

**最后更新**: 2025-11-04  
**状态**: 已解决所有已知问题
