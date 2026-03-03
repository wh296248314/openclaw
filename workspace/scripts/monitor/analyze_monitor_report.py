#!/usr/bin/env python3
import re

with open('guardian_monitor_20260303_165220.log', 'r') as f:
    content = f.read()

print("🎯 监控卫士30分钟运行分析:")
print("=" * 50)

# 分析进程稳定性
process_checks = re.findall(r'监控进程运行正常|监控进程已停止|PID文件不存在', content)
normal_checks = process_checks.count('监控进程运行正常')
total_checks = len(process_checks)

print(f"\n1. 进程稳定性: {normal_checks}/{total_checks} 次检查正常")
if normal_checks == total_checks:
    print("   ✅ 进程稳定运行，无重启")
else:
    print("   ⚠️  进程有异常")

# 分析告警数量
warnings = re.findall(r'WARNING|ERROR|CRITICAL', content)
print(f"\n2. 告警数量: {len(warnings)} 次")
if len(warnings) == 0:
    print("   ✅ 无误报告警（好现象）")
else:
    print(f"   ⚠️  发现告警: {warnings}")

# 分析系统资源
cpu_values = re.findall(r'CPU:\s*([\d.]+)%', content)
mem_values = re.findall(r'内存:\s*([\d.]+)%', content)

if cpu_values and mem_values:
    avg_cpu = sum(float(v) for v in cpu_values) / len(cpu_values)
    avg_mem = sum(float(v) for v in mem_values) / len(mem_values)
    print(f"\n3. 平均系统资源:")
    print(f"   CPU: {avg_cpu:.1f}%")
    print(f"   内存: {avg_mem:.1f}%")
    
    if avg_cpu < 20 and avg_mem < 30:
        print("   ✅ 资源占用正常")
    else:
        print("   ⚠️  资源占用较高")

# 检查任务状态
task_counts = re.findall(r'活跃任务:\s*(\d+)\s*个', content)
if task_counts:
    print(f"\n4. 任务监控:")
    print(f"   活跃任务数变化: {task_counts}")
    if all(count == '0' for count in task_counts):
        print("   ⚠️  无活跃任务（可能任务被自动清理）")

print("\n" + "=" * 50)
print("🎯 总体评价:")
if normal_checks == total_checks and len(warnings) == 0:
    print("✅ 监控卫士运行稳定，无异常告警")
else:
    print("⚠️  监控卫士运行有异常，需要进一步检查")

print("\n💡 建议:")
print("1. 添加任务持久化，防止重启丢失任务")
print("2. 完善僵死任务检测机制")
print("3. 配置钉钉通知进行实际告警测试")
