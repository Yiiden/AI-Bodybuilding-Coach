import argparse
import requests
import cv2
import base64
import platform
import sys
import os
import time

# 引入模組
try:
    from compare_pose import HRNetInferencer, PoseComparator
except ImportError:
    print("錯誤：找不到 compare_pose.py")
    sys.exit(1)

# --- 工具函式 ---
def open_cap(src):
    is_windows = platform.system().lower().startswith("win")
    if src.isdigit():
        idx = int(src)
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW if is_windows else cv2.CAP_V4L2)
    else:
        backend = 0
        if not is_windows and src.startswith("/dev/video"):
            backend = cv2.CAP_V4L2
        cap = cv2.VideoCapture(src, backend)
    return cap

def draw_skeleton(img, kps, score):
    # 定義連線
    connections = [
        (0, 1), (0, 2), (1, 3), (2, 4), # Face
        (5, 6), (5, 7), (7, 9), (6, 8), (8, 10), # Arms
        (5, 11), (6, 12), (11, 12), # Torso
        (11, 13), (13, 15), (12, 14), (14, 16) # Legs
    ]
    
    # 畫點 (黃色)
    for i, (x, y) in enumerate(kps):
        if x < 1 and y < 1: continue 
        cv2.circle(img, (int(x), int(y)), 4, (0, 255, 255), -1)

    # 畫線 (綠色)
    for i, j in connections:
        if i >= len(kps) or j >= len(kps): continue
        pt1 = (int(kps[i][0]), int(kps[i][1]))
        pt2 = (int(kps[j][0]), int(kps[j][1]))
        
        if (pt1[0] < 1 or pt1[1] < 1 or pt2[0] < 1 or pt2[1] < 1):
            continue
        cv2.line(img, pt1, pt2, (0, 255, 0), 2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', default="8", help="相機來源 (通常是 8)")
    parser.add_argument('--ip', default='172.20.10.5', help='Laptop IP')
    
    # 預設圖片資料夾
    parser.add_argument('--ref_dir', default='reference_photo', help='標準動作圖資料夾')
    
    args = parser.parse_args()

    # 1. 初始化 AI
    print("=== 初始化 AI 模型 ===")
    try:
        inferencer = HRNetInferencer(port_id=0, 
                                     fw_path='res/firmware/KL730/kp_firmware.tar', 
                                     model_path='res/models/KL730/HRNet/models_730.nef')
        comparator = PoseComparator()
    except Exception as e:
        print(f"初始化失敗: {e}")
        return

    # 2. 預載參考圖 (快取)
    # 定義動作名稱與檔名的對應 (請確保圖片放在 reference_photo 資料夾下)
    ref_files = {
        "Front Lat Spread": "Figure2_Front_Lat_Spread.png",
        "Front Double Biceps": "Figure1_Front_Double_Biceps.png",
        "Side Chest": "Figure3_Side_Chest.png",
        "Back Double Biceps": "Figure4_Back_Double_Biceps.png",
        "Back Lat Spread": "Figure5_Back_Lat_Spread.png",
        "Side Triceps": "Figure6_Side_Triceps.png",
        "Abdominals and Thighs": "Figure7_Abdominals_and_Thighs.png"
    }

    ref_db = {}
    print("=== 載入標準動作參考圖 ===")
    
    for pose_name, filename in ref_files.items():
        # 組合完整路徑
        # 注意：如果您原本是用 Figure2_Front_Lat_Spread.png 這種名字，請改檔名或改上面的字典
        path = os.path.join(args.ref_dir, filename)
        
        if os.path.exists(path):
            print(f" -> Loading {pose_name} from {filename}...", end=" ")
            try:
                kps, sc = inferencer.predict(path)
                ref_db[pose_name] = (kps, sc)
                print("OK")
            except Exception as e:
                print(f"Failed: {e}")
        else:
            print(f"⚠️ 找不到: {path} (此動作將無法評分)")

    # 3. 開啟相機
    print(f"=== 開啟相機: {args.src} ===")
    cap = open_cap(args.src)
    if not cap.isOpened():
        print("無法開啟相機")
        return

    # 設定 URL
    cmd_url = f"http://{args.ip}:5001/get_command"
    post_url = f"http://{args.ip}:5001/receive_pose"

    current_mode = "Front Lat Spread"
    
    print("=== 開始串流推論 ===")
    
    while True:
        # 讀圖
        ret, frame = cap.read()
        if not ret: break

        # 縮圖 (240x180)
        frame_resized = cv2.resize(frame, (240, 180))
        
        try:
            # 問模式
            try:
                resp = requests.get(cmd_url, timeout=0.1)
                if resp.status_code == 200:
                    current_mode = resp.json().get("command", current_mode)
            except:
                pass 

            # 推論
            kps_user, scores_user = inferencer.predict(frame_resized)
            
            # 算分
            final_score = 0
            if current_mode in ref_db:
                kps_ref, scores_ref = ref_db[current_mode]
                final_score = comparator.compare(kps_ref, scores_ref, 
                                                 kps_user, scores_user, 
                                                 pose_name=current_mode, thr=0.2)

            # 畫圖 (只畫骨架，分數由網頁顯示)
            draw_skeleton(frame_resized, kps_user, final_score)

            # 轉 Base64
            _, buffer = cv2.imencode('.jpg', frame_resized, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
            b64_img = base64.b64encode(buffer).decode('utf-8')

            # 發送
            payload = {
                "score": float(final_score),
                "keypoints": kps_user.tolist(),
                "image": b64_img
            }
            requests.post(post_url, json=payload, timeout=3.0)
            
            print(f"\rMode: {current_mode} | Score: {final_score:.1f} | Sending...", end="")

        except Exception as e:
            pass

    cap.release()

if __name__ == "__main__":
    main()