import requests
from bs4 import BeautifulSoup
from flask import Flask
import datetime

app = Flask(__name__)

@app.route('/')
def get_weather():
    # スクレイピング対象：Yahoo!天気（東京）
    url = "https://weather.yahoo.co.jp/weather/jp/13/4410.html"
    
    try:
        # タイムアウトを設定して接続
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        
        # タイトルとメインの天気予報ブロックを取得
        title = soup.title.text
        forecast_box = soup.find(class_="forecastCity")
        
        if forecast_box:
            # 構造変更に対応できるよう安全に取得
            weather_node = forecast_box.find(class_="weather")
            weather_text = weather_node.p.img['alt'] if weather_node else "取得失敗"
            icon_url = weather_node.p.img['src'] if weather_node else ""
        else:
            weather_text = "情報が見つかりません"
            icon_url = ""

        # 現在時刻（コンテナ内時刻）
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return f"""
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Docker Weather App</title>
            <style>
                body {{ font-family: sans-serif; text-align: center; padding: 50px; background-color: #f0f2f5; }}
                .card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: inline-block; }}
                h1 {{ color: #333; }}
                .weather-text {{ font-size: 24px; font-weight: bold; color: #007bff; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>東京の天気</h1>
                <p>取得元: {title}</p>
                <div>
                    <img src="{icon_url}" alt="{weather_text}">
                    <p class="weather-text">{weather_text}</p>
                </div>
                <hr>
                <p><small>Access Time: {now}</small></p>
                <p><small>Powered by Flask & Docker</small></p>
            </div>
        </body>
        </html>
        """

    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
