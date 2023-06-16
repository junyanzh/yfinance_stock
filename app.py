from flask import Flask, request, jsonify
import yfinance as yf
from datetime import datetime, timedelta
import os
app = Flask(__name__)

@app.route('/api', methods=['POST'])
def compare_stocks():
    data = request.get_json()
    ticker1 = data['ticker1']
    ticker2 = data['ticker2']
    
    end = datetime.today().strftime('%Y-%m-%d')
    start = (datetime.today() - timedelta(days=10)).strftime('%Y-%m-%d')
    
    try:
        ticker1_data = yf.download(ticker1, start=start, end=end)
        ticker2_data = yf.download(ticker2, start=start, end=end)
    except Exception as e:
        return jsonify({'error': f'Could not retrieve ticker: {e}'})

    ticker1_change = (ticker1_data['Close'][-1] - ticker1_data['Close'][0]) / ticker1_data['Close'][0]
    ticker2_change = (ticker2_data['Close'][-1] - ticker2_data['Close'][0]) / ticker2_data['Close'][0]
    
    if ticker1_change > ticker2_change:
        return jsonify({'ticker': ticker1, 'change': ticker1_change})
    else:
        return jsonify({'ticker': ticker2, 'change': ticker2_change})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
