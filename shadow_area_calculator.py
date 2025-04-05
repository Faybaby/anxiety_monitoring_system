import os
from PIL import Image, ImageDraw, ImageFont

class ShadowAreaCalculator:
    """心理阴影面积计算器组件"""
    
    def __init__(self, emotion_data=None):
        """初始化计算器
        
        Args:
            emotion_data: 情绪分析数据
        """
        self.emotion_data = emotion_data
    
    def set_emotion_data(self, emotion_data):
        """设置情绪数据
        
        Args:
            emotion_data: 情绪分析数据
        """
        self.emotion_data = emotion_data
    
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
    
    def calculate_shadow_area(self):
        """计算心理阴影面积"""
        if not self.emotion_data:
            print("没有情绪数据，无法计算心理阴影面积")
            return None
            
        # 1. 获取情绪强度
        affect_level = self.emotion_data.get("affect_level", 5)
        
        # 2. 计算语言攻击权重
        attack_keywords = self.emotion_data.get("attack_keywords", [])
        # 根据关键词判断攻击强度
        light_attacks = 0
        medium_attacks = 0
        heavy_attacks = 0
        
        # 简单判断攻击强度的关键词
        light_keywords = ["不够好", "慢", "效率低", "不专业"]
        medium_keywords = ["差劲", "无能", "不适合", "失望"]
        heavy_keywords = ["废物", "白痴", "滚", "炒鱿鱼"]
        
        for keyword in attack_keywords:
            if any(light_word in keyword.lower() for light_word in light_keywords):
                light_attacks += 1
            elif any(medium_word in keyword.lower() for medium_word in medium_keywords):
                medium_attacks += 1
            elif any(heavy_word in keyword.lower() for heavy_word in heavy_keywords):
                heavy_attacks += 1
            else:
                # 默认为轻度攻击
                light_attacks += 1
                
        attack_weight = (light_attacks * 1) + (medium_attacks * 2) + (heavy_attacks * 3)
        
        # 3. 计算身体感应反应权重
        body_map = self.emotion_data.get("body_map", {})
        body_weights = {
            "head": 1,
            "chest": 3,
            "stomach": 4,
            "neck": 2,
            "back": 2,
            "hands": 1,
            "legs": 1,
            "face": 1,
            "heart": 5,
            "abdomen": 3
        }
        
        body_weight = 0
        for part, description in body_map.items():
            if description and part in body_weights:
                body_weight += body_weights[part]
        
        # 4. 计算情绪波动因子
        timeline = self.emotion_data.get("timeline", [])
        emotion_values = [point.get("emotion_value", 0) for point in timeline if point.get("emotion_value", 0) > 0]
        
        if emotion_values:
            # 计算最大波动幅度
            max_change = max(emotion_values) - min(emotion_values) if len(emotion_values) > 1 else 0
            
            # 根据波动幅度确定情绪波动因子
            if max_change <= 1:
                emotion_wave_factor = 1
            elif max_change <= 2:
                emotion_wave_factor = 2
            elif max_change <= 4:
                emotion_wave_factor = 3
            elif max_change <= 6:
                emotion_wave_factor = 4
            else:
                emotion_wave_factor = 5
        else:
            emotion_wave_factor = 1
        
        # 5. 计算心理阴影面积
        shadow_area = (affect_level * attack_weight + body_weight) * emotion_wave_factor
        
        # 返回计算结果和中间值，用于展示
        return {
            "shadow_area": shadow_area,
            "affect_level": affect_level,
            "attack_weight": attack_weight,
            "body_weight": body_weight,
            "emotion_wave_factor": emotion_wave_factor,
            "light_attacks": light_attacks,
            "medium_attacks": medium_attacks,
            "heavy_attacks": heavy_attacks
        }
    
    def generate_visualization(self):
        """生成心理阴影面积可视化图像"""
        if not self.emotion_data:
            print("没有情绪数据，无法生成心理阴影面积可视化")
            return None
            
        # 计算心理阴影面积
        shadow_data = self.calculate_shadow_area()
        if not shadow_data:
            return None
            
        # 创建画布
        img = Image.new('RGB', (600, 500), color='white')
        draw = ImageDraw.Draw(img)
        
        # 获取字体
        font_title = self._get_font(16, is_title=True)
        font = self._get_font(14)
        font_small = self._get_font(12)
        
        # 添加标题
        draw.text((200, 20), "心理阴影面积计算", fill="black", font=font_title)
        
        # 绘制心理阴影面积值
        shadow_area = shadow_data["shadow_area"]
        draw.text((50, 70), f"心理阴影面积: {shadow_area:.2f}", fill="red", font=font_title)
        
        # 绘制计算公式
        formula = "(情绪强度 × 语言攻击权重 + 身体感应反应权重) × 情绪波动因子"
        draw.text((50, 110), f"计算公式: {formula}", fill="black", font=font)
        
        # 绘制各参数值
        y_pos = 150
        draw.text((50, y_pos), f"情绪强度 (affect_level): {shadow_data['affect_level']}", fill="black", font=font)
        y_pos += 30
        
        draw.text((50, y_pos), f"语言攻击权重 (attack_weight): {shadow_data['attack_weight']}", fill="black", font=font)
        y_pos += 25
        draw.text((70, y_pos), f"- 轻度攻击: {shadow_data['light_attacks']} × 1 = {shadow_data['light_attacks']}", fill="black", font=font_small)
        y_pos += 25
        draw.text((70, y_pos), f"- 中度攻击: {shadow_data['medium_attacks']} × 2 = {shadow_data['medium_attacks'] * 2}", fill="black", font=font_small)
        y_pos += 25
        draw.text((70, y_pos), f"- 重度攻击: {shadow_data['heavy_attacks']} × 3 = {shadow_data['heavy_attacks'] * 3}", fill="black", font=font_small)
        y_pos += 30
        
        draw.text((50, y_pos), f"身体感应反应权重 (body_weight): {shadow_data['body_weight']}", fill="black", font=font)
        y_pos += 30
        
        draw.text((50, y_pos), f"情绪波动因子 (emotion_wave_factor): {shadow_data['emotion_wave_factor']}", fill="black", font=font)
        y_pos += 40
        
        # 绘制计算过程
        calculation = f"({shadow_data['affect_level']} × {shadow_data['attack_weight']} + {shadow_data['body_weight']}) × {shadow_data['emotion_wave_factor']} = {shadow_area:.2f}"
        draw.text((50, y_pos), f"计算过程: {calculation}", fill="blue", font=font)
        y_pos += 40
        
        # 绘制心理阴影面积评估
        if shadow_area < 50:
            assessment = "轻微心理阴影: 情绪影响较小，可以通过简单的自我调节恢复。"
            color = "green"
        elif shadow_area < 100:
            assessment = "中度心理阴影: 情绪受到明显影响，建议采取积极的情绪管理策略。"
            color = "orange"
        elif shadow_area < 200:
            assessment = "重度心理阴影: 情绪受到严重影响，建议寻求专业心理支持。"
            color = "red"
        else:
            assessment = "极重度心理阴影: 情绪受到极大冲击，强烈建议立即寻求专业心理帮助。"
            color = "purple"
            
        draw.text((50, y_pos), "评估结果:", fill="black", font=font_title)
        y_pos += 30
        
        # 处理评估文本换行
        max_width = 500
        lines = self._wrap_text(assessment, font, max_width)
        for line in lines:
            draw.text((70, y_pos), line, fill=color, font=font)
            y_pos += 25
        
        return img

