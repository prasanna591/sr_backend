from flask import Flask,jsonify,request
from flask_cors import CORS
import pandas as pd
from difflib import get_close_matches

app = Flask(__name__)
CORS(app)

df =pd.read_csv("skill_recommendation_dataset.csv")

career_goals = df['Career Goal'].str.lower().tolist()

@app.route('/')
def home():
    return jsonify({"message":"welcome to the recommendation"})

@app.route('/recommend',methods=['GET'])
def recommend_skills():

    user_goal = request.args.get('goal', '').strip().lower()
    
    match = get_close_matches(user_goal,career_goals, n=1, cutoff=0.3)


    if match:
        matched_goal = match[0]
        result = df[df['Career Goal'].str.lower() == matched_goal].iloc[0]

        return jsonify({
            "match":result['Career Goal'],
            "recommended_skills":result['Recommended Skills'],
            "recommended_projects": result['Recommended Projects']
        })
      
    else:
        return jsonify({"error": "sorry, no recommendation found ,try a different career goal"}), 404
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)

