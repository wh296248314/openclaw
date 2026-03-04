# 技能库清单

## 当前安装的技能

### 自定义技能（~/.openclaw/skills/）
1. **amap-traffic** - 高德地图交通信息
2. **hn** - Hacker News阅读器
3. **otaku-reco** - 二次元推荐系统
4. **otaku-wiki** - 番剧/角色百科
5. **pptx-creator** - PPTX创建工具
6. **qwen-image** - 通义千问图像生成
7. **stock-watcher** - 股票监控
8. **url-digest** - URL摘要工具

### Feishu扩展技能（~/.openclaw/extensions/feishu/skills/）
1. **feishu-doc** - 飞书文档操作
2. **feishu-drive** - 飞书云盘管理
3. **feishu-perm** - 飞书权限管理
4. **feishu-wiki** - 飞书知识库

### 系统技能（~/.npm-global/lib/node_modules/openclaw/skills/）
1. **clawhub** - 技能库管理
2. **healthcheck** - 健康检查
3. **skill-creator** - 技能创建工具
4. **tmux** - Tmux远程控制
5. **video-frames** - 视频帧提取
6. **weather** - 天气查询

## 技能状态检查

### 需要验证的技能
1. **amap-traffic** - 需要API密钥验证
2. **qwen-image** - 需要阿里云API验证
3. **stock-watcher** - 需要数据源验证

### 功能正常的技能
1. **otaku-reco** - 基于AniList API，无需配置
2. **otaku-wiki** - 基于AniList API，无需配置
3. **hn** - Hacker News，无需配置
4. **pptx-creator** - 本地Python库，应正常工作
5. **url-digest** - 网页抓取，应正常工作

### Feishu技能
- 所有Feishu技能都需要有效的飞书应用配置
- 当前飞书通道已配置，技能应可用

## 整理计划

### 阶段1：技能验证
1. 测试每个技能的基本功能
2. 检查依赖和配置要求
3. 标记无法使用的技能

### 阶段2：文档整理
1. 为每个技能创建使用说明
2. 整理技能配置要求
3. 创建技能索引

### 阶段3：依赖管理
1. 检查Python依赖
2. 检查Node.js依赖
3. 确保所有依赖可安装

### 阶段4：优化改进
1. 修复发现的任何问题
2. 更新过时的技能
3. 添加缺失的功能

## 优先级
1. **高优先级**：经常使用的技能（otaku, stock-watcher, qwen-image）
2. **中优先级**：工具类技能（pptx-creator, url-digest）
3. **低优先级**：特定场景技能（amap-traffic, hn）