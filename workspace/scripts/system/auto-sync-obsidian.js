#!/usr/bin/env node

// Obsidian 自动同步监控脚本
// 监控 memory/YYYY-MM-DD.md 文件变化，自动同步到 Obsidian

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const WORKSPACE_DIR = '/home/admin/openclaw/workspace';
const MEMORY_DIR = path.join(WORKSPACE_DIR, 'memory');
const SYNC_SCRIPT = path.join(WORKSPACE_DIR, 'sync-obsidian-daily.sh');

// 获取今天的日期
const today = new Date();
const year = today.getFullYear();
const month = String(today.getMonth() + 1).padStart(2, '0');
const day = String(today.getDate()).padStart(2, '0');
const todayStr = `${year}-${month}-${day}`;

const todayFile = path.join(MEMORY_DIR, `${todayStr}.md`);
const stateFile = path.join(WORKSPACE_DIR, 'obsidian-sync-state.json');

console.log(`📅 今天: ${todayStr}`);
console.log(`📁 监控文件: ${todayFile}`);
console.log(`📜 同步脚本: ${SYNC_SCRIPT}`);

// 检查文件是否存在
if (!fs.existsSync(todayFile)) {
  console.log('⚠️ 今日记忆文件不存在，创建基础模板...');
  
  const template = `# ${todayStr} 工作记录

## ✅ 已完成任务

## 📋 进行中任务

## 🔄 待处理

## 📝 系统配置与更新

## 💭 想法与笔记
`;
  
  fs.writeFileSync(todayFile, template, 'utf8');
  console.log('✅ 已创建今日记忆文件');
}

// 读取当前文件状态
let lastState = {};
if (fs.existsSync(stateFile)) {
  try {
    lastState = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
  } catch (e) {
    console.log('⚠️ 状态文件损坏，重新创建');
  }
}

// 获取文件信息
const stats = fs.statSync(todayFile);
const currentState = {
  mtime: stats.mtimeMs,
  size: stats.size,
  contentHash: require('crypto').createHash('md5').update(fs.readFileSync(todayFile, 'utf8')).digest('hex')
};

// 检查是否有变化
const lastFileState = lastState[todayStr];
let shouldSync = false;

if (!lastFileState) {
  console.log('🆕 首次同步今日文件');
  shouldSync = true;
} else if (lastFileState.mtime !== currentState.mtime || 
           lastFileState.size !== currentState.size ||
           lastFileState.contentHash !== currentState.contentHash) {
  console.log('🔄 检测到文件变化，需要同步');
  console.log(`   修改时间: ${lastFileState.mtime} → ${currentState.mtime}`);
  console.log(`   文件大小: ${lastFileState.size} → ${currentState.size}`);
  shouldSync = true;
} else {
  console.log('📭 文件无变化，跳过同步');
}

// 执行同步
if (shouldSync) {
  try {
    console.log('🚀 开始执行同步...');
    const output = execSync(SYNC_SCRIPT, { encoding: 'utf8' });
    console.log(output);
    
    // 更新状态
    lastState[todayStr] = currentState;
    fs.writeFileSync(stateFile, JSON.stringify(lastState, null, 2), 'utf8');
    
    console.log('✅ 同步完成，状态已更新');
  } catch (error) {
    console.error('❌ 同步失败:', error.message);
    if (error.stderr) console.error('错误输出:', error.stderr.toString());
    if (error.stdout) console.error('标准输出:', error.stdout.toString());
  }
}

console.log('🎯 Obsidian 自动同步监控完成');