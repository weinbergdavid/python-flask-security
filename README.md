
<h4>Python Flask-Security Example</h4>
This is working example of login for flask framework based on Falsk-Security extention. The example based on this <a href="http://mandarvaze.github.io/2015/01/token-auth-with-flask-security.html">blog</a><br/>
The example tested on python 3.5.1 with PyCharm on windows.
<br/><br/><br/>
<h5>How to run this example?</h5>
<br/>
Open cmd and run:<br/>
  1. cd /path-to-dir/<br/>
  2. pip install -r ./requirements.txt<br/>
  3. python run.py<br/>
<br/>

Open another CMD and run:<br/>
  1. cd /path-to-dir/<br/>
  2. http 127.0.0.1:5001/dummy-api-anonymous/<br/>
  3. http -a test@example.com:test123 127.0.0.1:5001/dummy-api-http/<br/>
  4. python get_token.py<br/>
  5. http 127.0.0.1:5001/dummy-api-token/  Authentication-Token:<token from get_token scirpt><br/>


The result need to be like this image:
<img src="https://github.com/weinbergdavid/python-flask-security/blob/master/api-example.PNG"></img>
