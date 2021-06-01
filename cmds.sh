gunicorn -w 4 -b 127.0.0.1:10086 paint_color_api_flask:app --reload

