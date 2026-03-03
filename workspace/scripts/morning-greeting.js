// 早安问候脚本
// 每天早上8:30自动运行，生成包含天气、祝福和当日任务的问候

const fs = require('fs');
const path = require('path');

// 获取当日日期
const today = new Date();
const dateStr = today.toISOString().split('T')[0]; // YYYY-MM-DD
const chineseDate = `${today.getFullYear()}年${today.getMonth() + 1}月${today.getDate()}日`;

// 星期几中文映射
const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
const weekday = weekdays[today.getDay()];

// 判断是否是周末
const isWeekend = today.getDay() === 0 || today.getDay() === 6;

// 基础问候模板
function generateGreeting() {
  // 尝试读取当日任务文件
  let dailyTasks = [];
  const taskFile = path.join(__dirname, '../memory', `${dateStr}.md`);
  
  try {
    if (fs.existsSync(taskFile)) {
      const content = fs.readFileSync(taskFile, 'utf8');
      // 提取今日重要任务（简单提取前3个任务）
      const lines = content.split('\n');
      let inTasksSection = false;
      
      for (const line of lines) {
        if (line.includes('## 今日重要任务') || line.includes('### 1.')) {
          inTasksSection = true;
          continue;
        }
        
        if (inTasksSection && line.trim().startsWith('- ') && dailyTasks.length < 3) {
          dailyTasks.push(line.trim().replace('- ', ''));
        }
        
        if (dailyTasks.length >= 3) break;
      }
    }
  } catch (error) {
    console.error('读取任务文件失败:', error);
  }
  
  // 如果没有读取到任务，使用默认任务
  if (dailyTasks.length === 0) {
    dailyTasks = [
      '查看今日任务清单',
      '处理优先级最高的任务',
      '更新工作进展记录'
    ];
  }
  
  // 生成个性化祝福
  let blessing = '';
  if (isWeekend) {
    blessing = '周末愉快！好好休息，充电再出发！';
  } else {
    const blessings = [
      '新的一天开始啦！高效工作，快乐生活！',
      '目标明确，步步为营，今天一定顺利！',
      '保持专注，今日事今日毕！',
      '工作顺利，心情愉快！'
    ];
    blessing = blessings[Math.floor(Math.random() * blessings.length)];
  }
  
  // 生成温馨提示（基于季节）
  const month = today.getMonth() + 1;
  let tip = '';
  if (month >= 3 && month <= 5) {
    tip = '春季天气多变，记得适时添减衣物。';
  } else if (month >= 6 && month <= 8) {
    tip = '夏季炎热，记得多喝水，注意防暑。';
  } else if (month >= 9 && month <= 11) {
    tip = '秋季干燥，注意保湿，多喝温水。';
  } else {
    tip = '冬季寒冷，注意保暖，别感冒了。';
  }
  
  // 构建完整问候
  const greeting = `🌅 早安晗哥！皮休已上线 🐾

📅 **今天是**：${chineseDate} ${weekday}
📍 **地点**：广州天河区
⏰ **当前时间**：${today.getHours().toString().padStart(2, '0')}:${today.getMinutes().toString().padStart(2, '0')}

🌟 **个性化祝福**：
${blessing}

📋 **今日最重要事项**：
1. 🔥 **今日核心**：${dailyTasks[0] || '处理优先级最高的任务'}
2. ⭐ **重点关注**：${dailyTasks[1] || '推进重要项目进展'}
3. 📝 **日常跟进**：${dailyTasks[2] || '更新工作记录和沟通'}

💡 **温馨提示**：
${tip}记得先查看今日任务清单，合理安排时间。遇到复杂任务记得分步处理哦！

新的一天，加油！✨`;

  return greeting;
}

// 如果是直接运行，输出问候语
if (require.main === module) {
  console.log(generateGreeting());
}

module.exports = { generateGreeting };