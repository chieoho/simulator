from flask import Flask

app = Flask(__name__)

# 加载地图
@app.route('/loadMap', methods=['POST'])
def load_map():
    return True

# 初始化库存
@app.route('/initStock', methods=['POST'])
def init_stock():
    return True

# 配置策略
@app.route('/configStrategy', methods=['POST'])
def config_strategy():
    return True


# 创建任务
@app.route('/createTmsTask', methods=['POST'])
def create_tms_task():
    return True

