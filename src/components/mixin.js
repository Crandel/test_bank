import auth from '../auth';

export var getAccountsMixin = {
  methods: {
    getAccounts() {
      var headers = auth.getAuthHeader();
      this.$http.get('accounts/list', {headers: headers}).then(
        response => {
          this.accounts = response.body.data;
        }, err => {
          this.errors = err.body.message;
        }
      );
    }
  }
}
