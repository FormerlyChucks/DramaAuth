from flask import Flask, redirect, render_template, request, make_response
import requests

app = Flask(__name__,static_url_path='')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/authorize', methods=['POST'])
def authorize():
    client_id = request.form.get('auth_cid')
    client_secret = request.form.get('auth_secret')
    scopes = request.form.get('auth_scopes')
    if client_id and scopes and client_secret:
        authorization_params = {'client_id': client_id,
                                'redirect_uri': 'http://localhost:8888/grant',
                                'state': 'wtf',
                                'scope': scopes,
                                'permanent': 'true'}
        authorize_user = requests.post('https://rdrama.ga/oauth/authorize',params=authorization_params)
        if authorize_user.status_code == 200:
            response = make_response(redirect(authorize_user.url))
            response.set_cookie('client_id', client_id)
            response.set_cookie('client_secret', client_secret)
            return response
        else:
            return render_template('index.html',error=authorize_user['oauth_error'])
    else:
        return render_template('index.html',error='All Values Must Be Supplied')

@app.route('/grant', methods=['GET'])
def grant():
    code = request.args.get('code')
    client_id = request.cookies.get('client_id')
    client_secret = request.cookies.get('client_secret')
    grant_data = {'client_id': client_id,
                  'client_secret': client_secret,
                  'grant_type': 'code',
                  'code': code}
    grant_user = requests.post('https://rdrama.ga/oauth/grant', data=grant_data)
    if grant_user.status_code == 200:
        response = make_response(render_template('index.html',j=gdata.json()))
        response.delete_cookie('client_secret')
        response.delete_cookie('client_id')
        return response
    else:
        return render_template('index.html',error=gdata['oauth_error'])

if __name__ == '__main__':
    app.run()
