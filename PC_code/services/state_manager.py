class StateManager:
    def __init__(self):
        self.data = {
            "target_pose": "Front Lat Spread",
            "score": 0,
            "image": "", # Base64 string
            "user_profile": {
                "height": "",
                "weight": "",
                "age": ""
            }
        }

    def set_target_pose(self, pose_name):
        self.data["target_pose"] = pose_name

    def get_target_pose(self):
        return self.data["target_pose"]

    def update_data(self, score, image):
        self.data["score"] = score
        # 只有當板子真的有傳圖過來才更新，避免空圖覆蓋
        if image:
            self.data["image"] = image

    def get_status(self):
        return {
            "score": self.data["score"],
            "image": self.data["image"]
        }
    
    def set_user_profile(self, height, weight, age):
        self.data["user_profile"] = {
            "height": height,
            "weight": weight,
            "age": age
        }
    
    def get_user_profile(self):
        return self.data["user_profile"]

# 建立一個單例實體 (Singleton) 供 app.py 引用
state_manager = StateManager()