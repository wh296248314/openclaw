#!/bin/bash
# SCRM回收机制问题解决执行脚本
# 问题：填写完跟进记录就会被回收，回收机制和商机阶段导致

echo "========================================================"
echo "SCRM回收机制问题解决执行脚本"
echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================================"

# 设置工作目录
WORKDIR="/home/admin/openclaw/workspace/SCRM回收机制问题解决_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$WORKDIR"
cd "$WORKDIR"

echo "步骤1: 创建工作目录结构"
echo "--------------------------------"

# 创建目录结构
mkdir -p 01_问题分析
mkdir -p 02_解决方案
mkdir -p 03_测试验证
mkdir -p 04_实施计划
mkdir -p 05_沟通记录
mkdir -p 06_文档输出

echo "工作目录: $(pwd)"
echo "目录结构创建完成"

echo ""
echo "步骤2: 复制问题分析文档"
echo "--------------------------------"

# 复制问题分析文档
cp ../SCRM回收机制问题分析.md 01_问题分析/
echo "问题分析文档已复制: 01_问题分析/SCRM回收机制问题分析.md"

echo ""
echo "步骤3: 生成详细解决方案文档"
echo "--------------------------------"

# 生成详细解决方案
cat > 02_解决方案/详细技术方案.md << 'EOF'
# SCRM回收机制问题 - 详细技术方案

## 1. 问题概述
**问题ID**: SCRM-002
**问题**: 填写完跟进记录就会被回收
**根本原因**: 回收机制与商机阶段不匹配

## 2. 当前系统分析

### 2.1 数据库表结构
```sql
-- 客户表
CREATE TABLE customer (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20),
    stage VARCHAR(50), -- 商机阶段
    last_follow_time DATETIME,
    recycle_time DATETIME,
    status VARCHAR(20)
);

-- 跟进记录表
CREATE TABLE follow_record (
    id BIGINT PRIMARY KEY,
    customer_id BIGINT,
    content TEXT,
    follow_time DATETIME,
    next_follow_time DATETIME,
    created_by VARCHAR(50)
);

-- 回收日志表
CREATE TABLE recycle_log (
    id BIGINT PRIMARY KEY,
    customer_id BIGINT,
    recycle_reason VARCHAR(200),
    recycle_time DATETIME,
    operator VARCHAR(50)
);
```

### 2.2 当前问题代码分析
```java
// 问题代码示例（简化版）
public class FollowRecordService {
    
    @Transactional
    public void saveFollowRecord(FollowRecord record) {
        // 保存跟进记录
        followRecordDao.save(record);
        
        // 问题：保存后立即检查回收
        checkAndRecycleCustomer(record.getCustomerId());
    }
    
    private void checkAndRecycleCustomer(Long customerId) {
        Customer customer = customerDao.findById(customerId);
        
        // 简单的回收逻辑：只要保存跟进记录就回收
        if (shouldRecycle(customer)) {
            recycleCustomer(customer);
        }
    }
}
```

## 3. 解决方案设计

### 3.1 新回收机制设计

#### 3.1.1 回收触发时机调整
```java
// 新设计：分离保存和回收
public class NewFollowRecordService {
    
    @Transactional
    public void saveFollowRecord(FollowRecord record) {
        // 只保存跟进记录，更新最后跟进时间
        followRecordDao.save(record);
        
        Customer customer = customerDao.findById(record.getCustomerId());
        customer.setLastFollowTime(record.getFollowTime());
        customerDao.update(customer);
        
        // 不立即触发回收，由定时任务处理
    }
}
```

