#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRM数据导入工具
用于处理成长数据和亲子数据导入到SCRM系统
"""

import pandas as pd
import os
import sys
from datetime import datetime
import json

class SCRMDataImporter:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report = {
            "import_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "佳琪老师",
            "data_provider": "泽彬",
            "growth_data": {},
            "parent_child_data": {},
            "summary": {}
        }
    
    def validate_growth_data(self, file_path):
        """验证成长数据文件"""
        print(f"验证成长数据文件: {file_path}")
        
        try:
            # 根据文件扩展名读取数据
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, encoding='utf-8')
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("不支持的文件格式，请使用CSV或Excel文件")
            
            # 检查必填字段
            required_fields = [
                '学员ID', '学员姓名', '家长联系方式', '课程名称',
                '退费金额', '退费原因', '退费日期', '经办人', '校区'
            ]
            
            missing_fields = []
            for field in required_fields:
                if field not in df.columns:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"警告：缺少必填字段: {missing_fields}")
            
            # 统计信息
            total_records = len(df)
            valid_records = df.dropna(subset=required_fields).shape[0]
            invalid_records = total_records - valid_records
            
            self.report["growth_data"] = {
                "file_name": os.path.basename(file_path),
                "total_records": total_records,
                "valid_records": valid_records,
                "invalid_records": invalid_records,
                "missing_fields": missing_fields,
                "data_preview": df.head(3).to_dict('records')
            }
            
            print(f"成长数据验证完成:")
            print(f"  总记录数: {total_records}")
            print(f"  有效记录: {valid_records}")
            print(f"  无效记录: {invalid_records}")
            
            return df, missing_fields
            
        except Exception as e:
            print(f"验证成长数据时出错: {str(e)}")
            return None, []
    
    def validate_parent_child_data(self, file_path):
        """验证亲子数据文件"""
        print(f"验证亲子数据文件: {file_path}")
        
        try:
            # 根据文件扩展名读取数据
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, encoding='utf-8')
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("不支持的文件格式，请使用CSV或Excel文件")
            
            # 检查必填字段
            required_fields = [
                '亲子ID', '家长姓名', '联系方式', '宝宝姓名', '宝宝年龄',
                '课程名称', '退费金额', '退费原因', '退费日期', '经办人', '校区'
            ]
            
            missing_fields = []
            for field in required_fields:
                if field not in df.columns:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"警告：缺少必填字段: {missing_fields}")
            
            # 统计信息
            total_records = len(df)
            valid_records = df.dropna(subset=required_fields).shape[0]
            invalid_records = total_records - valid_records
            
            self.report["parent_child_data"] = {
                "file_name": os.path.basename(file_path),
                "total_records": total_records,
                "valid_records": valid_records,
                "invalid_records": invalid_records,
                "missing_fields": missing_fields,
                "data_preview": df.head(3).to_dict('records')
            }
            
            print(f"亲子数据验证完成:")
            print(f"  总记录数: {total_records}")
            print(f"  有效记录: {valid_records}")
            print(f"  无效记录: {invalid_records}")
            
            return df, missing_fields
            
        except Exception as e:
            print(f"验证亲子数据时出错: {str(e)}")
            return None, []
    
    def generate_import_template(self, data_type="growth"):
        """生成SCRM系统导入模板"""
        print(f"生成{data_type}数据导入模板...")
        
        if data_type == "growth":
            template_data = {
                "学员ID": "",
                "学员姓名": "",
                "家长联系方式": "",
                "课程名称": "",
                "退费金额": "",
                "退费原因": "",
                "退费日期": "",
                "经办人": "",
                "校区": "",
                "备注": ""
            }
            filename = f"SCRM_成长数据导入模板_{self.timestamp}.xlsx"
        else:
            template_data = {
                "亲子ID": "",
                "家长姓名": "",
                "联系方式": "",
                "宝宝姓名": "",
                "宝宝年龄": "",
                "课程名称": "",
                "退费金额": "",
                "退费原因": "",
                "退费日期": "",
                "经办人": "",
                "校区": "",
                "备注": ""
            }
            filename = f"SCRM_亲子数据导入模板_{self.timestamp}.xlsx"
        
        # 创建DataFrame
        df = pd.DataFrame([template_data])
        
        # 保存为Excel文件
        df.to_excel(filename, index=False)
        print(f"导入模板已生成: {filename}")
        
        return filename
    
    def process_data_for_import(self, df, data_type="growth"):
        """处理数据为SCRM系统导入格式"""
        print(f"处理{data_type}数据为SCRM导入格式...")
        
        # 这里可以根据SCRM系统的具体要求进行数据转换
        # 例如：日期格式转换、金额格式转换、字段映射等
        
        processed_df = df.copy()
        
        # 示例：日期格式转换
        if '退费日期' in processed_df.columns:
            try:
                processed_df['退费日期'] = pd.to_datetime(processed_df['退费日期']).dt.strftime('%Y-%m-%d')
            except:
                pass
        
        # 示例：金额格式转换
        if '退费金额' in processed_df.columns:
            try:
                processed_df['退费金额'] = pd.to_numeric(processed_df['退费金额'], errors='coerce')
            except:
                pass
        
        output_filename = f"SCRM_{data_type}_数据_已处理_{self.timestamp}.xlsx"
        processed_df.to_excel(output_filename, index=False)
        
        print(f"处理后的数据已保存: {output_filename}")
        return output_filename
    
    def generate_import_report(self):
        """生成导入报告"""
        print("生成数据导入报告...")
        
        # 计算汇总信息
        growth_total = self.report["growth_data"].get("total_records", 0)
        growth_valid = self.report["growth_data"].get("valid_records", 0)
        parent_total = self.report["parent_child_data"].get("total_records", 0)
        parent_valid = self.report["parent_child_data"].get("valid_records", 0)
        
        total_records = growth_total + parent_total
        total_valid = growth_valid + parent_valid
        
        success_rate = (total_valid / total_records * 100) if total_records > 0 else 0
        
        self.report["summary"] = {
            "total_records": total_records,
            "total_valid_records": total_valid,
            "success_rate": round(success_rate, 2),
            "import_status": "待导入"  # 实际导入后更新为"已完成"
        }
        
        # 保存报告为JSON文件
        report_filename = f"SCRM数据导入报告_{self.timestamp}.json"
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(self.report, f, ensure_ascii=False, indent=2)
        
        # 生成文本报告
        txt_report = f"""SCRM数据导入报告
