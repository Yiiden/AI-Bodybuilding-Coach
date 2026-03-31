import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from services.state_manager import state_manager
from services.ai_coach import generate_advice
from services.pose_library import POSE_DATA, get_pose_info # 確保引入 POSE_DATA

app = Flask(__name__)

# ==========================================
# 設定區 (請填入您的 API Key)
# ==========================================
GEMINI_API_KEY = ""  # <--- 請確認這裡有填入您的 Key
# ==========================================

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        pose = request.form.get('pose_selector')
        
        # 接收前端傳來的使用者個資
        h = request.form.get('height')
        w = request.form.get('weight')
        a = request.form.get('age')
        
        # 存入 State Manager
        state_manager.set_target_pose(pose)
        state_manager.set_user_profile(h, w, a)
        
        return redirect(url_for('dashboard'))
    
    # 傳遞 POSE_DATA 給前端 (這樣 index.html 才能切換圖片)
    return render_template('index.html', pose_data=POSE_DATA)

@app.route('/dashboard')
def dashboard():
    pose_name = state_manager.get_target_pose()
    info = get_pose_info(pose_name)
    
    # 將動作名稱與 YouTube ID 傳給前端
    return render_template('dashboard.html', 
                           target_pose=pose_name, 
                           youtube_id=info.get('youtube_id'))

# --- API: 前端 JS 輪詢狀態用 ---
@app.route('/get_status')
def get_status():
    return jsonify(state_manager.get_status())

# --- API: 倒數結束，觸發 AI 分析 ---
@app.route('/trigger_analysis', methods=['POST'])
def trigger_analysis():
    # 1. 取得當下鎖定的數據
    data = state_manager.get_status()
    score = data['score']
    image = data['image']
    pose = state_manager.get_target_pose()
    
    # [修正點] 2. 必須取得使用者個資
    profile = state_manager.get_user_profile()
    
    print(f"觸發分析 -> 動作: {pose}, 分數: {score}")

    # [修正點] 3. 呼叫 AI 時傳入 user_profile
    # generate_advice(api_key, pose_name, score, user_profile, image_data)
    advice = generate_advice(
        api_key=GEMINI_API_KEY, 
        pose_name=pose, 
        score=score, 
        user_profile=profile, 
        image_data=image
    )
    
    return jsonify({"status": "ok", "advice": advice})

# --- API: 接收板子傳來的資料 ---
@app.route('/receive_pose', methods=['POST'])
def receive_pose():
    data = request.json
    score = data.get('score', 0)
    image = data.get('image', "")
    # 更新狀態
    state_manager.update_data(score, image)
    return jsonify({"status": "ok"})

# --- API: 給板子問指令 ---
@app.route('/get_command')
def get_command():
    return jsonify({"command": state_manager.get_target_pose()})

if __name__ == '__main__':
    # 啟動 Server
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)