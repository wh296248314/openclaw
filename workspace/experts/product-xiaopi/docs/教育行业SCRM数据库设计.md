# 教育行业SCRM数据库设计

**整理时间：** 2026-03-23
**状态说明：** ✅ 已确认 | 🔄 待完善 | ⚠️ 待调整

---

## 一、核心四状态定义

### 状态流转图
```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  资源   │───▶│  线索   │───▶│  商机   │───▶│  转化   │───▶│  流失   │
│  Lead   │    │  Opp   │    │  Deal   │    │ 成交    │    │  Churn  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │              │
     │              │              │              │
     ▼              ▼              ▼              ▼
  联系方式       有手机号       五要素齐全       已缴费
  非手机号       或微信                       已入读
```

### 状态定义

| 状态 | 定义 | 判断标准 |
|------|------|----------|
| **资源** | 不同渠道留资，联系方式非手机号 | 微信号、邮箱等 |
| **线索** | 有手机号或已加微信的客户 | 联系方式获取 |
| **商机** | 五要素齐全的客户 | 姓名+手机号+年级+公立校+意向 |
| **转化** | 已完成支付报名 | 订单+支付+学员档案 |
| **流失** | 不再续费或退费 | 退费/到期不续 |

---

## 二、资源流转流程图

### 资源从哪里来
```
┌─────────────────────────────────────────────────────────────────┐
│                         资源来源渠道                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│   │ 渠道活码 │  │ 广告投放  │  │ 线下活动 │  │ 合作渠道 │      │
│   └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘      │
│        │              │              │              │             │
│        ▼              ▼              ▼              ▼             │
│   ┌─────────────────────────────────────────────────────────┐    │
│   │                    资源入库                             │    │
│   │         （微信号/邮箱/其他联系方式）                    │    │
│   └─────────────────────────────────────────────────────────┘    │
│                            │                                     │
│                            ▼                                     │
│   ┌─────────────────────────────────────────────────────────┐    │
│   │                   资源待跟进                            │    │
│   │              （等待获取手机号）                         │    │
│   └─────────────────────────────────────────────────────────┘    │
│                            │                                     │
│          ┌────────────────┼────────────────┐                    │
│          ▼                                 ▼                    │
│   ┌─────────────┐                  ┌─────────────┐              │
│   │ 获取手机号  │                  │  无法获取    │              │
│   │ 转为线索    │                  │  资源作废   │              │
│   └──────┬──────┘                  └─────────────┘              │
│          │                                                       │
│          ▼                                                       │
│   ┌─────────────┐                                               │
│   │  进入线索池  │                                               │
│   └─────────────┘                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 三、资源跟进流程图

### 线索跟进流程
```
┌─────────────────────────────────────────────────────────────────┐
│                         线索跟进流程                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐                                               │
│   │  新线索分配  │                                               │
│   └──────┬──────┘                                               │
│          │                                                       │
│          ▼                                                       │
│   ┌─────────────┐     ┌─────────────┐                           │
│   │  分配给谁？  │────▶│  指定跟进人 │                           │
│   └─────────────┘     └──────┬──────┘                           │
│          │                     │                                   │
│          │            ┌────────┴────────┐                        │
│          │            ▼                 ▼                        │
│          │     ┌───────────┐     ┌───────────┐                  │
│          │     │ 销售顾问   │     │  销售主管  │                  │
│          │     └───────────┘     └───────────┘                  │
│          │                                                       │
│          ▼                                                       │
│   ┌─────────────┐                                               │
│   │  首次跟进    │                                               │
│   └──────┬──────┘                                               │
│          │                                                       │
│          ▼                                                       │
│   ┌─────────────────────────────────────────┐                   │
│   │              跟进阶段                     │                   │
│   ├─────────────────────────────────────────┤                   │
│   │  未跟进 → 初步接触 → 需求确认 → 方案制定 │                   │
│   │       → 价格洽谈 → 合同签署 → 已签约     │                   │
│   └─────────────────────────────────────────┘                   │
│                            │                                      │
│          ┌────────────────┼────────────────┐                    │
│          ▼                ▼                ▼                    │
│   ┌───────────┐   ┌───────────┐   ┌───────────┐                │
│   │   成单     │   │  继续跟进  │   │   流失    │                │
│   │  转为商机  │   │  保持跟进  │   │  进入流失 │                │
│   └───────────┘   └───────────┘   └───────────┘                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 四、资源回收流程图

