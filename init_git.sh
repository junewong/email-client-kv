#!/bin/bash
# Git仓库初始化脚本

echo "========================================="
echo "  初始化Git仓库"
echo "========================================="
echo ""

# 检查是否已经是Git仓库
if [ -d .git ]; then
    echo "⚠️  已经是Git仓库"
    read -p "是否重新初始化? (y/N): " reinit
    if [ "$reinit" != "y" ]; then
        echo "取消操作"
        exit 0
    fi
    rm -rf .git
fi

# 初始化Git
echo "初始化Git仓库..."
git init

# 添加所有文件
echo "添加文件..."
git add .

# 首次提交
echo "创建首次提交..."
git commit -m "Initial commit: Android邮件客户端 v0.1

功能:
- 登录和账户管理
- 邮件列表查看
- 邮件详情查看
- 发送和回复邮件
- 密码加密存储
- 本地缓存

技术栈:
- Python + Kivy
- IMAP/SMTP协议
- SQLite数据库
- AES加密"

echo ""
echo "✅ Git仓库初始化完成！"
echo ""
echo "下一步:"
echo "1. 在GitHub创建新仓库"
echo "2. 运行以下命令推送代码:"
echo ""
echo "   git remote add origin https://github.com/你的用户名/email-client-py.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. 推送后GitHub Actions会自动构建APK"
echo ""
