python3 mock_collect.py $1 8 10 data/pages "English Collector" &

#python3 mock_process.py $1 8 2 data/pages data/sentiment "Sentiment Analysis" &
#python3 mock_collect.py $1 8 10 data/pages-es "Spanish Collector" &
#python3 mock_process.py $1 8 2 data/pages-es data/pages-tr "Translation" &
#python3 mock_process.py $1 8 2 data/pages-tr data/sentiment-es "Spanish Sentiment Analysis" &


#Steps: Clean up group-id make one for URLS - English, Spanish 
# 		Consume the URLS in mock_process. 
#		We don't want auto acknowledgement: only acknowledge when we're done processing
		# look at consumer and make sure it's set to not auto acknowledgement
		# downlaod kafka gui
		# try and figure out why this isn't working god fucking damn it i hate this shit so much 
		# basically the error now is it's running process.py for some reason when 
		# i call mock_collect which should NOT be happening. 