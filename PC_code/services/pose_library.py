# services/pose_library.py

POSE_DATA = {
    "Front Double Biceps": {
        "name_zh": "正面雙二頭肌",
        "img_filename": "Figure1_Front_Double_Biceps.png",
        "youtube_id": "TgqynNtxroY?si=nCzAvl9KmS06z6jU",
        "prompt_template": """
        動作：正面雙二頭肌 (Front Double Biceps)
        重點檢查：
        1. 【手臂高度】：雙臂應舉至水平或略高於肩膀，不可過低。
        2. 【二頭肌峰】：檢查二頭肌的收縮程度與肌峰高度。
        3. 【X-Frame】：寬肩、細腰、腿部外展應呈現 X 字型體態。
        4. 【前臂控制】：前臂應向內彎曲以擠壓二頭肌。
        """
    },
    "Front Lat Spread": {
        "name_zh": "正面擴背肌",
        "img_filename": "Figure2_Front_Lat_Spread.png", # 教科書圖片 (請放在 static/images/)
        "youtube_id": "RLT7zJGXiho?si=4QZKLf-xmiUDuT5O", 
        "prompt_template": """
        動作：正面擴背肌 (Front Lat Spread)
        重點檢查：
        1. 【背闊肌展開】：檢查背部是否呈現寬闊的 V 字型，這是此動作的關鍵。
        2. 【手部位置】：雙手是否正確插在腰際，手肘是否向外推以撐開背肌。
        3. 【對稱性】：雙肩應保持水平，不可歪斜。
        4. 【腿部】：雙腿應站穩並繃緊，展現大腿線條。
        """
    },
    # --- 3. 側面胸肌 (新) ---
    "Side Chest": {
        "name_zh": "側面胸肌",
        "img_filename": "Figure3_Side_Chest.png", # 請自行修改檔名
        "youtube_id": "Z-DvXUks_HA",
        "prompt_template": """
        動作：側面胸肌 (Side Chest)
        重點檢查：
        1. 【手臂角度】：靠近裁判的手臂應彎曲成直角 (90度)，握住另一手的手腕。
        2. 【胸肌厚度】：胸部應向上挺起並用力擠壓，展現飽滿度。
        3. 【腿部細節】：前腿應彎曲並踮起腳尖，展現小腿與大腿後側 (Hamstring) 線條。
        4. 【二頭肌】：彎曲的手臂應同時展示二頭肌的飽滿度。
        """
    },

    # --- 4. 背面雙二頭肌 (新) ---
    "Back Double Biceps": {
        "name_zh": "背面雙二頭肌",
        "img_filename": "Figure4_Back_Double_Biceps.png", # 請自行修改檔名
        "youtube_id": "kuHtzeXfN_Y",
        "prompt_template": """
        動作：背面雙二頭肌 (Back Double Biceps)
        重點檢查：
        1. 【背部細節】：檢查背部肌群的分離度，包括斜方肌、大圓肌與豎脊肌 (聖誕樹)。
        2. 【手臂姿勢】：與正面動作類似，手臂應保持水平，展示三頭肌與二頭肌線條。
        3. 【下肢狀態】：一腳應向後踮起，展示臀大肌 (Glutes) 與大腿後側 (Hamstrings) 的緊實度。
        4. 【整體比例】：檢查上下半身的比例與倒三角體型。
        """
    },

    # --- 5. 背面擴背肌 (新) ---
    "Back Lat Spread": {
        "name_zh": "背面擴背肌",
        "img_filename": "Figure5_Back_Lat_Spread.png", # 請自行修改檔名
        "youtube_id": "yl0mGgQou9Q",
        "prompt_template": """
        動作：背面擴背肌 (Back Lat Spread)
        重點檢查：
        1. 【背部寬度】：背闊肌應向兩側極致展開，寬度是首要評分標準。
        2. 【手肘位置】：手插腰時，手肘應盡量向前向外推，幫助背肌展開。
        3. 【肌肉密度】：除了寬度，亦需觀察背部肌肉的厚度與擠壓感。
        4. 【下肢展示】：一腳向後踮起，展示小腿肌肉 (Calf) 的收縮。
        """
    },

    # --- 6. 側面三頭肌 (新) ---
    "Side Triceps": {
        "name_zh": "側面三頭肌",
        "img_filename": "Figure6_Side_Triceps.png", # 請自行修改檔名
        "youtube_id": "lZhMqbyAF-c",
        "prompt_template": """
        動作：側面三頭肌 (Side Triceps)
        重點檢查：
        1. 【三頭肌展示】：展示臂應在背後被另一手抓住，並用力伸直，展現三頭肌的馬蹄形線條。
        2. 【腹部控制】：腹外斜肌與腹直肌應保持緊縮，不可放鬆凸出。
        3. 【腿部線條】：側面站立時，大腿外側 (股外側肌) 與小腿應全程用力。
        4. 【挺胸】：胸部應保持挺起，展現上半身氣勢。
        """
    },

    # --- 7. 腹肌與腿部 (新) ---
    "Abdominals and Thighs": {
        "name_zh": "腹肌與腿部",
        "img_filename": "Figure7_Abdominals_and_Thighs.png", # 請自行修改檔名
        "youtube_id": "kTJOwpy2k9A",
        "prompt_template": """
        動作：腹肌與腿部 (Abdominals and Thighs)
        重點檢查：
        1. 【手部位置】：雙手應抱於頭後，不可遮住臉部或頸部。
        2. 【腹肌分離度】：腹直肌 (六塊肌) 應明顯收縮，展現深邃的切割線。
        3. 【腿部展示】：前伸的一腳應用力踩地，展現股四頭肌的線條與分離度。
        4. 【軀幹姿勢】：身體可微向前捲曲 (Crunch) 以極大化腹肌收縮，但不可過度彎腰。
        """
    }
    # 您可以在這裡繼續擴充其他 5 個動作...
}

def get_pose_info(pose_name):
    return POSE_DATA.get(pose_name, {})