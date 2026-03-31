import google.generativeai as genai
from services.pose_library import get_pose_info

def generate_advice(api_key, pose_name, score, user_profile, image_data=None):
    if not api_key or api_key == "YOUR_API_KEY":
        return "錯誤：請先在 app.py 設定 Gemini API Key。"

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        # 取得該動作專屬的 Prompt
        pose_info = get_pose_info(pose_name)
        specific_rules = pose_info.get("prompt_template", "無特定規則")
        
        prompt = f"""
        你現在是專業健美教練。學員資料如下：
        - 年紀：{user_profile.get('age')} 歲
        - 身高：{user_profile.get('height')} cm
        - 體重：{user_profile.get('weight')} kg
    
        學員剛剛完成了 '{pose_name}' 的動作定格。
        系統經由骨架運算給出的評分是：{score:.2f} / 100。

        該動作的評分重點如下：
        {specific_rules}
    
        請用繁體中文回答，回答風格盡量簡明扼要，沒有冗言贅字。
        根據分數與學員身體素質，給出 3 點具體建議。
        """
        
        # 未來如果想傳圖片給 AI，可以在這裡把 image_data (base64) 轉成圖片物件傳入
        # 目前為了速度與省錢，我們先只傳文字 prompt
        
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f"Backend Error: {str(e)}") # 在終端機印出錯誤以便除錯
        return f"AI 發生錯誤: {str(e)}"