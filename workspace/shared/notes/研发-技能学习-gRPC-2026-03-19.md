# 技能学习：gRPC 高性能RPC框架

## 基本信息
- **技能名称**: gRPC (Google Remote Procedure Call)
- **学习日期**: 2026-03-19
- **所属领域**: 分布式系统 / 微服务通信
- **技能类型**: 框架 / 协议

---

## 技能特点（3点）

### 1. 高性能二进制序列化
- 使用 **Protocol Buffers** 作为接口定义语言和消息序列化格式
- 二进制格式比JSON/XML小3-10倍，序列化/反序列化速度快20-100倍
- 支持流式传输（Server Streaming、Client Streaming、Bidirectional Streaming）

### 2. 强类型跨语言支持
- 通过 `.proto` 文件定义服务接口，实现语言无关
- 自动生成多语言客户端/服务端代码（Go、Java、Python、C++等）
- 一处定义，全端可用，确保API一致性

### 3. HTTP/2 底层支持
- 多路复用：单个TCP连接并行处理多个请求
- 双向流：客户端和服务端可以同时发送数据
- 内置流量控制、压缩和连接复用，性能远超HTTP/1.1

---

## 应用场景

### 适用场景
- **微服务间通信**：服务网格（Istio、gRPC-Web）
- **移动端API**：低带宽、低延迟的移动数据传输
- **实时通信**：流式数据处理、直播推流
- **跨语言系统**：Python服务调用Go服务、Java调用Node.js

### 不适用场景
- 浏览器直接调用（需要gRPC-Web代理）
- 公开API（推荐REST/GraphQL）
- 简单CRUD操作（Overkill）

---

## 在我们项目中的潜在应用

基于SCRM项目特点，gRPC可应用于：
1. **用户服务 ↔ 订单服务** 内部通信
2. **消息队列选型**：gRPC替代部分Kafka场景
3. **实时通知**：用户行为事件流

---

## 学习资源

### 官方文档
- 官网：https://grpc.io/
- 文档：https://grpc.io/docs/
- Protocol Buffers：https://protobuf.dev/

### GitHub官方仓库
- https://github.com/grpc/grpc

### 快速入门
1. 安装 protoc 编译器
2. 安装对应语言的 gRPC 插件
3. 定义 .proto 文件
4. 生成代码并实现服务

### 推荐学习路径
1. 先学 Protocol Buffers 基础
2. 理解 gRPC 四种调用模式（Unary/Server/Client/Bidi）
3. 用 Go 或 Python 写一个简单 Demo
4. 了解 gRPC 与 REST 的对比和迁移策略

---

## 相关技能扩展
- **Protocol Buffers**: 接口定义语言
- **HTTP/2**: 底层传输协议
- **Envoy**: gRPC-Web代理和负载均衡
- **gRPC-Gateway**: 将gRPC转REST的工具
