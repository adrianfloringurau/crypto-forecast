from flask import Flask, request, jsonify
import datetime
import extractor

app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def get_prediction():
    coin = request.args.get('coin') #crypto coin
    time = request.args.get('time') #in miliseconds

    end_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - datetime.timedelta(days=365 * 10)  # 10 years ago

    predicted_price, accuracy = extractor.extract(coin, time, start_date, end_date)
    price_prediction = {
        "coin": coin,
        "time": time,
        "predicted_price": str(predicted_price),
        "accuracy": str(accuracy),
    }

    return jsonify(price_prediction)

if __name__ == '__main__':
    app.run(debug=True)