#### 3.1.2 定时回收任务
```java
@Component
public class CustomerRecycleScheduler {
    
    @Scheduled(cron = "0 0 2 * * ?") // 每天凌晨2点执行
    public void autoRecycleCustomers() {
        List<Customer> candidates = findRecycleCandidates();
        
        for (Customer customer : candidates) {
            // 根据商机阶段决定是否回收
            if (shouldRecycleByStage(customer)) {
                // 发送预警通知
                sendRecycleWarning(customer);
                
                // 等待确认后回收（或自动回收）
                scheduleRecycle(customer);
            }
        }
    }
    
    private boolean shouldRecycleByStage(Customer customer) {
        String stage = customer.getStage();
        Date lastFollowTime = customer.getLastFollowTime();
        Date now = new Date();
        
        long days = TimeUnit.MILLISECONDS.toDays(now.getTime() - lastFollowTime.getTime());
        
        // 根据商机阶段设置不同的回收阈值
        Map<String, Integer> stageThresholds = Map.of(
            "初步接触", 7,
            "需求了解", 14,
            "方案沟通", 21,
            "报价阶段", 30,
            "成交阶段", -1, // 不回收
            "已成交", -1    // 不回收
        );
        
        Integer threshold = stageThresholds.get(stage);
        if (threshold == null || threshold == -1) {
            return false;
        }
        
        return days > threshold;
    }
}
```

### 3.2 数据库变更设计

#### 3.2.1 新增表
```sql
-- 回收规则表
CREATE TABLE recycle_rule (
    id BIGINT PRIMARY KEY,
    stage VARCHAR(50) NOT NULL,
    threshold_days INT NOT NULL,
    warning_days INT, -- 预警提前天数
    auto_recycle BOOLEAN DEFAULT false,
    enabled BOOLEAN DEFAULT true,
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 回收预警记录表
CREATE TABLE recycle_warning (
    id BIGINT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    warning_time DATETIME NOT NULL,
    expected_recycle_time DATETIME,
    notified BOOLEAN DEFAULT false,
    acknowledged BOOLEAN DEFAULT false
);
```

#### 3.2.2 数据迁移脚本
```sql
-- 迁移现有回收配置
INSERT INTO recycle_rule (stage, threshold_days, warning_days, auto_recycle, enabled)
VALUES 
    ('初步接触', 7, 3, false, true),
    ('需求了解', 14, 3, false, true),
    ('方案沟通', 21, 5, false, true),
    ('报价阶段', 30, 7, false, true),
    ('成交阶段', -1, NULL, false, true),
    ('已成交', -1, NULL, false, true);
```

### 3.3 接口设计

#### 3.3.1 回收检查接口
```java
@RestController
@RequestMapping("/api/customer/recycle")
public class RecycleController {
    
    @GetMapping("/check/{customerId}")
    public RecycleCheckResult checkRecycle(@PathVariable Long customerId) {
        Customer customer = customerService.getCustomer(customerId);
        RecycleRule rule = recycleRuleService.getRuleByStage(customer.getStage());
        
        RecycleCheckResult result = new RecycleCheckResult();
        result.setCustomerId(customerId);
        result.setStage(customer.getStage());
        result.setLastFollowTime(customer.getLastFollowTime());
        result.setThresholdDays(rule.getThresholdDays());
        result.setShouldRecycle(shouldRecycle(customer, rule));
        result.setWarningDays(rule.getWarningDays());
        
        return result;
    }
}
```

#### 3.3.2 预警通知接口
```java
@RestController
@RequestMapping("/api/notification")
public class NotificationController {
    
    @PostMapping("/recycle-warning")
    public void sendRecycleWarning(@RequestBody RecycleWarningRequest request) {
        // 发送企业微信通知
        wechatService.sendRecycleWarning(request);
        
        // 发送系统消息
        systemMessageService.sendRecycleWarning(request);
        
        // 记录预警日志
        warningLogService.logWarning(request);
    }
}
```

## 4. 实施步骤

### 4.1 第一阶段：准备阶段（今天）
1. **环境准备**
   ```bash
   # 备份生产数据
   mysqldump -u root -p scrm_db > scrm_backup_$(date +%Y%m%d).sql
   
   # 准备测试环境
   git checkout -b feature/recycle-mechanism-fix
   ```

2. **代码分析**
   - 定位问题代码位置
   - 分析影响范围
   - 制定修改计划

