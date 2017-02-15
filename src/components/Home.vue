<template>
  <div class="col-sm-6 col-sm-offset-3">
    <h1>List of Accounts</h1>
    <div v-if="accounts">
      <div class="alert alert-danger" v-if="errors">
        <p v-for="er in errors">{{ er }}</p>
      </div>
      <div class="account bg-success" v-for="account in accounts">
        <p>Balance: {{ account.balance }} {{ account.currency_type }}, transactions: {{ account.transactions_count }}
        </p>
        <router-link  class='btn btn-primary' :to="{ name: 'account', params: { AcId: account.id }}">
          Account details
        </router-link>
      </div>
    </div>
    <router-link  class='btn btn-success' :to="{ name: 'new-account'}">
      New Account
    </router-link>
  </div>
</template>

<script>
import {getAccountsMixin} from './mixin'

export default {

  data() {
    return {
      accounts: '',
      errors: ''
    }
  },
  mixins: [getAccountsMixin],
  created() {
    this.getAccounts();
  },
}
</script>
<style>
.account {
  border: 1px solid #ccc;
  padding: 10 px;
  margin: 10px;
}
</style>