### 公海池回收机制
```
┌─────────────────────────────────────────────────────────────────┐
│                        资源回收流程                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐                                               │
│   │   私海池    │                                               │
│   │  (顾问持有) │                                               │
│   └──────┬──────┘                                               │
│          │                                                       │
│          │ 超过X天未跟进                                        │
│          ▼                                                       │
│   ┌─────────────┐                                               │
│   │  提醒顾问   │                                               │
│   │  继续跟进   │                                               │
│   └──────┬──────┘                                               │
│          │                                                       │
│          │ 超过Y天仍未跟进                                       │
│          ▼                                                       │
│   ┌─────────────────────────────────────────┐                   │
│   │              自动回收                    │                   │
│   │         进入公海池（可被认领）          │                   │
│   └─────────────────────────────────────────┘                   │
│                            │                                      │
│          ┌────────────────┼────────────────┐                    │
│          ▼                ▼                ▼                    │
│   ┌───────────┐   ┌───────────┐   ┌───────────┐                  │
│   │  被认领    │   │  长期未   │   │   自然    │                  │
│   │  进入新私海 │   │  认领     │   │   流失    │                  │
│   └───────────┘   └───────────┘   └───────────┘                  │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│                                                                  │
│   回收规则：                                                     │
│   - 顾问持有的线索，超过X天未跟进 → 回收至公海                   │
│   - 公海线索超过Z天未被认领 → 标记为无效资源                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 五、商机状态流转图

### 商机全生命周期
```
┌─────────────────────────────────────────────────────────────────┐
│                       商机状态流转                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────────────────────────────────────────────────┐    │
│   │                    创建商机                             │    │
│   │            （资源/线索 → 填写五要素）                   │    │
│   └─────────────────────────┬───────────────────────────────┘    │
│                             │                                      │
│                             ▼                                      │
│   ┌─────────────────────────────────────────────────────────┐    │
│   │                    跟进中                                │    │
│   │         (未跟进/跟进未转化)                            │    │
│   └─────────────────────────┬───────────────────────────────┘    │
│                             │                                      │
│          ┌─────────────────┼─────────────────┐                    │
│          ▼                 ▼                 ▼                    │
│   ┌───────────┐   ┌───────────┐   ┌───────────┐                 │
│   │   成单     │   │   转移    │   │   放弃    │                 │
│   │ (已成单)  │   │ (转移他人)│   │ (主动放弃)│                 │
│   └──────┬────┘   └──────┬────┘   └──────┬────┘                 │
│          │                │                │                     │
│          ▼                │                ▼                     │
│   ┌───────────┐            │          ┌───────────┐              │
│   │  创建订单  │            │          │   关单    │              │
│   │  自动关单  │            │          │ (close)  │              │
│   └───────────┘            │          └───────────┘              │
│                            │                                    │
│                            ▼                                    │
│                      ┌───────────┐                              │
│                      │   关单     │                              │
│                      │ 原因记录   │                              │
│                      └───────────┘                              │
│                                                                  │
│  商机唯一性规则：同一客户 + 同一校区 = 只有一个商机              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 六、表结构设计

### 1. 资源表（resource）✅

