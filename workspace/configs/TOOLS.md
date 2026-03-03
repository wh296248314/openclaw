# TOOLS.md - 本地工具配置

技能定义_如何_使用工具。这个文件是_我的_具体配置——那些只属于我这个环境的东西。

## 🛠️ 当前系统配置

### 🌐 网络代理
- **clash-party**: v1.9.2 (Linux amd64)
- **订阅链接**: `https://feed.iggv5.com/c/11669368-e191-407d-867f-90c5f87fbdf4/platform/clash/iGG-iGuge`
- **配置文件**: `~/.config/mihomo-party/profiles/19cb15a3055.yaml`
- **代理端口**: 
  - HTTP: 7890
  - SOCKS: 7891
  - Mixed: 7892
- **启动脚本**: `/home/admin/openclaw/workspace/start-clash.sh`
- **节点数量**: 98个（香港、日本、美国、台湾、新加坡等）

### ⌨️ 输入法
- **虎码输入法**: Huma输入法
- **数据库文件**: `/usr/share/ibus-table/tables/tiger.db` (8.5MB SQLite)
- **配置状态**: 已安装并设为默认输入框架
- **重启命令**: `ibus restart`

### 🔍 监控系统
#### 智能超时监控卫士
- **当前版本**: 功能完整的增强版
- **进程PID**: 182637（通过`start_complete_guardian.sh`启动）
- **配置文件**: `timeout_guardian_optimized_config.json`
- **超时阈值**:
  - 🔴 Critical: 30秒
  - 🟠 High: 60秒
  - 🟡 Medium: 120秒
  - 🟢 Low: 300秒
- **系统监控**:
  - CPU告警: >80%警告, >95%严重
  - 内存告警: >85%警告, >95%严重
  - 磁盘告警: >90%警告, >98%严重
- **日志文件**: `complete_guardian.log`
- **仪表板**: `python3 complete_guardian_main.py --dashboard`

#### 钉钉通知模块
- **状态**: 代码就绪，等待Webhook配置
- **测试脚本**: `test_dingtalk_quick.py`
- **集成版**: `enhanced_guardian_with_dingtalk_fixed.py`
- **环境变量**:
  - `DINGTALK_WEBHOOK_URL`（需要配置）
  - `DINGTALK_SECRET`（可选）

### 📁 Git仓库
- **主仓库**: `git@github.com:wh296248314/lifeos.git`
- **唯一推送目标**: 只有GitHub，没有其他平台
- **大文件规则**: 单个文件限制100MB，超过90MB要处理
- **清理命令**: `git gc --prune=now`
- **自动提交**: Obsidian每日三次（12:00, 19:00, 23:00）

### 🐧 系统信息
- **操作系统**: Ubuntu 22.04 LTS (jammy), 64-bit
- **工作目录**: `/home/admin/openclaw/workspace`
- **OpenClaw版本**: 需要检查更新
- **内存目录**: `memory/`（存放每日工作记录）

## 🔧 实用脚本
### 监控相关
- `start_complete_guardian.sh` - 启动完整版监控卫士
- `monitor_guardian_30min.sh` - 30分钟监控观察脚本
- `test_dingtalk_quick.py` - 钉钉通知快速测试

### 代理相关
- `start-clash.sh` - 启动clash-party代理

### 测试相关
- `test_guardian.py` - 监控卫士功能测试
- `demo_enhanced_guardian.sh` - 增强版演示脚本

## 📊 健康检查命令
```bash
# 检查监控卫士状态
ps aux | grep complete_guardian
python3 complete_guardian_main.py --dashboard

# 检查代理状态
curl --proxy http://127.0.0.1:7890 http://ip-api.com/json

# 检查系统资源
top -bn1 | grep "Cpu(s)"
free -m
df -h /

# 检查Git状态
cd /home/admin/openclaw/workspace && git status
```

## ⚠️ 注意事项
1. **大文件处理**: 定期检查是否有超过90MB的文件，避免Git推送失败
2. **监控告警**: 钉钉通知需要配置Webhook URL才能生效
3. **代理更新**: clash-party订阅每小时自动更新
4. **内存管理**: 每日工作记录保存在`memory/`目录，定期整理

## 🔄 更新记录
- **2026-03-03**: 添加clash-party、虎码输入法、监控卫士配置
- **2026-03-03**: 创建钉钉通知模块和测试脚本
- **2026-03-03**: 记录Git仓库配置和系统信息

---

*这是我的工具备忘单。添加任何有助于我工作的东西。*
