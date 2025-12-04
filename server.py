#!/usr/bin/env python3
"""
简单的HTTP服务器，用于部署Python代码示例集网站
提供更好的错误处理和日志记录
"""

import http.server
import socketserver
import os
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('PythonCodeServer')

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    """自定义HTTP请求处理器"""
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        logger.info("%s - - [%s] %s" % (
            self.client_address[0],
            self.log_date_time_string(),
            format % args))
    
    def do_GET(self):
        """处理GET请求"""
        try:
            logger.info(f"收到请求: {self.path} 来自 {self.client_address[0]}")
            
            # 如果请求根路径，重定向到index.html
            if self.path == '/':
                self.path = '/index.html'
            
            # 调用父类的do_GET方法处理请求
            super().do_GET()
            
        except Exception as e:
            logger.error(f"处理请求时发生错误: {e}")
            self.send_error(500, f"服务器内部错误: {str(e)}")

def run_server(port=8000, host='0.0.0.0'):
    """启动HTTP服务器"""
    try:
        # 创建TCP服务器
        with socketserver.TCPServer((host, port), CustomHandler) as httpd:
            logger.info(f"Python代码示例集网站服务器启动成功")
            logger.info(f"访问地址: http://{host}:{port}")
            logger.info(f"按 Ctrl+C 停止服务器")
            
            # 启动服务器，持续运行直到收到中断信号
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        logger.info("收到中断信号，正在关闭服务器...")
        httpd.server_close()
        logger.info("服务器已关闭")
        
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
        raise

if __name__ == "__main__":
    # 确保在正确的目录下运行
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    logger.info(f"当前工作目录: {os.getcwd()}")
    
    # 启动服务器
    run_server(port=8000, host='0.0.0.0')