| 字段 | 类型 | 说明 |
|------|------|------|
| resource_id | BIGINT | 资源ID |
| source_channel | VARCHAR | 来源渠道 |
| source_detail | VARCHAR | 来源详情 |
| contact_type | VARCHAR | 联系方式类型 |
| contact_value | VARCHAR | 联系方式值 |
| channel_code | VARCHAR | 渠道码/场景值 |
| get_method | VARCHAR | 获取方式 |
| get_time | DATETIME | 获取时间 |
| get_user_id | BIGINT | 获取人 |
| ext_system | VARCHAR | 来源系统 |
| activity_id | BIGINT | 关联活动ID |
| activity_name | VARCHAR | 活动名称 |
| activity_type | VARCHAR | 活动类型 |
| activity_time | DATETIME | 活动时间 |
| customer_id | BIGINT | 关联客户ID |
| status | TINYINT | 状态 |
| remark | TEXT | 备注 |
| created_at | DATETIME | 创建时间 |

---

### 2. 线索表（lead）✅

| 字段 | 类型 | 说明 |
|------|------|------|
| lead_id | BIGINT | 线索ID |
| customer_id | BIGINT | 关联客户ID |
| create_user_id | BIGINT | 创建人/导入人 |
| create_dept_id | BIGINT | 创建人部门 |
| assign_user_id | BIGINT | 分配给谁 |
| assign_dept_id | BIGINT | 分配部门 |
| follow_user_id | BIGINT | 跟进人 |
| follow_dept_id | BIGINT | 跟进部门 |
| activity_id | BIGINT | 关联活动ID |
| phone | VARCHAR | 手机号 |
| wechat | VARCHAR | 微信 |
| source_channel | VARCHAR | 来源渠道 |
| source_detail | VARCHAR | 来源详情 |
| channel_code | VARCHAR | 渠道码 |
| activity_name | VARCHAR | 活动名称 |
| get_method | VARCHAR | 获取方式 |
| get_time | DATETIME | 获取时间 |
| assign_time | DATETIME | 分配时间 |
| follow_count | INT | 跟进次数 |
| last_follow_time | DATETIME | 最后跟进时间 |
| next_follow_time | DATETIME | 下次跟进时间 |
| last_follow_remark | TEXT | 最后跟进备注 |
| follow_record | TEXT | 跟进记录 |
| call_status | TINYINT | 接线状态 |
| is_blacklist | TINYINT | 是否黑名单 |
| intent_level | TINYINT | 意向等级 |
| intent_product | VARCHAR | 意向产品 |
| status | TINYINT | 状态 |
| invalid_reason | VARCHAR | 无效原因 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

### 3. 客户表（customer）✅

| 字段 | 类型 | 说明 |
|------|------|------|
| customer_id | BIGINT | 客户ID |
| name | VARCHAR | 客户姓名 |
| phone | VARCHAR | 主手机号 |
| father_phone | VARCHAR | 爸爸手机号 |
| mother_phone | VARCHAR | 妈妈手机号 |
| other_phone | VARCHAR | 其他手机号 |
| wechat | VARCHAR | 微信 |
| relation | VARCHAR | 与学员关系 |
| source_channel | VARCHAR | 一级渠道 |
| source_sub_channel | VARCHAR | 二级渠道 |
| source_system | VARCHAR | 来源系统 |
| biz_dept_id | BIGINT | 事业部门ID |
| branch_id | BIGINT | 分校ID |
| line_id | BIGINT | 条线ID |
| campus_id | BIGINT | 校区ID |
| status | TINYINT | 状态 |
| created_at | DATETIME | 创建时间 |

---

### 4. 学员表（student）✅

| 字段 | 类型 | 说明 |
|------|------|------|
| student_id | BIGINT | 学员ID |
| name | VARCHAR | 学员姓名 |
| current_grade | VARCHAR | 当前年级（学校年级）|
| enter_grade | VARCHAR | 进入年级（报名年级）|
| school | VARCHAR | 在读学校 |
| school_type | VARCHAR | 学校类型 |
| birthday | DATE | 出生日期 |
| gender | TINYINT | 性别 |
| status | TINYINT | 状态 |
| created_at | DATETIME | 创建时间 |

---

### 5. 学员客户关联表（student_customer）✅

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | ID |
| student_id | BIGINT | 学员ID |
| customer_id | BIGINT | 客户ID |
| relation | VARCHAR | 与学员关系 |
| is_primary | TINYINT | 是否主联系人 |

---

### 6. 商机表（opportunity）✅

