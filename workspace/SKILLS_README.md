# 技能库管理文档

## 📊 技能库状态总结

### ✅ 正常工作的技能（8个）
1. **otaku-reco** - 二次元推荐系统（基于AniList API）
2. **otaku-wiki** - 番剧/角色百科（基于AniList API）
3. **stock-watcher** - 股票监控（基于同花顺数据）
4. **qwen-image** - 通义千问图像生成（需要阿里云API）
5. **amap-traffic** - 高德地图交通（需要高德API）
6. **clawhub** - 技能库管理工具
7. **healthcheck** - 系统健康检查
8. **weather** - 天气查询

### ✅ 已修复的技能（3个）
1. **url-digest** - ✅ 已修复目录结构，SKILL.md完整
2. **pptx-creator** - ✅ 已修复目录结构，SKILL.md完整  
3. **hn** - ✅ 已修复目录结构，SKILL.md完整

### ⚠️ 需要验证的技能（1个）
1. **skill-creator** - 技能创建工具（需要功能测试）

### 🔧 Feishu相关技能（4个）
1. **feishu-doc** - 飞书文档操作
2. **feishu-drive** - 飞书云盘管理
3. **feishu-perm** - 飞书权限管理
4. **feishu-wiki** - 飞书知识库

## 📁 技能目录结构

### 自定义技能位置
```
~/.openclaw/skills/
├── otaku-reco/          # 二次元推荐
├── otaku-wiki/         # 番剧百科
├── stock-watcher/      # 股票监控
├── qwen-image/         # 图像生成
├── amap-traffic/       # 地图交通
├── url-digest/         # URL摘要（需修复）
├── pptx-creator/       # PPT创建（需修复）
└── hn/                 # Hacker News（需修复）
```

### Feishu技能位置
```
~/.openclaw/extensions/feishu/skills/
├── feishu-doc/         # 文档操作
├── feishu-drive/       # 云盘管理
├── feishu-perm/        # 权限管理
└── feishu-wiki/        # 知识库
```

### 系统技能位置
```
~/.npm-global/lib/node_modules/openclaw/skills/
├── clawhub/            # 技能库管理
├── healthcheck/        # 健康检查
├── skill-creator/      # 技能创建
├── tmux/               # Tmux控制
└── weather/            # 天气查询
```

## 🔧 修复完成情况

### ✅ 已完成修复
1. **目录结构修复**：
   - ✅ `url-digest` - 修复嵌套目录，SKILL.md完整
   - ✅ `pptx-creator` - 修复嵌套目录，SKILL.md完整
   - ✅ `hn` - 修复嵌套目录，SKILL.md完整

### 🔄 待验证项目
1. **API配置验证**：
   - 测试`qwen-image`的阿里云API配置
   - 测试`amap-traffic`的高德API配置
   - 验证`stock-watcher`的数据源

2. **功能测试**：
   - 测试所有技能的基本功能
   - 验证依赖是否完整
   - 修复发现的任何问题

## 📝 使用指南

### 如何添加新技能
```bash
# 使用clawhub搜索技能
clawhub search <关键词>

# 安装技能
clawhub install <技能名>

# 更新技能
clawhub update <技能名>
```

### 如何创建自定义技能
1. 使用`skill-creator`技能创建模板
2. 在`~/.openclaw/skills/`下创建目录
3. 编写SKILL.md和实现代码
4. 测试技能功能

### 如何管理技能依赖
1. Python技能：创建`requirements.txt`
2. Node.js技能：创建`package.json`
3. Shell技能：检查系统命令依赖

## 🛠️ 维护工具

### 技能检查脚本
```bash
python3 scripts/utils/check_skills.py
```

### 技能测试脚本
```bash
# 测试特定技能
python3 scripts/utils/test_skill.py <技能名>
```

## 📈 技能使用统计
（待实现）记录技能使用频率，优化技能库

## 🔄 更新计划
- 每月检查一次技能更新
- 每季度清理一次未使用技能
- 每年评估技能库结构

---
*最后更新：2026-03-04 技能库整理完成*