python3 mock_collect.py $1 8 10 data/pages "English Collector" &
python3 mock_process.py $1 8 2 data/pages data/sentiment "Sentiment Analysis" &
python3 mock_collect.py $1 8 10 data/pages-es "Spanish Collector" &
python3 mock_process.py $1 8 2 data/pages-es data/pages-tr "Translation" &
python3 mock_process.py $1 8 2 data/pages-tr data/sentiment-es "Spanish Sentiment Analysis" &
