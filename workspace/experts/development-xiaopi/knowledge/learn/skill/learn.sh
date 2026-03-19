#!/bin/bash
# 学习工作流脚本
# 定期执行技能发现和推荐

WORKSPACE="/home/pixiu/.openclaw/workspace/experts/development-xiaopi"
CONFIG_FILE="$WORKSPACE/learn/config.yaml"
LOG_FILE="$WORKSPACE/learn/logs/learning.log"

# 确保日志目录存在
mkdir -p "$WORKSPACE/learn/logs"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 读取配置中的领域
get_domains() {
    # 简单解析YAML获取领域名称
    grep -A 1 "name:" "$CONFIG_FILE" | grep -v "name:" | sed 's/^[ \t]*- //' | sed 's/^[ \t]*//'
}

# 搜索技能
search_skills() {
    local domain=$1
    local keywords=$(grep -A 20 "name: $domain" "$CONFIG_FILE" | grep "keywords:" -A 10 | grep -v "keywords:" | head -5)
    
    log "搜索领域: $domain"
    
    for kw in $keywords; do
        log "  搜索关键词: $kw"
        clawhub search "$kw" --no-input 2>/dev/null | head -10
    done
}

# 主函数
main() {
    log "========== 开始学习任务 =========="
    
    if [ ! -f "$CONFIG_FILE" ]; then
        log "错误: 配置文件不存在"
        exit 1
    fi
    
    # 获取所有领域
    domains=$(get_domains)
    
    for domain in $domains; do
        log "处理领域: $domain"
        search_skills "$domain"
    done
    
    log "========== 学习任务完成 =========="
}

main "$@"