====================

导入时间: {self.report['import_time']}
操作人: {self.report['operator']}
数据提供: {self.report['data_provider']}

成长数据:
  文件: {self.report['growth_data'].get('file_name', '未提供')}
  总记录数: {growth_total}
  有效记录: {growth_valid}
  无效记录: {growth_total - growth_valid}

亲子数据:
  文件: {self.report['parent_child_data'].get('file_name', '未提供')}
  总记录数: {parent_total}
  有效记录: {parent_valid}
  无效记录: {parent_total - parent_valid}

汇总:
  总记录数: {total_records}
  有效记录: {total_valid}
  导入成功率: {success_rate:.2f}%

下一步:
  1. 将处理后的数据文件导入SCRM系统
  2. 验证导入结果
  3. 发送邮件通知
"""
        
        txt_filename = f"SCRM数据导入报告_{self.timestamp}.txt"
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write(txt_report)
        
        print(f"导入报告已生成:")
        print(f"  JSON报告: {report_filename}")
        print(f"  文本报告: {txt_filename}")
        
        return report_filename, txt_report
    
    def generate_email_content(self):
        """生成邮件内容"""
        print("生成邮件通知内容...")
        
        growth_data = self.report["growth_data"]
        parent_data = self.report["parent_child_data"]
        summary = self.report["summary"]
        
        email_content = f"""【SCRM数据导入完成】成长与亲子退费数据导入报告 - {datetime.now().strftime('%Y年%m月%d日')}

尊敬的各位同事：

已完成成长与亲子退费数据导入到SCRM系统的准备工作，具体如下：

一、数据导入概况
- 导入时间：{self.report['import_time']}
- 操作人：{self.report['operator']}
- 数据提供：{self.report['data_provider']}

