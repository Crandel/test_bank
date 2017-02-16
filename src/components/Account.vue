<template>
  <div class="col-sm-6 col-sm-offset-3">
    <h1>Detail information about account</h1>
    <div class="account bg-success" v-if="account">
      <p>Balance: {{ account.balance }} {{ account.currency_type }}, created: {{account.create_time | nice_date }}
      </p>
      <ol v-if="account.transactions">
        <li v-for="tr in account.transactions">From {{tr.source}} to {{ tr.destination}} -> {{ tr.amount }} {{ tr.create_time | nice_date }}</li>
      </ol>
    </div>
  </div>
</template>

<script>
 import auth from '../auth'

 export default {

   data() {
     return {
       account: '',
       errors: ''
     }
   },
   created() {
     this.getAccount()
   },
   methods: {
     getAccount() {
       var headers = auth.getAuthHeader();
       var accountId = this.$route.params.AcId
       this.$http.get('accounts/' + accountId, {headers: headers}).then(
         data => {
           this.account = data.body.data;
         }, err => {
           this.errors = err.body.message;
         }
       )
     }
   },
   filters: {
     nice_date(value) {
       var date = new Date(value),
           options = {hour12: false};
       return date.toLocaleDateString('lv-LV', options)
     }
   }
 }
</script>