### 4.2 第二阶段：开发阶段（3月4日）
1. **数据库变更**
   ```sql
   -- 执行DDL变更
   ALTER TABLE customer ADD COLUMN recycle_rule_id BIGINT;
   CREATE INDEX idx_customer_stage ON customer(stage);
   ```

2. **代码修改**
   - 修改跟进记录保存逻辑
   - 实现新的回收检查逻辑
   - 添加预警通知功能

### 4.3 第三阶段：测试阶段（3月5日）
1. **单元测试**
   ```java
   @Test
   public void testSaveFollowRecordWithoutRecycle() {
       FollowRecord record = new FollowRecord();
       // 测试保存跟进记录不触发回收
   }
   
   @Test
   public void testRecycleByStage() {
       // 测试不同商机阶段的回收逻辑
   }
   ```

2. **集成测试**
   - 测试完整业务流程
   - 测试数据一致性
   - 测试性能影响

### 4.4 第四阶段：上线阶段（3月6日）
1. **上线前检查**
   ```bash
   # 检查数据库变更
   SHOW TABLES LIKE 'recycle_%';
   
   # 检查代码版本
   git log --oneline -10
   ```

2. **上线部署**
   ```bash
   # 部署新版本
   ./deploy.sh --env=production --version=1.2.0
   
   # 执行数据迁移
   ./migrate.sh --env=production
   ```

## 5. 回滚方案

### 5.1 回滚条件
- 新功能导致系统崩溃
- 数据出现严重不一致
- 用户反馈问题严重

### 5.2 回滚步骤
```bash
# 1. 停止新版本服务
systemctl stop scrm-service

# 2. 恢复旧版本代码
git checkout main
./deploy.sh --env=production --version=1.1.0

# 3. 恢复数据库（如果需要）
mysql -u root -p scrm_db < scrm_backup_$(date +%Y%m%d).sql

# 4. 启动服务
systemctl start scrm-service
```

## 6. 监控指标

### 6.1 技术监控
```yaml
监控指标:
  - 名称: 回收任务执行时间
    阈值: < 5分钟
    报警: 超过阈值
  
  - 名称: 数据库连接数
    阈值: < 80%
    报警: 超过阈值
  
  - 名称: 错误日志数量
    阈值: < 10/小时
    报警: 超过阈值
```

### 6.2 业务监控
```yaml
业务指标:
  - 每日回收客户数
  - 回收预警发送数
  - 用户确认回收数
  - 自动回收数
  - 回收相关投诉数
```

## 7. 成功标准

### 7.1 技术标准
- [ ] 所有单元测试通过
- [ ] 集成测试通过
- [ ] 性能测试达标
- [ ] 监控指标正常

### 7.2 业务标准
- [ ] 原始问题解决
- [ ] 用户反馈积极
- [ ] 业务指标改善
- [ ] 无数据丢失

---
**方案版本**: v1.0
**创建时间**: $(date '+%Y-%m-%d %H:%M')
**负责人**: 待确认
**状态**: 待评审
EOF

echo "详细技术方案已生成: 02_解决方案/详细技术方案.md"

echo ""
echo "步骤4: 生成测试用例"
echo "--------------------------------"

# 生成测试用例
cat > 03_测试验证/测试用例.md << 'EOF'
# SCRM回收机制问题 - 测试用例

## 测试环境
- 环境: 测试环境
- 数据库: MySQL 8.0
- 应用版本: 1.2.0-SNAPSHOT
- 测试时间: $(date '+%Y-%m-%d')

## 测试用例列表

### TC-001: 保存跟进记录不触发立即回收
**测试目标**: 验证保存跟进记录后不会立即回收客户
**前置条件**: 
1. 测试客户处于"需求了解"阶段
2. 最后跟进时间为3天前

**测试步骤**:
1. 登录SCRM系统
2. 进入客户详情页
3. 填写跟进记录并保存
4. 检查客户是否还在原销售名下

**预期结果**:
- 跟进记录保存成功
- 客户未被回收
- 最后跟进时间更新为当前时间

**实际结果**:
- [ ] 通过
- [ ] 失败

**备注**:
________________________________________

