import Vue from 'vue';
import App from './components/App.vue';
import Home from './components/Home.vue';
import NewTransaction from './components/NewTransaction.vue';
import Account from './components/Account.vue';
import NewAccount from './components/NewAccount.vue';
import Signup from './components/Signup.vue';
import Login from './components/Login.vue';
import VueRouter from 'vue-router';
import VueResource from 'vue-resource';

import auth from './auth';

Vue.use(VueResource);
Vue.use(VueRouter);

auth.checkAuth();

Vue.http.options.root = '/api';
Vue.http.headers.common['X-Requested-With'] = 'XMLHttpRequest';

const routes = [
  {
    path: '/', component: Home, name: 'home', beforeEnter: (to, from, next) => {
      if(auth.user.authenticated){
        next();
      }else{
        to = {name:'login'};
        next(to);
      }
    }
  },{
    path: '/transaction', component: NewTransaction,
    name: 'transaction', beforeEnter: (to, from, next) => {
      if(auth.user.authenticated){
        next();
      }else{
        to = {name:'login'};
        next(to);
      }
    }
  },{
    path: '/account/:AcId', component: Account,
    name: 'account', beforeEnter: (to, from, next) => {
      if(auth.user.authenticated){
        next();
      }else{
        to = {name:'login'};
        next(to);
      }
    }
  },{
    path: '/account/new', component: NewAccount,
    name: 'new-account', beforeEnter: (to, from, next) => {
      if(auth.user.authenticated){
        next();
      }else{
        to = {name:'login'};
        next(to);
      }
    }
  },{
    path: '/login', component: Login, name: 'login'
  },{
    path: '/signup', component: Signup, name: 'signup'
  },
  {
    path: '*', redirect: '/'
  }
];

export var router = new VueRouter({
  routes
});

new Vue({
  el: '#app',
  data: {
    token: 'token'
  },
  router,
  render: h => h(App)
});