| 字段 | 类型 | 说明 |
|------|------|------|
| opportunity_id | BIGINT | 商机ID |
| customer_id | BIGINT | 客户ID |
| student_id | BIGINT | 学员ID |
| student_name | VARCHAR | 学员姓名 |
| student_grade | VARCHAR | 学员年级 |
| student_school | VARCHAR | 公立学校 |
| customer_name | VARCHAR | 客户姓名 |
| customer_phone | VARCHAR | 客户手机号 |
| intent_course | VARCHAR | 意向课程 |
| intent_level | TINYINT | 意向等级 |
| intent_amount | DECIMAL | 意向金额 |
| biz_dept_id | BIGINT | 事业部门ID |
| branch_id | BIGINT | 分校ID |
| line_id | BIGINT | 条线ID |
| campus_id | BIGINT | 校区ID |
| activity_id | BIGINT | 关联活动ID |
| activity_name | VARCHAR | 活动名称 |
| follow_stage | VARCHAR | 跟进阶段 |
| follow_type | VARCHAR | 跟进方式 |
| follow_count | INT | 跟进次数 |
| last_follow_time | DATETIME | 最后跟进时间 |
| next_follow_time | DATETIME | 下次跟进时间 |
| last_follow_remark | TEXT | 最后跟进备注 |
| follow_record | TEXT | 跟进记录 |
| call_status | TINYINT | 接线状态 |
| call_record_url | VARCHAR | 录音地址 |
| follow_user_id | BIGINT | 跟进人 |
| follow_dept_id | BIGINT | 跟进部门 |
| order_id | BIGINT | 关联订单ID |
| close_reason | VARCHAR | 关单原因 |
| close_time | DATETIME | 关单时间 |
| status | TINYINT | 状态 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### 跟进阶段
- 未跟进
- 跟进未转化
- 已成单
- 已流失

#### 关单原因
- 已成单
- 转移
- 过期
- 放弃

#### 商机业务规则
1. 同一客户 + 同一校区 = 只有一个商机
2. 成单时自动关单
3. 转移时原商机关单
4. 超过有效期自动关单
5. 必须关单后才能再建新商机

---

### 7. 订单表（order）✅

| 字段 | 类型 | 说明 |
|------|------|------|
| order_id | BIGINT | 订单ID |
| order_no | VARCHAR | 订单号 |
| customer_id | BIGINT | 客户ID |
| student_id | BIGINT | 学员ID |
| opportunity_id | BIGINT | 商机ID |
| product_id | BIGINT | 产品ID |
| product_name | VARCHAR | 产品名称 |
| biz_dept_id | BIGINT | 事业部门ID |
| branch_id | BIGINT | 分校ID |
| line_id | BIGINT | 条线ID |
| campus_id | BIGINT | 校区ID |
| activity_id | BIGINT | 活动ID |
| activity_name | VARCHAR | 活动名称 |
| original_price | DECIMAL | 原价 |
| discount_amount | DECIMAL | 优惠金额 |
| actual_price | DECIMAL | 实收金额 |
| pay_type | VARCHAR | 支付方式 |
| pay_time | DATETIME | 支付时间 |
| status | TINYINT | 状态 |
| created_at | DATETIME | 创建时间 |

---

### 8. 机构表（organization）✅

| 字段 | 类型 | 说明 |
|------|------|------|
| org_id | BIGINT | 机构ID |
| org_name | VARCHAR | 机构名称 |
| org_type | VARCHAR | 机构类型 |
| parent_id | BIGINT | 上级机构ID |
| level | INT | 层级深度 |
| path | VARCHAR | 路径 |
| status | TINYINT | 状态 |
| created_at | DATETIME | 创建时间 |

#### 机构类型
- 分校
- 条线
- 部门
- 分区
- 校区
- 人员

#### 层级结构
```
分校 → 条线 → 部门 → 分区 → 校区 → 部门 → 人员
```

#### 数据权限规则
上级可以看到下级的数据，下级看不到上级的数据

---

### 9. 流失表（churn）✅