### TC-002: 商机阶段敏感回收 - 初步接触阶段
**测试目标**: 验证初步接触阶段7天后触发回收
**前置条件**:
1. 测试客户处于"初步接触"阶段
2. 最后跟进时间为8天前

**测试步骤**:
1. 执行回收定时任务
2. 检查是否发送回收预警
3. 检查客户状态

**预期结果**:
- 发送回收预警通知
- 客户进入待回收状态
- 销售可以确认或取消回收

**实际结果**:
- [ ] 通过
- [ ] 失败

**备注**:
________________________________________

### TC-003: 商机阶段敏感回收 - 成交阶段
**测试目标**: 验证成交阶段不触发回收
**前置条件**:
1. 测试客户处于"成交阶段"
2. 最后跟进时间为60天前

**测试步骤**:
1. 执行回收定时任务
2. 检查是否发送回收预警
3. 检查客户状态

**预期结果**:
- 不发送回收预警
- 客户保持原状态
- 不被回收

**实际结果**:
- [ ] 通过
- [ ] 失败

**备注**:
________________________________________

### TC-004: 回收预警机制
**测试目标**: 验证回收预警提前通知功能
**前置条件**:
1. 测试客户处于"方案沟通"阶段
2. 最后跟进时间为18天前（阈值21天，预警提前3天）

**测试步骤**:
1. 执行回收定时任务
2. 检查预警通知
3. 验证预警内容

**预期结果**:
- 发送预警通知给销售
- 通知包含客户信息和预计回收时间
- 销售可以延长跟进时间

**实际结果**:
- [ ] 通过
- [ ] 失败

**备注**:
________________________________________

### TC-005: 手动回收功能
**测试目标**: 验证手动回收功能正常
**前置条件**:
1. 测试客户处于任意阶段
2. 销售有回收权限

**测试步骤**:
1. 进入客户详情页
2. 点击手动回收按钮
3. 选择回收原因并确认
4. 检查客户状态

**预期结果**:
- 回收成功
- 客户进入公海
- 记录回收日志

**实际结果**:
- [ ] 通过
- [ ] 失败

**备注**:
________________________________________

### TC-006: 数据一致性测试
**测试目标**: 验证回收过程数据一致性
**前置条件**:
1. 多个测试客户
2. 不同商机阶段
3. 不同最后跟进时间

**测试步骤**:
1. 批量执行回收任务
2. 检查数据库一致性
3. 验证业务逻辑正确性

**预期结果**:
- 数据一致，无脏数据
- 业务逻辑正确执行
- 日志记录完整

**实际结果**:
- [ ] 通过
- [ ] 失败

**备注**:
________________________________________

### TC-007: 性能测试
**测试目标**: 验证回收任务性能
**前置条件**:
1. 10万测试客户数据
2. 不同阶段分布

**测试步骤**:
1. 执行回收定时任务
2. 监控执行时间
3. 监控系统资源

**预期结果**:
- 执行时间 < 5分钟
- CPU使用率 < 80%
- 内存使用正常

**实际结果**:
- [ ] 通过
- [ ] 失败

**备注**:
________________________________________

## 测试结果汇总

| 测试用例 | 测试结果 | 测试人员 | 测试时间 | 备注 |
|----------|----------|----------|----------|------|
| TC-001 |          |          |          |      |
| TC-002 |          |          |          |      |
| TC-003 |          |          |          |      |
| TC-004 |          |          |          |      |
| TC-005 |          |          |          |      |
| TC-006 |          |          |          |      |
| TC-007 |          |          |          |      |

## 总体测试结论
- [ ] 所有测试用例通过
- [ ] 主要功能测试通过
- [ ] 性能测试达标
- [ ] 建议上线

## 签字确认
- 测试人员: _________ 日期: _________
- 开发人员: _________ 日期: _________
- 产品人员: _________ 日期: _________
EOF

echo "测试用例已生成: 03_测试验证/测试用例.md"

echo ""
echo "步骤5: 生成实施计划"
echo "--------------------------------"

# 生成实施计划
cat > 04_实施计划/详细实施计划.md <<