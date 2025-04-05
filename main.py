import os
import json
import requests
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import traceback  # 添加这一行

# 导入心理阴影面积计算器
from shadow_area_calculator import ShadowAreaCalculator

# API配置
api_key = "sk-bWWNDfwuOrM0Rw1fhzjN1GUrgBn2o4y2ajEfK8I9wG4PNw5K"
base_url = "https://api.chatanywhere.tech/v1"

# api_key = "sk-yhyHIS4iiJzWq46g669fAf3b885440E0Ab3174317e585bC6"
# base_url = "https://api.1lm.me/v1"

class WorkplaceAnxietySimulator:
    def __init__(self):
        self.emotion_data = None
        # 初始化心理阴影面积计算器
        self.shadow_calculator = ShadowAreaCalculator()
    
    def analyze_text(self, pua_text):
        """分析用户输入的PUA文本，提取情绪数据"""
        prompt = """
        用户输入对话："{}"
        请直接精细化完成该核心任务——分析对话是否包含职场PUA语言并提取情绪响应字段对json字符串中的空字段进行赋值。
        执行任务步骤：
        方法论：
        采用【语言攻击识别 + 情绪认知评估 + 身体感应映射 + 情绪时间线建模 + 健康表达替换 + 情绪释放反馈】六维分析框架，结合心理学非暴力沟通（NVC）、情绪聚焦疗法（EFT）与身体感知疗法（Somatic Experiencing）进行系统评估。
        方法论执行步骤：
        健康表达对照（healthy_reframe）：逐字修改用户输入的对话原句，
        例如对话原句："你别给脸不要脸!别逼我在世界上最快乐的地方扇你！" healthy_reframe："亲爱的,我给你准备了一个台阶下，因为我不想在这世上最美好的地方做出不礼貌的事~"

        识别语言攻击词汇（attack_keywords）：提取对话中包含的压迫、贬低、操控等词句。

        标记情绪类型（emotion_tag）：分析语言所激发的核心情绪，如羞耻、内疚、恐惧、无力等。

        标记身体感应区域（body_map）：结合情绪类型对应生理反应部位，如羞耻感集中在头部，恐惧感集中在胃部。
        ("head": "头痛、面部潮红、发热、头晕", "chest": "胸口沉重、呼吸急促、心跳加速","stomach": "恶心、空虚、胃部紧张","neck": "脖部僵硬、肩膀紧绷、压迫感","back": "背部紧张、脊柱不适、感到压迫","hands": "手心出汗、手指紧握、手指颤抖","legs": "腿部麻木、沉重、无法站立","face": "面部潮红、面部紧绷、表情僵硬","heart": "心跳加速、心悸、胸部压迫感","abdomen": "腹部紧绷、空虚、胃翻腾")

        评估情绪强度等级（1-10）affect_level：综合语言攻击程度与情绪反应判断其强度。

        构建情绪时间曲线（timeline）：模拟对话进行中的情绪波动轨迹，最多5个时间节点，每个节点包括：时间点、情绪值、内在声音（标签）。

        输出情绪释放反馈（emotion_release）：
        recommended_reply=向上管理的反击话术（向上管理公式：暴露弱点与“无关痛痒的求助”+强化对方价值与捧杀+情感转移与请求帮助的智慧引导+轻描淡写的态度与灵活回旋空间）,
        level_up_msg=高能成长提示,
        unlocked_skill=新技能标签,
        release_percent=反击后情绪释放度。
        
        请补全以下JSON字符串的字段值,完成赋值任务：
        {{
        "attack_keywords": [],
        "emotion_tag": "",
        "affect_level": 0,
        "body_map": {{
            "head": "",
            "chest": "",
            "stomach": "",
            "neck": "",
            "back": "",
            "hands": "",
            "legs": "",
            "face": "",
            "heart": "",
            "abdomen": ""
        }},
        "timeline": [
            {{"time_index": 0, "emotion_value": 0, "inner_voice": ""}},
            {{"time_index": 1, "emotion_value": 0, "label": ""}},
            {{"time_index": 2, "emotion_value": 0, "inner_voice": ""}},
            {{"time_index": 3, "emotion_value": 0, "label": ""}},
            {{"time_index": 4, "emotion_value": 0, "inner_voice": ""}}
        ],
        "healthy_reframe": "",
        "emotion_release": {{
            "recommended_reply": "",
            "level_up_msg": "",
            "unlocked_skill": "",
            "release_percent": 0
        }}
        }}
        """.format(pua_text)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "你是一个专业的职场心理分析师，擅长识别PUA话语并分析其情绪影响。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        try:
            print(f"正在发送API请求到 {base_url}...")
            print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
            response = requests.post(f"{base_url}/chat/completions", headers=headers, json=data, timeout=30)
            
            # 打印响应状态和内容，帮助调试
            print(f"API响应状态码: {response.status_code}")
            
            # 如果响应不成功，尝试打印错误信息
            if response.status_code != 200:
                print(f"API错误响应: {response.text}")
                raise Exception(f"API请求失败，状态码: {response.status_code}")
            
            result = response.json()
            print("API响应成功，正在解析结果...")
            print(f"完整API响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            # 检查响应结构
            if "choices" not in result or len(result["choices"]) == 0:
                print(f"API响应格式异常: {result}")
                raise Exception("API响应格式异常，缺少choices字段")
            
            content = result["choices"][0]["message"]["content"]
            print(f"API返回内容前100字符: {content[:100]}...")
            print(f"完整返回内容:\n{content}")
            
            # 尝试解析JSON
            try:
                analysis = json.loads(content)
                self.emotion_data = analysis
                print("成功解析JSON结果")
                print(f"解析后的JSON数据: {json.dumps(analysis, ensure_ascii=False, indent=2)}")
                return analysis
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {str(e)}")
                print(f"原始内容: {content}")
                
                # 尝试提取JSON部分
                try:
                    # 查找可能的JSON开始和结束位置
                    json_start = content.find('{')
                    json_end = content.rfind('}') + 1
                    
                    if json_start >= 0 and json_end > json_start:
                        json_str = content[json_start:json_end]
                        print(f"提取的JSON字符串前100字符: {json_str[:100]}...")
                        print(f"完整提取的JSON字符串:\n{json_str}")
                        
                        # 尝试修复常见的JSON格式问题
                        # 1. 替换单引号为双引号
                        json_str = json_str.replace("'", '"')
                        # 2. 确保布尔值和null是小写的
                        json_str = json_str.replace("True", "true").replace("False", "false").replace("None", "null")
                        print(f"修复后的JSON字符串:\n{json_str}")
                        
                        # 再次尝试解析
                        analysis = json.loads(json_str)
                        self.emotion_data = analysis
                        print("成功从响应中提取并解析JSON")
                        return analysis
                    else:
                        print("无法在响应中找到有效的JSON")
                except Exception as e2:
                    print(f"提取JSON失败: {str(e2)}")
                
                # 如果仍然失败，尝试使用正则表达式提取
                try:
                    import re
                    # 尝试匹配最外层的花括号及其内容
                    pattern = r'\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\}'
                    matches = re.findall(pattern, content)
                    if matches:
                        json_str = matches[0]
                        print(f"通过正则表达式提取的JSON前100字符: {json_str[:100]}...")
                        print(f"完整正则提取的JSON:\n{json_str}")
                        
                        # 尝试修复常见的JSON格式问题
                        json_str = json_str.replace("'", '"').replace("True", "true").replace("False", "false").replace("None", "null")
                        print(f"正则提取后修复的JSON:\n{json_str}")
                        
                        # 再次尝试解析
                        analysis = json.loads(json_str)
                        self.emotion_data = analysis
                        print("成功通过正则表达式提取并解析JSON")
                        return analysis
                except Exception as e3:
                    print(f"正则表达式提取JSON失败: {str(e3)}")
                
                # 如果所有尝试都失败，返回一个默认结构
                print("所有解析尝试都失败，使用默认分析结果")
                default_result = {
                    "attack_keywords": ["解析失败"],
                    "emotion_tag": "未知",
                    "affect_level": 5,
                    "body_map": {
                        "head": "未知",
                        "chest": "未知",
                        "stomach": "未知",
                        "neck": "未知",
                        "back": "未知",
                        "hands": "未知",
                        "legs": "未知",
                        "face": "未知",
                        "heart": "未知",
                        "abdomen": "未知"
                    },
                    "timeline": [
                        {"time_index": 0, "emotion_value": 3, "inner_voice": "未知"},
                        {"time_index": 1, "emotion_value": 5, "label": "未知"},
                        {"time_index": 2, "emotion_value": 7, "inner_voice": "未知"},
                        {"time_index": 3, "emotion_value": 6, "label": "未知"},
                        {"time_index": 4, "emotion_value": 4, "inner_voice": "未知"}
                    ],
                    "healthy_reframe": "API返回结果解析失败，无法生成替代表述",
                    "emotion_release": {
                        "release_percent": 50,
                        "unlocked_skill": "错误处理",
                        "level_up_msg": "遇到技术问题时保持冷静"
                    }
                }
                self.emotion_data = default_result
                return default_result
                
        except Exception as e:
            print(f"API请求失败: {str(e)}")
            # 返回默认结构
            default_result = {
                 "attack_keywords": ["API请求失败"],
                "emotion_tag": "未知",
                "affect_level": 5,
                "body_map": {
                    "head": "未知",
                    "chest": "未知",
                    "stomach": "未知",
                    "neck": "未知",
                    "back": "未知",
                    "hands": "未知",
                    "legs": "未知",
                    "face": "未知",
                    "heart": "未知",
                    "abdomen": "未知"
                },
                "timeline": [
                    {"time_index": 0, "emotion_value": 3, "inner_voice": "未知"},
                    {"time_index": 1, "emotion_value": 5, "label": "未知"},
                    {"time_index": 2, "emotion_value": 7, "inner_voice": "未知"},
                    {"time_index": 3, "emotion_value": 6, "label": "未知"},
                    {"time_index": 4, "emotion_value": 4, "inner_voice": "未知"}
                ],
                "healthy_reframe": "无法生成替代表述",
                "emotion_release": {
                    "release_percent": 50,
                    "unlocked_skill": "无法获取",
                    "level_up_msg": "无法获取"
                } , # 修复了右花括号
            }
            self.emotion_data = default_result
            return default_result
    
    def _get_font(self, size=14, is_title=False):
        """获取支持中文的字体，按优先级尝试多种字体"""
        font_paths = [
            "C:/Windows/Fonts/simhei.ttf",     # 黑体
            "C:/Windows/Fonts/simsun.ttc",     # 宋体
            "C:/Windows/Fonts/msyh.ttc",       # 微软雅黑
            "C:/Windows/Fonts/simkai.ttf",     # 楷体
            "./fonts/simhei.ttf",              # 项目目录下的黑体
            "./fonts/simsun.ttc",              # 项目目录下的宋体
        ]
        
        # 如果是标题，使用更大的字号
        if is_title:
            size = int(size * 1.5)
        
        # 尝试加载字体
        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, size)
            except Exception:
                continue
        
        # 如果所有字体都加载失败，使用默认字体
        print("警告：无法加载中文字体，可能导致中文显示为乱码")
        return ImageFont.load_default()
    
    def _translate_body_part(self, part):
        """将身体部位英文名称翻译为中文"""
        translations = {
            "head": "头部",
            "face": "面部",
            "neck": "颈部",
            "chest": "胸部",
            "heart": "心脏",
            "stomach": "胃部",
            "abdomen": "腹部",
            "back": "背部",
            "hands": "手部",
            "legs": "腿部"
        }
        return translations.get(part, part)
    
    def _get_chinese_font(self, size=12):
        """获取支持中文的matplotlib字体"""
        try:
            # 尝试使用matplotlib内置的中文字体
            from matplotlib.font_manager import FontProperties
            
            font_paths = [
                "C:/Windows/Fonts/simhei.ttf",     # 黑体
                "C:/Windows/Fonts/simsun.ttc",     # 宋体
                "C:/Windows/Fonts/msyh.ttc",       # 微软雅黑
                "./fonts/simhei.ttf",              # 项目目录下的黑体
            ]
            
            # 尝试加载字体
            for font_path in font_paths:
                if os.path.exists(font_path):
                    return FontProperties(fname=font_path, size=size)
                    
            # 如果找不到指定字体，使用系统默认字体
            return FontProperties(size=size)
        except Exception as e:
            print(f"获取中文字体失败: {str(e)}")
            return None
    
    def generate_heatmap(self):
        """生成焦虑热力图"""
        try:
            if not self.emotion_data:
                print("没有情绪数据，无法生成热力图")
                return None
                
            # 创建图表
            plt.figure(figsize=(8, 10))
            
            # 加载人体轮廓图像
            body_outline = np.ones((500, 300, 3))  # 创建一个白色背景
            
            # 绘制简单的人体轮廓
            # 头部
            plt.gca().add_patch(plt.Circle((150, 75), 50, fill=False, color='black'))
            # 躯干
            plt.plot([150, 150], [125, 350], 'k-', linewidth=2)
            # 手臂
            plt.plot([150, 75], [200, 250], 'k-', linewidth=2)
            plt.plot([150, 225], [200, 250], 'k-', linewidth=2)
            # 腿部
            plt.plot([150, 100], [350, 450], 'k-', linewidth=2)
            plt.plot([150, 200], [350, 450], 'k-', linewidth=2)
            
            # 获取身体映射数据
            body_map = self.emotion_data.get("body_map", {})
            
            # 定义hotspots位置和强度
            hotspots = []
            
            # 定义身体部位的位置映射
            body_positions = {
                "head": (150, 75),     # 头部
                "face": (150, 60),     # 面部
                "neck": (150, 125),    # 颈部
                "chest": (150, 175),   # 胸部
                "heart": (130, 175),   # 心脏
                "stomach": (150, 250), # 胃部
                "abdomen": (150, 275), # 腹部
                "back": (150, 200),    # 背部
                "hands": (75, 250),    # 手部
                "legs": (150, 400)     # 腿部
            }
            
            # 添加所有身体部位的热点
            for part, position in body_positions.items():
                if part in body_map and body_map[part]:
                    x, y = position
                    intensity = 40  # 热点大小
                    hotspots.append((x, y, intensity))
            
            # 绘制热力图
            for x, y, intensity in hotspots:
                plt.gca().add_patch(plt.Circle((x, y), intensity, alpha=0.5, color='red'))
            
            # 添加标签
            plt.text(150, 20, "焦虑热力图", fontproperties=self._get_chinese_font(size=16), 
                    ha='center', va='center')
            
            # 添加身体部位标签
            y_offset = 50
            for part in body_positions.keys():
                if part in body_map and body_map[part]:
                    # 截断过长的描述文本
                    description = body_map[part]
                    if len(description) > 20:
                        description = description[:20] + "..."
                    
                    plt.text(230, y_offset, f"{self._translate_body_part(part)}: {description}", 
                            fontproperties=self._get_chinese_font(), 
                            ha='left', va='center')
                    y_offset += 30
            
            # 设置坐标轴
            plt.axis('off')
            plt.xlim(0, 400)
            plt.ylim(500, 0)
            
            # 保存图像到内存
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
            buf.seek(0)
            plt.close()
            
            # 从内存加载图像
            img = Image.open(buf)
            return img
        except Exception as e:
            print(f"生成热力图失败: {str(e)}")
            traceback.print_exc()
            return None
    
    def generate_emotion_curve(self):
        """生成情绪波动曲线图"""
        if not self.emotion_data:
            return None
            
        # 创建图表
        plt.figure(figsize=(8, 5))
        
        # 获取时间线数据
        timeline = self.emotion_data.get("timeline", [])
        time_points = [point.get("time_index", 0) for point in timeline]
        emotion_values = [point.get("emotion_value", 0) for point in timeline]
        
        # 绘制曲线
        plt.plot(time_points, emotion_values, marker='o', linestyle='-', color='blue', linewidth=2)
        
        # 添加标签和标题
        plt.title("情绪波动曲线", fontproperties=self._get_chinese_font())
        plt.xlabel("时间点", fontproperties=self._get_chinese_font())
        plt.ylabel("情绪强度", fontproperties=self._get_chinese_font())
        
        # 设置坐标轴范围
        plt.ylim(0, 10)
        plt.xlim(min(time_points) - 0.5, max(time_points) + 0.5)
        
        # 添加网格
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # 添加情绪标签
        for i, point in enumerate(timeline):
            label = point.get("label", "")
            inner_voice = point.get("inner_voice", "")
            text = label or inner_voice
            if text:
                plt.annotate(text, 
                             xy=(time_points[i], emotion_values[i]),
                             xytext=(0, 10),
                             textcoords="offset points",
                             ha='center',
                             fontproperties=self._get_chinese_font(size=8),
                             bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3))
        
        # 保存图像到内存
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        
        # 从内存加载图像
        img = Image.open(buf)
        return img
    
   
    
    def generate_dialogue_comparison(self, original_text):
        """生成对话双轨对比图"""
        if not self.emotion_data:
            return None
            
        img = Image.new('RGB', (800, 400), color='white')
        draw = ImageDraw.Draw(img)
        
        # 获取字体
        font_title = self._get_font(16, is_title=True)
        font = self._get_font(14)
        
        # 添加标题
        draw.text((320, 20), "对话对比", fill="black", font=font_title)
        
        # 分隔线
        draw.line((400, 50, 400, 350), fill='gray', width=2)
        
        # 添加PUA话术
        draw.text((50, 60), "PUA话术:", fill="red", font=font_title)
        
        # 文本换行处理 - 使用更大的行间距
        line_spacing = 25  # 增加行间距
        max_width = 330    # 减小最大宽度，避免文字靠近分隔线
        
        # 左侧PUA话术
        lines = self._wrap_text(original_text, font, max_width)
        y_position = 90
        for line in lines:
            draw.text((50, y_position), line, fill="black", font=font)
            y_position += line_spacing  # 使用更大的行间距
        
        # 添加健康替代表述
        draw.text((450, 60), "健康表达:", fill="green", font=font_title)
        
        # 右侧健康表达
        healthy_reframe = self.emotion_data.get("healthy_reframe", "无法生成替代表述")
        lines = self._wrap_text(healthy_reframe, font, max_width)
        
        y_position = 90
        for line in lines:
            draw.text((450, y_position), line, fill="black", font=font)
            y_position += line_spacing  # 使用更大的行间距
        
        return img
    
    def _wrap_text(self, text, font, max_width):
        """辅助方法：将文本按指定宽度换行，优化中文处理"""
        lines = []
        # 先按自然段落分割
        paragraphs = text.split('\n')
        
        for paragraph in paragraphs:
            # 如果段落为空，添加一个空行
            if not paragraph:
                lines.append("")
                continue
                
            # 对于中文文本，按字符分割更合适
            current_line = ""
            
            # 逐字处理
            for char in paragraph:
                test_line = current_line + char
                # 测量文本宽度
                try:
                    # 尝试使用getbbox (PIL 9.0+)
                    bbox = font.getbbox(test_line)
                    width = bbox[2]
                except AttributeError:
                    try:
                        # 尝试使用getsize (旧版PIL)
                        width, height = font.getsize(test_line)
                    except AttributeError:
                        # 如果两种方法都不可用，使用一个估计值
                        width = len(test_line) * 14  # 估计每个中文字符14像素宽
                
                if width <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = char
            
            # 添加最后一行
            if current_line:
                lines.append(current_line)
        
        return lines
    
    def generate_progress_bar(self):
        """生成焦虑解压进度条"""
        if not self.emotion_data:
            print("没有情绪数据，无法生成进度条")
            return None
            
        # 导入textwrap模块用于文本换行
        import textwrap
            
        emotion_release = self.emotion_data.get("emotion_release", {})
        recommended_reply = emotion_release.get("recommended_reply", "无法生成推荐回复")
        release_percent = emotion_release.get("release_percent", 50)
        unlocked_skill = emotion_release.get("unlocked_skill", "无反击技能")
        level_up_msg = emotion_release.get("level_up_msg", "继续努力")
        
        # 创建画布
        img = Image.new('RGB', (600, 400), color='white')  # 增加高度以容纳更多文本
        draw = ImageDraw.Draw(img)
        
        # 获取字体
        font_title = self._get_font(16, is_title=True)
        font = self._get_font(14)
        
        # 添加标题
        draw.text((200, 20), "焦虑解压进度", fill="black", font=font_title)
        
        # 绘制进度条背景
        draw.rectangle((50, 80, 550, 120), outline='black', width=2)
        
        # 绘制进度
        progress_width = int(500 * release_percent / 100)
        draw.rectangle((50, 80, 50 + progress_width, 120), fill='green', outline=None)
        
        # 添加百分比文本
        draw.text((275, 95), f"{release_percent}%", fill="black", font=font_title)
        
        # 添加解锁技能
        draw.text((50, 140), "解锁技能:", fill="blue", font=font_title)
        draw.text((70, 165), f"• {unlocked_skill}", fill="black", font=font)
        
        # 添加回复建议
        draw.text((50, 200), "回复建议:", fill="green", font=font_title)
        
        # 处理回复建议文本换行
        try:
            # 使用self.emotion_data而不是emotion_data
            wrapped_reply = textwrap.fill(recommended_reply, width=40)
            y_position = 225
            for line in wrapped_reply.split('\n'):
                draw.text((70, y_position), f"• {line}", fill="black", font=font)
                y_position += 25
        except Exception as e:
            print(f"处理回复建议文本失败: {str(e)}")
            draw.text((70, 225), "• 无法显示回复建议", fill="black", font=font)
            y_position = 250
        
        # 添加升级信息
        draw.text((50, y_position + 10), "成长提示:", fill="purple", font=font_title)
        
        # 处理成长提示文本换行
        try:
            wrapped_msg = textwrap.fill(level_up_msg, width=40)
            y_position += 35
            for line in wrapped_msg.split('\n'):
                draw.text((70, y_position), f"• {line}", fill="black", font=font)
                y_position += 25
        except Exception as e:
            print(f"处理成长提示文本失败: {str(e)}")
            draw.text((70, y_position + 35), "• 无法显示成长提示", fill="black", font=font)
        
        return img
    
    def process_input(self, pua_text):
        """处理用户输入，生成分析结果和可视化图像"""
        try:
            print(f"\n===== 开始处理用户输入 =====")
            print(f"输入文本: {pua_text}")
            
            # 分析文本
            print(f"\n----- 开始文本分析 -----")
            analysis = self.analyze_text(pua_text)
            print(f"----- 文本分析完成 -----")
            print(f"分析结果: {json.dumps(analysis, ensure_ascii=False, indent=2)}")
            
            # 生成图像
            print(f"\n----- 开始生成可视化图像 -----")
            try:
                heatmap = self.generate_heatmap()
            except Exception as e:
                print(f"生成热力图失败: {str(e)}")
                traceback.print_exc()
                heatmap = None
                
            try:
                emotion_curve = self.generate_emotion_curve()
            except Exception as e:
                print(f"生成情绪曲线失败: {str(e)}")
                traceback.print_exc()
                emotion_curve = None
                
            try:
                dialogue_comparison = self.generate_dialogue_comparison(pua_text)
            except Exception as e:
                print(f"生成对话对比图失败: {str(e)}")
                traceback.print_exc()
                dialogue_comparison = None
                
            try:
                progress_bar = self.generate_progress_bar()
            except Exception as e:
                print(f"生成进度条失败: {str(e)}")
                traceback.print_exc()
                progress_bar = None
            
            try:
                shadow_area_viz = self.generate_shadow_area_visualization()
            except Exception as e:
                print(f"生成心理阴影面积可视化失败: {str(e)}")
                traceback.print_exc()
                shadow_area_viz = None
            
            return {
                "analysis": analysis,
                "heatmap": heatmap,
                "emotion_curve": emotion_curve,
                "dialogue_comparison": dialogue_comparison,
                "progress_bar": progress_bar,
                "shadow_area_viz": shadow_area_viz
            }
        except Exception as e:
            print(f"处理输入失败: {str(e)}")
            traceback.print_exc()
            # 返回一个最小的结果集
            return {
                "analysis": {"error": f"处理失败: {str(e)}"},
                "heatmap": None,
                "emotion_curve": None,
                "dialogue_comparison": None,
                "progress_bar": None,
                "shadow_area_viz": None
            }

# 测试代码
if __name__ == "__main__":
    simulator = WorkplaceAnxietySimulator()
    
    # 测试用的PUA话语
    test_pua = "你怎么连这么简单的事情都做不好？别人都能很快完成，就你这么慢，是不是不适合这个岗位？"
    
    # 处理输入
    result = simulator.process_input(test_pua)
    
    # 打印结果
    print("情绪分析结果:", json.dumps(result["analysis"], ensure_ascii=False, indent=2))
    
    # 保存图像
    result["heatmap"].save("heatmap.png")
    result["emotion_curve"].save("emotion_curve.png")
    result["dialogue_comparison"].save("dialogue_comparison.png")
    result["progress_bar"].save("progress_bar.png")
    if result["shadow_area_viz"]:
        result["shadow_area_viz"].save("shadow_area.png")
        print("心理阴影面积图像已保存")
    
    print("图像已保存到当前目录")
     
