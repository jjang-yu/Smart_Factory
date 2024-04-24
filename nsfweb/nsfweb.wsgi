# nsfweb.wsgi
import sys
import site

# 가상 환경의 site-packages 디렉터리 경로
site.addsitedir('/usr/lib/python3.9/dist-packages')

# 애플리케이션의 경로 추가
sys.path.insert(0, '/var/www/nsfweb')

from app import app as application