二、数据验证结果统计
1. 成长数据退费表
   - 总记录数：{growth_data.get('total_records', 0)}
   - 有效记录：{growth_data.get('valid_records', 0)}
   - 无效记录：{growth_data.get('invalid_records', 0)}
   - 成功率：{(growth_data.get('valid_records', 0)/growth_data.get('total_records', 1)*100 if growth_data.get('total_records', 0) > 0 else 0):.1f}%

2. 亲子数据退费表
   - 总记录数：{parent_data.get('total_records', 0)}
   - 有效记录：{parent_data.get('valid_records', 0)}
   - 无效记录：{parent_data.get('invalid_records', 0)}
   - 成功率：{(parent_data.get('valid_records', 0)/parent_data.get('total_records', 1)*100 if parent_data.get('total_records', 0) > 0 else 0):.1f}%

三、汇总信息
- 总记录数：{summary.get('total_records', 0)}
- 总有效记录：{summary.get('total_valid_records', 0)}
- 整体成功率：{summary.get('success_rate', 0)}%

四、下一步工作
1. 请将处理后的数据文件导入SCRM系统
2. 导入后请在系统中核对数据
3. 如有问题请及时反馈

五、附件说明
1. 数据验证报告
2. 处理后的数据文件（如已生成）
3. 导入模板（如需要）

感谢各位同事的配合！

发件人：{self.report['operator']}
日期：{datetime.now().strftime('%Y年%m月%d日')}
"""
        
        email_filename = f"SCRM数据导入邮件内容_{self.timestamp}.txt"
        with open(email_filename, 'w', encoding='utf-8') as f:
            f.write(email_content)
        
        print(f"邮件内容已生成: {email_filename}")
        return email_content, email_filename

def main():
    """主函数"""
    print("=" * 60)
    print("SCRM数据导入工具")
    print("=" * 60)
    
    importer = SCRMDataImporter()
    
    # 检查是否有数据文件
    data_files = []
    for file in os.listdir('.'):
        if file.endswith(('.csv', '.xlsx', '.xls')) and ('成长' in file or '亲子' in file or '退费' in file):
            data_files.append(file)
    
    if not data_files:
        print("未找到数据文件，正在生成导入模板...")
        
        # 生成模板
        growth_template = importer.generate_import_template("growth")
        parent_template = importer.generate_import_template("parent_child")
        
        print("\n请按照以下步骤操作:")
        print("1. 将模板发送给泽彬填写数据")
        print("2. 收到数据文件后运行本工具进行验证")
        print("3. 处理数据并导入SCRM系统")
        print("4. 发送邮件通知")
        
        return
    
    # 处理找到的数据文件
    growth_df = None
    parent_df = None
    
    for file in data_files:
        if '成长' in file or 'growth' in file.lower():
            print(f"\n处理成长数据文件: {file}")
            growth_df, growth_missing = importer.validate_growth_data(file)
            
            if growth_df is not None and len(growth_missing) == 0:
                processed_file = importer.process_data_for_import(growth_df, "growth")
                print(f"成长数据处理完成: {processed_file}")
        
        elif '亲子' in file or 'parent' in file.lower():
            print(f"\n处理亲子数据文件: {file}")
            parent_df, parent_missing = importer.validate_parent_child_data(file)
            
            if parent_df is not None and len(parent_missing) == 0:
                processed_file = importer.process_data_for_import(parent_df, "parent_child")
                print(f"亲子数据处理完成: {processed_file}")
    
    # 生成报告
    report_file, report_text = importer.generate_import_report()
    
    # 生成邮件内容
    email_content, email_file = importer.generate_email_content()
    
    print("\n" + "=" * 60)
    print("数据导入准备工作完成!")
    print("=" * 60)
    print("\n下一步操作:")
    print("1. 将处理后的数据文件导入SCRM系统")
    print("2. 使用生成的邮件内容发送通知")
    print("3. 保存导入报告以备查阅")
    print(f"\n报告文件: {report_file}")
    print(f"邮件内容文件: {email_file}")

if __name__ == "__main__":
    main()