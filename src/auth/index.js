import {router} from '../main';

const LOGIN_URL = 'users/login';
const SIGNUP_URL = 'users/signup';

export default {

  user: {
    authenticated: false
  },

  login(context, creds, redirect) {
    context.$http.post(LOGIN_URL, creds).then(
      data => {
        localStorage.setItem('id_token', data.body.token);

        this.user.authenticated = true;
        if(redirect) {
          router.push({ name: redirect});
        }

      }, err => {
        context.error = err.body;
      });
  },

  signup(context, creds, redirect) {
    context.$http.post(SIGNUP_URL, creds).then(
      data => {
        localStorage.setItem('id_token', data.data.token);

        this.user.authenticated = true;

        if(redirect) {
          router.push({ name: redirect});
        }

      },
      err => {
        context.error = err.body.message;
      });
  },

  logout() {
    localStorage.removeItem('id_token');
    this.user.authenticated = false;
  },

  checkAuth() {
    var token = localStorage.getItem('id_token');
    if(token) {
      this.user.authenticated = true;
    }
    else {
      this.user.authenticated = false;
    }
  },

  getAuthHeader() {
    return {
      'Authorization': 'Token ' + localStorage.getItem('id_token')
    };
  }
}