| 字段 | 类型 | 说明 |
|------|------|------|
| churn_id | BIGINT | 流失ID |
| customer_id | BIGINT | 客户ID |
| student_id | BIGINT | 学员ID |
| order_id | BIGINT | 最后订单ID |
| biz_dept_id | BIGINT | 事业部门ID |
| branch_id | BIGINT | 分校ID |
| line_id | BIGINT | 条线ID |
| campus_id | BIGINT | 校区ID |
| churn_type | VARCHAR | 流失类型 |
| churn_reason | VARCHAR | 流失原因 |
| last_order_time | DATETIME | 最后订单时间 |
| last_follow_time | DATETIME | 最后跟进时间 |
| last_class_time | DATETIME | 最后上课时间 |
| can_reach | TINYINT | 是否可召回 |
| is_return | TINYINT | 是否回流 |
| status | TINYINT | 状态 |
| created_at | DATETIME | 创建时间 |

#### 流失类型
- 退费
- 不再续费

---

### 10. 用户表（user）⚠️ 待调整

| 字段 | 类型 | 说明 |
|------|------|------|
| user_id | BIGINT | 用户ID |
| name | VARCHAR | 姓名 |
| dept_id | BIGINT | 部门ID |
| dept_name | VARCHAR | 部门名称 |
| role | VARCHAR | 角色 |
| phone | VARCHAR | 手机号 |
| wechat | VARCHAR | 微信 |
| work_wechat | VARCHAR | 企业微信 |
| email | VARCHAR | 邮箱 |
| status | TINYINT | 状态 |
| created_at | DATETIME | 创建时间 |

> ⚠️ 待完善：可能还需要调整字段

---

### 11. 活动表（activity）🔄 待完善

| 字段 | 类型 | 说明 |
|------|------|------|
| activity_id | BIGINT | 活动ID |
| activity_name | VARCHAR | 活动名称 |
| activity_type | VARCHAR | 活动类型 |
| activity_channel | VARCHAR | 活动渠道 |
| target_audience | VARCHAR | 目标人群 |
| start_time | DATETIME | 开始时间 |
| end_time | DATETIME | 结束时间 |
| location | VARCHAR | 活动地点 |
| budget | DECIMAL | 预算金额 |
| actual_cost | DECIMAL | 实际费用 |
| expected_leads | INT | 预期线索量 |
| actual_leads | INT | 实际线索量 |
| converted_leads | INT | 转化线索量 |
| roi | DECIMAL | ROI投入产出比 |
| create_user_id | BIGINT | 创建人 |
| create_dept_id | BIGINT | 创建部门 |
| owner_dept | VARCHAR | 负责部门 |
| status | TINYINT | 状态 |
| remark | TEXT | 备注 |
| created_at | DATETIME | 创建时间 |

> 🔄 待完善：活动规则、活动与渠道的关联等

---

### 12. 产品表（product）- 对接外部系统 ✅

| 字段 | 类型 | 说明 |
|------|------|------|
| product_id | BIGINT | 产品ID |
| product_name | VARCHAR | 产品名称 |
| line_id | BIGINT | 条线ID |
| subject | VARCHAR | 科目 |
| grade_range | VARCHAR | 适用年级范围 |
| price | DECIMAL | 价格 |
| status | TINYINT | 状态 |
| ext_id | VARCHAR | 外部系统产品ID |
| sync_time | DATETIME | 同步时间 |

---

### 13. 班级表（class）- 对接外部系统 ✅

| 字段 | 类型 | 说明 |
|------|------|------|
| class_id | BIGINT | 班级ID |
| class_name | VARCHAR | 班级名称 |
| product_id | BIGINT | 产品ID |
| teacher_id | BIGINT | 老师ID |
| campus_id | BIGINT | 校区ID |
| start_time | DATETIME | 开课时间 |
| end_time | DATETIME | 结束时间 |
| status | TINYINT | 状态 |
| ext_id | VARCHAR | 外部系统班级ID |
| sync_time | DATETIME | 同步时间 |

---

