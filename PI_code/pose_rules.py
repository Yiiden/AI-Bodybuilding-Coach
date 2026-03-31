# pose_rules.py
# 定義各個健美動作的評分規則 (依據 IFBB Men's Bodybuilding Rules 2024)

RULES = {
    # =========================================
    # 1. 正面擴背肌 (Front Lat Spread)
    # =========================================
    "Front Lat Spread": [
        # 上半身 V 型 (關鍵) - 手肘向外撐開
        {'p1': 'l_shldr', 'p2': 'l_elbow', 'weight': 3.0, 'name': 'L_Lat_Flare'},
        {'p1': 'l_elbow', 'p2': 'l_wrist', 'weight': 3.0, 'name': 'L_Hand_Hip'},
        {'p1': 'r_shldr', 'p2': 'r_elbow', 'weight': 3.0, 'name': 'R_Lat_Flare'},
        {'p1': 'r_elbow', 'p2': 'r_wrist', 'weight': 3.0, 'name': 'R_Hand_Hip'},
        # 肩膀水平
        {'p1': 'l_shldr', 'p2': 'r_shldr', 'weight': 3.0, 'name': 'Shoulders_Level'},
        # 下半身 (站姿)
        {'p1': 'l_hip',   'p2': 'l_knee',  'weight': 1.5, 'name': 'L_Leg_Stand'},
        {'p1': 'r_hip',   'p2': 'r_knee',  'weight': 1.5, 'name': 'R_Leg_Stand'},
    ],

    # =========================================
    # 2. 正面雙二頭肌 (Front Double Biceps)
    # =========================================
    "Front Double Biceps": [
        # 雙臂展示 (最關鍵) - 手肘水平，前臂內收
        {'p1': 'l_shldr', 'p2': 'l_elbow', 'weight': 4.0, 'name': 'L_Arm_Level'},
        {'p1': 'r_shldr', 'p2': 'r_elbow', 'weight': 4.0, 'name': 'R_Arm_Level'},
        {'p1': 'l_elbow', 'p2': 'l_wrist', 'weight': 4.0, 'name': 'L_Bicep_Peak'},
        {'p1': 'r_elbow', 'p2': 'r_wrist', 'weight': 4.0, 'name': 'R_Bicep_Peak'},
        # 肩膀與X-Frame
        {'p1': 'l_shldr', 'p2': 'r_shldr', 'weight': 2.0, 'name': 'Shoulders_Width'},
        # 下半身 (腿部外展)
        {'p1': 'l_hip',   'p2': 'l_knee',  'weight': 1.5, 'name': 'L_Leg_Flare'},
        {'p1': 'r_hip',   'p2': 'r_knee',  'weight': 1.5, 'name': 'R_Leg_Flare'},
    ],

    # =========================================
    # 3. 側面胸肌 (Side Chest)
    # =========================================
    "Side Chest": [
        # 展現側的手臂 (彎曲成直角)
        {'p1': 'r_shldr', 'p2': 'r_elbow', 'weight': 4.0, 'name': 'R_Arm_90'},
        {'p1': 'r_elbow', 'p2': 'r_wrist', 'weight': 4.0, 'name': 'R_Arm_Grip'},
        {'p1': 'l_shldr', 'p2': 'l_elbow', 'weight': 4.0, 'name': 'L_Arm_90'},
        {'p1': 'l_elbow', 'p2': 'l_wrist', 'weight': 4.0, 'name': 'L_Arm_Grip'},
        # 腿部 (彎曲並踮腳尖)
        {'p1': 'r_hip',   'p2': 'r_knee',  'weight': 2.0, 'name': 'R_Leg_Bend'},
        {'p1': 'r_knee',  'p2': 'r_ankle', 'weight': 2.0, 'name': 'R_Calf_Flex'},
        {'p1': 'l_hip',   'p2': 'l_knee',  'weight': 2.0, 'name': 'L_Leg_Bend'},
        {'p1': 'l_knee',  'p2': 'l_ankle', 'weight': 2.0, 'name': 'L_Calf_Flex'},
        # 軀幹挺胸
        {'p1': 'r_shldr', 'p2': 'r_hip',   'weight': 1.5, 'name': 'R_Torso_Arch'},
        {'p1': 'l_shldr', 'p2': 'l_hip',   'weight': 1.5, 'name': 'L_Torso_Arch'},
    ],

    # =========================================
    # 4. 背面雙二頭肌 (Back Double Biceps)
    # =========================================
    "Back Double Biceps": [
        # 手臂 (與正面類似，高權重)
        {'p1': 'l_shldr', 'p2': 'l_elbow', 'weight': 4.0, 'name': 'L_Arm_Level'},
        {'p1': 'r_shldr', 'p2': 'r_elbow', 'weight': 4.0, 'name': 'R_Arm_Level'},
        {'p1': 'l_elbow', 'p2': 'l_wrist', 'weight': 3.5, 'name': 'L_Forearm'},
        {'p1': 'r_elbow', 'p2': 'r_wrist', 'weight': 3.5, 'name': 'R_Forearm'},
        # 下半身 (重點：一腳向後踮起展示小腿)
        {'p1': 'l_hip',   'p2': 'l_knee',  'weight': 2.0, 'name': 'L_Leg_Back'},
        {'p1': 'r_hip',   'p2': 'r_knee',  'weight': 2.0, 'name': 'R_Leg_Back'},
        {'p1': 'l_knee',  'p2': 'l_ankle', 'weight': 2.0, 'name': 'L_Calf_Show'},
        {'p1': 'r_knee',  'p2': 'r_ankle', 'weight': 2.0, 'name': 'R_Calf_Show'},
    ],

    # =========================================
    # 5. 背面擴背肌 (Back Lat Spread)
    # =========================================
    "Back Lat Spread": [
        # 背闊肌展開 (手肘向外)
        {'p1': 'l_shldr', 'p2': 'l_elbow', 'weight': 3.5, 'name': 'L_Lat_Width'},
        {'p1': 'r_shldr', 'p2': 'r_elbow', 'weight': 3.5, 'name': 'R_Lat_Width'},
        # 手插腰
        {'p1': 'l_elbow', 'p2': 'l_wrist', 'weight': 2.5, 'name': 'L_Hand_Pos'},
        {'p1': 'r_elbow', 'p2': 'r_wrist', 'weight': 2.5, 'name': 'R_Hand_Pos'},
        # 腿部 (一腳向後)
        {'p1': 'l_hip',   'p2': 'l_knee',  'weight': 1.5, 'name': 'L_Leg_Pose'},
        {'p1': 'r_hip',   'p2': 'r_knee',  'weight': 1.5, 'name': 'R_Leg_Pose'},
    ],

    # =========================================
    # 6. 側面三頭肌 (Side Triceps)
    # =========================================
    "Side Triceps": [
        # 展示臂 (用力伸直，手腕被抓住)
        {'p1': 'r_shldr', 'p2': 'r_elbow', 'weight': 4.5, 'name': 'R_Tri_Straight'},
        {'p1': 'r_elbow', 'p2': 'r_wrist', 'weight': 4.5, 'name': 'R_Tri_Flex'},
        {'p1': 'l_shldr', 'p2': 'l_elbow', 'weight': 4.5, 'name': 'L_Tri_Straight'},
        {'p1': 'l_elbow', 'p2': 'l_wrist', 'weight': 4.5, 'name': 'L_Tri_Flex'},
        # 腿部 (側面展示)
        {'p1': 'r_hip',   'p2': 'r_knee',  'weight': 2.0, 'name': 'R_Leg_Side'},
        {'p1': 'l_hip',   'p2': 'l_knee',  'weight': 2.0, 'name': 'L_Leg_Side'},
    ],

    # =========================================
    # 7. 腹肌與腿部 (Abdominals and Thighs)
    # =========================================
    "Abdominals and Thighs": [
        # 雙手抱頭 (手肘向上或向外)
        {'p1': 'l_shldr', 'p2': 'l_elbow', 'weight': 3.0, 'name': 'L_Arm_Head'},
        {'p1': 'r_shldr', 'p2': 'r_elbow', 'weight': 3.0, 'name': 'R_Arm_Head'},
        # 腿部 (一腳向前伸出並用力踩地)
        {'p1': 'l_hip',   'p2': 'l_knee',  'weight': 3.5, 'name': 'L_Leg_Front'},
        {'p1': 'l_knee',  'p2': 'l_ankle', 'weight': 3.5, 'name': 'L_Quad_Flex'},
        {'p1': 'r_hip',   'p2': 'r_knee',  'weight': 3.5, 'name': 'R_Leg_Front'},
        {'p1': 'r_knee',  'p2': 'r_ankle', 'weight': 3.5, 'name': 'R_Quad_Flex'},
    ]
}