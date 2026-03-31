import os
import sys
import cv2
import numpy as np
from numpy.linalg import norm

# 引入剛剛寫好的規則
try:
    from pose_rules import RULES
except ImportError:
    print("警告: 找不到 pose_rules.py，將無法取得評分規則。")
    RULES = {}

# 嘗試匯入 Kneron SDK
try:
    import kp
except ImportError:
    print("錯誤: 找不到 'kp' 模組。")
    sys.exit(1)

# 匯入 KL730HRNet 的輔助函式
try:
    from KL730HRNet import decode_heatmap_to_keypoints, _to_numpy, _get_model_input_hw
except ImportError:
    pass

# ==========================================
# Part 1: KL730 HRNet 推論封裝 
# ==========================================
class HRNetInferencer:
    def __init__(self, port_id=0, fw_path=None, model_path=None):
        self.device_group = None
        
        # 1. 連接裝置
        print(f'[Device] Connecting to port {port_id}...')
        try:
            self.device_group = kp.core.connect_devices(usb_port_ids=[port_id])
            kp.core.set_timeout(device_group=self.device_group, milliseconds=10000)
            print(' - Success')
        except Exception as e:
            print(f'Error connecting to device: {e}')
            raise e

        # 2. 上傳 Firmware (重要修正：ncpu_fw_path 必須是空字串)
        if fw_path:
            print(f'[Firmware] Loading from {fw_path}...')
            kp.core.load_firmware_from_file(device_group=self.device_group,
                                            scpu_fw_path=fw_path,
                                            ncpu_fw_path='')
        
        # 3. 上傳模型
        if model_path:
            print(f'[Model] Loading from {model_path}...')
            self.model_nef_descriptor = kp.core.load_model_from_file(device_group=self.device_group,
                                                                     file_path=model_path)
            try:
                self.in_h, self.in_w = _get_model_input_hw(self.model_nef_descriptor)
            except:
                self.in_h, self.in_w = 256, 192 # Fallback
            print(f' - Success (Input Size: {self.in_w}x{self.in_h})')
        else:
            print("Error: Model path not specified.")
            sys.exit(1)

    def predict(self, img_input):
        # 處理輸入 (支援路徑或 numpy array)
        if isinstance(img_input, str):
            if not os.path.exists(img_input):
                return np.zeros((17, 2)), np.zeros(17)
            img_bgr = cv2.imread(img_input)
        else:
            img_bgr = img_input

        if img_bgr is None:
            return np.zeros((17, 2)), np.zeros(17)

        orig_h, orig_w = img_bgr.shape[:2]

        # Resize & Color Convert
        resized = cv2.resize(img_bgr, (self.in_w, self.in_h), interpolation=cv2.INTER_LINEAR)
        img_bgr565 = cv2.cvtColor(resized, cv2.COLOR_BGR2BGR565)

        # Build Descriptor
        generic_desc = kp.GenericImageInferenceDescriptor(
            model_id=self.model_nef_descriptor.models[0].id,
            inference_number=0,
            input_node_image_list=[
                kp.GenericInputNodeImage(
                    image=img_bgr565,
                    resize_mode=kp.ResizeMode.KP_RESIZE_DISABLE,
                    padding_mode=kp.PaddingMode.KP_PADDING_CORNER,
                    normalize_mode=kp.NormalizeMode.KP_NORMALIZE_KNERON,
                    image_format=kp.ImageFormat.KP_IMAGE_FORMAT_RGB565,
                )
            ]
        )

        # Inference
        kp.inference.generic_image_inference_send(
            device_group=self.device_group,
            generic_inference_input_descriptor=generic_desc
        )
        raw = kp.inference.generic_image_inference_receive(device_group=self.device_group)

        # Retrieve & Decode
        out0 = kp.inference.generic_inference_retrieve_float_node(
            node_idx=0,
            generic_raw_result=raw,
            channels_ordering=kp.ChannelOrdering.KP_CHANNEL_ORDERING_CHW,
        )
        
        try:
            heatmap = _to_numpy(out0)
            kpts_list = decode_heatmap_to_keypoints(heatmap, orig_w=orig_w, orig_h=orig_h)
            kps = np.array([[p[0], p[1]] for p in kpts_list], dtype=np.float32)
            scores = np.array([p[2] for p in kpts_list], dtype=np.float32)
            return kps, scores
        except Exception:
            return np.zeros((17, 2)), np.zeros(17)


# ==========================================
# Part 2: 姿勢比對邏輯 (使用 pose_rules)
# ==========================================
class PoseComparator:
    def __init__(self):
        self.KP = {
            'nose': 0, 'l_eye': 1, 'r_eye': 2, 'l_ear': 3, 'r_ear': 4,
            'l_shldr': 5, 'r_shldr': 6, 'l_elbow': 7, 'r_elbow': 8,
            'l_wrist': 9, 'r_wrist': 10, 'l_hip': 11, 'r_hip': 12,
            'l_knee': 13, 'r_knee': 14, 'l_ankle': 15, 'r_ankle': 16
        }

    def get_vector(self, kps, p1_name, p2_name):
        idx1 = self.KP[p1_name]
        idx2 = self.KP[p2_name]
        if idx1 >= len(kps) or idx2 >= len(kps): return None
        return kps[idx2] - kps[idx1]

    def cosine_similarity(self, v1, v2):
        norm1 = norm(v1)
        norm2 = norm(v2)
        if norm1 == 0 or norm2 == 0: return 0.0
        return np.dot(v1, v2) / (norm1 * norm2)

    def get_config(self, pose_name):
        # 直接從 RULES 字典中讀取
        return RULES.get(pose_name, [])

    def compare(self, kps_ref, scores_ref, kps_candidate, scores_candidate, pose_name="Front Lat Spread", thr=0.2):
        config = self.get_config(pose_name)
        
        if not config: 
            return 0.0

        total_score = 0
        total_weight = 0

        for item in config:
            p1 = item['p1']
            p2 = item['p2']
            weight = item['weight']
            idx1, idx2 = self.KP[p1], self.KP[p2]
            
            # 信心過濾
            if (scores_ref[idx1] < thr or scores_ref[idx2] < thr or 
                scores_candidate[idx1] < thr or scores_candidate[idx2] < thr):
                continue

            # 計算向量與相似度
            vec_ref = self.get_vector(kps_ref, p1, p2)
            vec_cand = self.get_vector(kps_candidate, p1, p2)

            sim = self.cosine_similarity(vec_ref, vec_cand)
            score_part = max(0, sim) * 100 
            
            total_score += score_part * weight
            total_weight += weight

        if total_weight == 0:
            return 0.0

        return total_score / total_weight