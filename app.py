from flask import Flask, render_template, request, jsonify
import base64
import io
import traceback
from PIL import Image, ImageDraw
from main import WorkplaceAnxietySimulator

app = Flask(__name__)
simulator = WorkplaceAnxietySimulator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        pua_text = request.form.get('pua_text', '')
        if not pua_text:
            return jsonify({"error": "请输入PUA话语"}), 400
        
        # 处理输入
        result = simulator.process_input(pua_text)
        
        # 将图像转换为base64字符串
        def img_to_base64(img):
            try:
                if img is None:
                    # 返回一个空白图像
                    blank_img = io.BytesIO()
                    Image.new('RGB', (400, 300), color='white').save(blank_img, format='PNG')
                    blank_img.seek(0)
                    return base64.b64encode(blank_img.read()).decode('utf-8')
                
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                return base64.b64encode(img_bytes.read()).decode('utf-8')
            except Exception as e:
                print(f"图像转换为base64失败: {str(e)}")
                # 返回一个错误提示图像
                error_img = io.BytesIO()
                error_image = Image.new('RGB', (400, 300), color='red')
                draw = ImageDraw.Draw(error_image)
                draw.text((100, 150), "图像生成失败", fill="white")
                error_image.save(error_img, format='PNG')
                error_img.seek(0)
                return base64.b64encode(error_img.read()).decode('utf-8')
        
        # 返回结果
        return jsonify({
            "emotion_data": result["analysis"],
            "heatmap": img_to_base64(result["heatmap"]),
            "emotion_curve": img_to_base64(result["emotion_curve"]),
            "dialogue_comparison": img_to_base64(result["dialogue_comparison"]),
            "progress_bar": img_to_base64(result["progress_bar"])
        })
    except Exception as e:
        print(f"分析请求处理失败: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": f"处理请求时发生错误: {str(e)}"}), 500

@app.route('/about')
def about():
    return render_template('about.html')  # 返回一个 HTML 模板

if __name__ == '__main__':
    app.run(debug=True)