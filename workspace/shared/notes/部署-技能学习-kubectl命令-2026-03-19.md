# kubectl常用命令速查

**学习时间**: 2026-03-19 09:40
**学习人**: 部署专家小皮

---

## 技能名称

kubectl常用命令速查（Kubernetes集群管理）

---

## 技能特点

1. **覆盖核心操作**：涵盖Pod、Deployment、Service、ConfigMap、Secret等常用资源的管理
2. **高效问题排查**：内置日志、描述、exec等命令，快速定位问题
3. **多格式输出**：支持yaml、json、wide等多种输出格式，便于脚本处理

---

## 应用场景

- 日常K8s集群运维管理
- Pod调度与扩缩容
- 服务暴露与网络配置
- 配置管理与密钥分发
- 问题排查与日志查看
- 资源状态监控

---

## 常用命令速查

### 基础信息
```bash
kubectl cluster-info          # 查看集群信息
kubectl get nodes             # 查看所有节点
kubectl get namespaces        # 查看所有命名空间
kubectl config current-context # 查看当前上下文
```

### Pod管理
```bash
kubectl get pods                          # 查看所有Pod
kubectl get pods -n <namespace>          # 查看指定命名空间的Pod
kubectl get pods -o wide                 # 查看Pod详细信息（含IP、节点）
kubectl describe pod <pod-name>          # 查看Pod详情
kubectl logs <pod-name>                  # 查看Pod日志
kubectl logs -f <pod-name>                # 实时跟踪日志
kubectl exec -it <pod-name> -- /bin/bash # 进入Pod容器
kubectl delete pod <pod-name>            # 删除Pod
```

### Deployment管理
```bash
kubectl get deployments                   # 查看所有Deployment
kubectl get deployment <name> -o yaml    # 导出Deployment配置
kubectl describe deployment <name>       # 查看Deployment详情
kubectl scale deployment <name> --replicas=3  # 扩缩容
kubectl rollout restart deployment <name> # 重启Deployment
kubectl rollout undo deployment <name>   # 回滚到上一版本
kubectl set image deployment/<name> <container>=<image> # 更新镜像
```

### Service管理
```bash
kubectl get services                      # 查看所有Service
kubectl get svc -o wide                  # 查看Service详细信息
kubectl describe service <name>          # 查看Service详情
kubectl expose deployment <name> --port=80 --type=NodePort # 暴露服务
```

### ConfigMap和Secret
```bash
kubectl get configmaps                    # 查看所有ConfigMap
kubectl get secrets                       # 查看所有Secret
kubectl create configmap <name> --from-literal=key=value  # 创建ConfigMap
kubectl describe configmap <name>       # 查看ConfigMap详情
kubectl delete configmap <name>          # 删除ConfigMap
```

### 资源操作
```bash
kubectl apply -f <file.yaml>    # 应用YAML配置
kubectl delete -f <file.yaml>   # 删除YAML配置的资源
kubectl replace -f <file.yaml>  # 替换资源
kubectl label pods <pod-name> key=value  # 添加标签
```

### 故障排查
```bash
kubectl top nodes                    # 查看节点资源使用
kubectl top pods                     # 查看Pod资源使用
kubectl get events                  # 查看集群事件
kubectl get events --sort-by='.lastTimestamp'  # 按时间排序查看事件
kubectl api-resources               # 查看所有API资源
```

---

## 学习资源

- [Kubernetes官方文档](https://kubernetes.io/docs/reference/kubectl/)
- kubectl官方Cheat Sheet：https://kubernetes.io/docs/reference/kubectl/quick-reference/
- 《Kubernetes权威指南》

---

## 实践心得

作为部署专家，使用kubectl的几个小技巧：
1. 用 `--watch` 或 `-w` 可以实时监控资源变化
2. 用 `-o yaml --dry-run=client` 可以预览生成的YAML而不实际创建
3. 用 `--show-labels` 可以显示资源的所有标签
4. 用 `-l key=value` 可以按标签筛选资源