### 14. 测评表（assessment）- 对接外部系统 ✅

| 字段 | 类型 | 说明 |
|------|------|------|
| assessment_id | BIGINT | 测评ID |
| student_id | BIGINT | 学员ID |
| assessment_type | VARCHAR | 测评类型 |
| score | DECIMAL | 分数 |
| result | TEXT | 测评结果 |
| ext_id | VARCHAR | 外部系统测评ID |
| sync_time | DATETIME | 同步时间 |

---

## 七、ER图

### 完整实体关系图
```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│   ┌──────────────┐                                                      │
│   │  organization │                                                      │
│   │   机构表      │                                                      │
│   └──────┬───────┘                                                      │
│          │ N                                                            │
│          │                                                              │
│          ▼                                                              │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                                                                 │  │
│   │   ┌──────────────┐         ┌──────────────────────┐            │  │
│   │   │   customer    │         │ student_customer    │            │  │
│   │   │   客户表      │────────│   学员客户关联表    │───────────│  │
│   │   └──────┬───────┘    N   └──────────────────────┘   N        │  │
│   │          │                        │                             │  │
│   │          │ N                     │                             │  │
│   │          ▼                        ▼                             │  │
│   │   ┌──────────────┐         ┌──────────────┐                   │  │
│   │   │  opportunity  │         │   student    │                   │  │
│   │   │   商机表      │         │   学员表      │                   │  │
│   │   └──────┬───────┘         └──────────────┘                   │  │
│   │          │                                                     │  │
│   │          │ N                     N                              │  │
│   │          ▼                           ▼                           │  │
│   │   ┌──────────────┐         ┌──────────────┐                   │  │
│   │   │    order     │         │   churn      │                   │  │
│   │   │   订单表      │         │   流失表      │                   │  │
│   │   └──────────────┘         └──────────────┘                   │  │
│   │          │                                                     │  │
│   │          │ N                                                   │  │
│   │          ▼                                                     │  │
│   │   ┌──────────────┐                                             │  │
│   │   │   resource   │                                             │  │
│   │   │   资源表      │                                             │  │
│   │   └──────────────┘                                             │  │
│   │          │                                                     │  │
│   │          │ N                                                   │  │
│   │          ▼                                                     │  │
│   │   ┌──────────────┐                                             │  │
│   │   │   -lead-     │                                             │  │
│   │   │   线索表      │                                             │  │
│   │   └──────────────┘                                             │  │
│   │                                                                 │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│   ┌──────────────┐         ┌──────────────┐         ┌──────────────┐  │
│   │  user        │         │  activity    │         │  product     │  │
│   │  用户表       │         │  活动表       │         │  产品表(对接) │  │
│   └──────────────┘         └──────────────┘         └──────────────┘  │
│                                                                         │
│   ┌──────────────┐         ┌──────────────┐                            │
│   │  class       │         │ assessment   │                            │
│   │  班级表(对接)│         │ 测评表(对接) │                            │
│   └──────────────┘         └──────────────┘                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 表关系说明

| 关联表 | 关联的两个实体 | 关系 |
|--------|---------------|------|
| customer_student | customer ↔ student | N:N |
| customer_opportunity | customer ↔ opportunity | N:N |
| customer_order | customer ↔ order | N:N |
| customer_churn | customer ↔ churn | N:N |

---

## 八、待完善清单

1. **用户表（user）** - ⚠️ 待调整，可能还需要调整字段
2. **活动表（activity）** - 🔄 待完善活动规则、渠道关联等

---

## 九、业务规则总结

### 客户与商机关系
- 一个客户 + 一个校区 = 只有一个商机
- 必须关单后才能新建商机

### 数据权限
- 上级可以看到下级的数据
- 下级看不到上级的数据

### 活动贯穿全流程
- 资源表 → 线索表 → 商机表 → 订单表
- 均可关联活动ID，实现全流程追溯

### 资源回收规则
- 顾问持有的线索，超过X天未跟进 → 回收至公海
- 公海线索超过Z天未被认领 → 标记为无效资源