# 简单测试代码
if __name__ == "__main__":
    # 创建一个测试用的情绪数据
    test_emotion_data = {
        "affect_level": 7,
        "attack_keywords": ["不适合", "效率低", "太慢了", "废物"],
        "body_map": {
            "head": "头痛",
            "chest": "胸闷",
            "stomach": "胃部不适",
            "heart": "心跳加速"
        },
        "timeline": [
            {"time_index": 0, "emotion_value": 3, "inner_voice": "我做得不好吗？"},
            {"time_index": 1, "emotion_value": 5, "label": "焦虑"},
            {"time_index": 2, "emotion_value": 7, "inner_voice": "我是不是真的不行？"},
            {"time_index": 3, "emotion_value": 6, "label": "自我怀疑"},
            {"time_index": 4, "emotion_value": 4, "inner_voice": "我需要证明自己"}
        ]
    }
    
    # 创建计算器实例
    calculator = ShadowAreaCalculator(test_emotion_data)
    
    # 计算心理阴影面积
    shadow_data = calculator.calculate_shadow_area()
    print("心理阴影面积计算结果:", shadow_data)
    
    # 生成可视化图像
    visualization = calculator.generate_visualization()
    if visualization:
        visualization.save("shadow_area_test.png")
        print("心理阴影面积可视化图像已保存")