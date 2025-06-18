from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os
import socket
import logging
from logging.config import dictConfig
import time
from models import Location, get_db, init_db
from sqlalchemy.orm import Session

# ログ設定
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'WARNING'
        }
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['console']
    },
    'werkzeug': {
        'level': 'WARNING',
        'handlers': ['console']
    }
})

app = Flask(__name__)
CORS(app)

# アクセスカウンター
request_count = {'get': 0, 'post': 0}
last_status_time = time.time()

@app.before_request
def count_request():
    """リクエストをカウントし、定期的にステータスを表示"""
    global last_status_time
    current_time = time.time()
    
    if request.endpoint != 'static':
        if request.method == 'GET':
            request_count['get'] += 1
        elif request.method == 'POST':
            request_count['post'] += 1

    # 30秒ごとにステータスを表示
    if current_time - last_status_time >= 30:
        print(f"\n[サーバーステータス]")
        print(f"合計リクエスト数: GET={request_count['get']}, POST={request_count['post']}")
        last_status_time = current_time

def get_local_ip():
    """ローカルIPアドレスを取得"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'

@app.route('/')
def index():
    """Web UIを提供"""
    # Renderの公開URLを直接渡す（httpやポート番号を含めず）
    public_url = os.getenv('PUBLIC_URL', 'https://soleiltest.onrender.com')
    # http(s)://が重複しないように整形
    public_url = public_url.replace('http://', '').replace('https://', '')
    public_url = f'https://{public_url}'
    return render_template('index.html', server_ip=public_url)

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({'message': 'Pythonサーバーからの応答です！'})

@app.route('/api/location', methods=['GET', 'POST', 'DELETE'])
def handle_location():
    db: Session = next(get_db())
    
    if request.method == 'POST':
        data = request.get_json()
        if not all(key in data for key in ['place_pos', 'count_person']):
            return jsonify({
                'status': 'エラー',
                'message': '必要なデータが不足しています（place_pos, count_person が必要です）'
            }), 400

        try:
            # 既存のレコードを確認
            location = db.query(Location).filter(Location.place_pos == data['place_pos']).first()
            
            if location:
                # 既存のレコードを更新
                location.count_person = data['count_person']
                if 'timestamp' in data:
                    location.timestamp = data['timestamp']
            else:
                # 新しいレコードを作成
                location = Location(
                    place_pos=data['place_pos'],
                    count_person=data['count_person'],
                    timestamp=data.get('timestamp')
                )
                db.add(location)
            
            db.commit()
            return jsonify({'status': '成功', 'message': 'データが保存されました'})
            
        except Exception as e:
            db.rollback()
            return jsonify({
                'status': 'エラー',
                'message': f'データの保存中にエラーが発生しました: {str(e)}'
            }), 500
    
    elif request.method == 'DELETE':
        place = request.args.get('place')
        if not place:
            return jsonify({
                'status': 'エラー',
                'message': '削除する場所を指定してください'
            }), 400

        try:
            location = db.query(Location).filter(Location.place_pos == place).first()
            if location:
                db.delete(location)
                db.commit()
                return jsonify({'status': '成功', 'message': f'{place}のデータを削除しました'})
            else:
                return jsonify({'status': 'エラー', 'message': f'{place}のデータが見つかりません'}), 404
                
        except Exception as e:
            db.rollback()
            return jsonify({
                'status': 'エラー',
                'message': f'データの削除中にエラーが発生しました: {str(e)}'
            }), 500
    
    # GETリクエストの場合、保存されているデータを全て返す
    try:
        locations = db.query(Location).all()
        return jsonify({'locations': [location.to_dict() for location in locations]})
    except Exception as e:
        return jsonify({
            'status': 'エラー',
            'message': f'データの取得中にエラーが発生しました: {str(e)}'
        }), 500

# データベースの初期化（本番環境でも必ず実行）
init_db()

# if __name__ == '__main__':
#     # 起動時のメッセージを表示
#     local_ip = get_local_ip()
#     print(f"\nサーバーが起動しました！")
#     print(f"アクセス用アドレス:")
#     print(f"------------------------")
#     print(f"PC/スマートフォン: http://{local_ip}:5000")
#     print(f"Unity: {local_ip}:5000")
#     print(f"------------------------\n")
#     
#     app.run(debug=False, host='0.0.0.0', port=5000)
