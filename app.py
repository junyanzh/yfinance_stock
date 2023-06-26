from flask import Flask, request, jsonify
import yfinance as yf
from datetime import datetime, timedelta
import os
app = Flask(__name__)
####
@app.route('/api', methods=['POST'])
def compare_stocks():
    data = request.get_json()
    ticker1 = data['ticker1']
    ticker2 = data['ticker2']
    ticker3 = data['ticker3']  # 新增的第三個股票
    
    end = datetime.today().strftime('%Y-%m-%d')
    start = (datetime.today() - timedelta(days=10)).strftime('%Y-%m-%d')
    
    try:
        ticker1_data = yf.download(ticker1, start=start, end=end)
        ticker2_data = yf.download(ticker2, start=start, end=end)
        ticker3_data = yf.download(ticker3, start=start, end=end)  # 新增的第三個股票的資料
    except Exception as e:
        return jsonify({'error': f'Could not retrieve ticker: {e}'})

    ticker1_change = (ticker1_data['Close'][-1] - ticker1_data['Close'][0]) / ticker1_data['Close'][0]
    ticker2_change = (ticker2_data['Close'][-1] - ticker2_data['Close'][0]) / ticker2_data['Close'][0]
    ticker3_change = (ticker3_data['Close'][-1] - ticker3_data['Close'][0]) / ticker3_data['Close'][0]  # 新增的第三個股票的變化
    
    # 用來比較三個股票的變化
    changes = {
        'ticker1': ticker1_change,
        'ticker2': ticker2_change,
        'ticker3': ticker3_change,
    }
    
    max_ticker = max(changes, key=changes.get)
    
    return jsonify({'ticker': max_ticker, 'change': changes[max_ticker]})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
