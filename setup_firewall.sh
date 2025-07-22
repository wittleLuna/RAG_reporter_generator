#!/bin/bash

echo "🔧 配置防火墙和安全组..."
echo "==============================="

# 1. 检查并开放8000端口 (CentOS/RHEL)
if command -v firewall-cmd &> /dev/null; then
    echo "📦 配置firewalld..."
    sudo firewall-cmd --permanent --add-port=8000/tcp
    sudo firewall-cmd --reload
    echo "✅ firewalld配置完成"
fi

# 2. 检查并开放8000端口 (Ubuntu/Debian)
if command -v ufw &> /dev/null; then
    echo "📦 配置ufw..."
    sudo ufw allow 8000/tcp
    sudo ufw reload
    echo "✅ ufw配置完成"
fi

# 3. 检查iptables
if command -v iptables &> /dev/null; then
    echo "📦 配置iptables..."
    sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
    sudo iptables-save > /etc/iptables/rules.v4 2>/dev/null || true
    echo "✅ iptables配置完成"
fi

# 4. 检查服务状态
echo "🔍 检查服务状态..."
if pgrep -f "uvicorn app:app" > /dev/null; then
    echo "✅ 服务正在运行"
else
    echo "⚠️ 服务未运行，请先运行 ./deploy_latest.sh"
fi

# 5. 检查端口监听
echo "🔌 检查端口监听..."
if netstat -tlnp | grep :8000 > /dev/null; then
    echo "✅ 端口8000正在监听"
else
    echo "❌ 端口8000未监听"
fi

# 6. 本地测试
echo "🌐 本地连接测试..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ 本地连接正常"
else
    echo "❌ 本地连接失败"
fi

echo ""
echo "📋 如果仍然无法访问，请检查："
echo "1. 云服务器控制台安全组设置"
echo "2. 确保入站规则允许8000端口"
echo "3. 检查服务器提供商防火墙设置"
echo ""
echo "🔧 手动配置安全组："
echo "- 协议：TCP"
echo "- 端口：8000"
echo "- 来源：0.0.0.0/0 (或特定IP段)"
echo ""
echo "🌐 测试访问："
echo "curl http://47.109.24.229:8000/health" 