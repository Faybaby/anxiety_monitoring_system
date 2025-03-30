import os
import sys
import subprocess
import webbrowser
import time
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app_log.txt"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("焦虑传感器")

def check_dependencies():
    """检查并安装依赖"""
    required_packages = [
        'flask', 'requests', 'matplotlib', 'pillow', 'numpy'
    ]
    
    logger.info("正在检查依赖...")
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"✓ {package} 已安装")
        except ImportError:
            logger.warning(f"✗ {package} 未安装，正在安装...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            logger.info(f"✓ {package} 安装完成")

def check_api_connection():
    """检查API连接状态"""
    import requests
    from main import api_key, base_url
    
    logger.info("正在检查API连接...")
    try:
        response = requests.get(
            f"{base_url}/models",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        if response.status_code == 200:
            logger.info("✓ API连接正常")
            return True
        else:
            logger.error(f"✗ API连接失败: 状态码 {response.status_code}")
            logger.error(f"响应内容: {response.text}")
            return False
    except Exception as e:
        logger.error(f"✗ API连接异常: {str(e)}")
        return False

def run_app():
    """运行应用程序"""
    logger.info("\n正在启动职场焦虑体感模拟器...")
    
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 检查API连接
    api_status = check_api_connection()
    if not api_status:
        logger.warning("API连接测试失败，应用可能无法正常工作")
        print("\n警告: API连接测试失败，应用可能无法正常工作")
        print("请检查网络连接和API密钥是否有效")
        
        # 询问用户是否继续
        choice = input("是否仍要继续启动应用? (y/n): ")
        if choice.lower() != 'y':
            logger.info("用户选择退出应用")
            return
    
    # 启动Flask应用
    from app import app
    
    # 在新线程中打开浏览器
    def open_browser():
        time.sleep(1.5)  # 等待Flask启动
        webbrowser.open('http://127.0.0.1:5000')
        logger.info("已在浏览器中打开应用")
    
    import threading
    threading.Thread(target=open_browser).start()
    
    # 运行Flask应用
    app.run(debug=False)

if __name__ == "__main__":
    print("=" * 50)
    print("职场焦虑体感模拟器 - 启动程序")
    print("=" * 50)
    
    try:
        check_dependencies()
        run_app()
    except Exception as e:
        logger.error(f"应用运行出错: {str(e)}", exc_info=True)
        print(f"\n错误: {str(e)}")
        print("详细错误信息已记录到app_log.txt文件中")
        input("按Enter键退出...")