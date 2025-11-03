#!/bin/bash
# Android APK构建脚本

set -e

echo "========================================="
echo "  Android邮件客户端 APK构建工具"
echo "========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: 未安装Docker"
    echo "请先安装Docker: https://www.docker.com/get-started"
    exit 1
fi

echo "✓ Docker已安装"
echo ""

# 选择构建方式
echo "请选择构建方式:"
echo "1) 使用Docker构建（推荐，跨平台）"
echo "2) 本地构建（需要Linux环境）"
echo "3) 仅测试模块导入"
read -p "请输入选项 (1-3): " choice

case $choice in
    1)
        echo ""
        echo "使用Docker构建APK..."
        echo "这可能需要30-60分钟（首次构建）"
        echo ""
        
        docker run --rm -v "$PWD":/app \
            kivy/buildozer android debug
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ 构建成功！"
            echo "APK文件位置: bin/"
            ls -lh bin/*.apk 2>/dev/null || echo "未找到APK文件"
        else
            echo ""
            echo "❌ 构建失败"
            exit 1
        fi
        ;;
    
    2)
        echo ""
        echo "本地构建APK..."
        
        if ! command -v buildozer &> /dev/null; then
            echo "❌ 错误: 未安装buildozer"
            echo "请运行: pip install buildozer"
            exit 1
        fi
        
        buildozer android debug
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ 构建成功！"
            echo "APK文件位置: bin/"
            ls -lh bin/*.apk
        else
            echo ""
            echo "❌ 构建失败"
            exit 1
        fi
        ;;
    
    3)
        echo ""
        echo "测试模块导入..."
        python3 test_import.py
        ;;
    
    *)
        echo "无效选项"
        exit 1
        ;;
esac

echo ""
echo "========================================="
echo "  构建完成"
echo "========================================="
