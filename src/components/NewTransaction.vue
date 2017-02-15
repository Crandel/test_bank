<template>
  <div class="col-sm-6 col-sm-offset-3">
    <h1>Create new transaction!</h1>
    <div class="">
      <div class="form-group">
        <div class="alert alert-danger" v-if="error.amount">
          <p>{{ error.amount }}</p>
        </div>
        <label for="">Amount
          <input
              type="number"
              class="form-control"
              placeholder="Enter amount"
              v-model="transaction.amount"
          >
        </label>
      </div>
      <div class="form-group">
        <div class="alert alert-danger" v-if="error.source_account">
          <p>{{ error.source_account }}</p>
        </div>
        <label for="">Source Account
          <select class="form-control" v-model="transaction.source_account">
            <option v-for="acc in accounts" :value="acc.id">{{ acc.balance }} {{ acc.currency_type }}</option>
          </select>
        </label>
      </div>
      <div class="form-group">
        <div class="alert alert-danger" v-if="error.destination_account">
          <p>{{ error.destination_account }}</p>
        </div>
        <label for="">Destination Account
          <select class="form-control" v-model="transaction.destination_account">
            <option v-for="acc in accounts" :value="acc.id">{{ acc.balance }} {{ acc.currency_type }}</option>
          </select>
        </label>
      </div>
      <button class="btn btn-primary" @click="submit()">Save</button>
    </div>
  </div>
</template>

<script>
 import auth from '../auth'
 import {getAccountsMixin} from './mixin'

 export default {

   data() {
     return {
       transaction: {
         source_account: '',
         destination_account: '',
         amount: 0
       },
       accounts: '',
       errors: '',
       error: ''
     }
   },
   mixins: [getAccountsMixin],
   created() {
     this.getAccounts();
   },
   methods: {
     submit() {
       var headers = auth.getAuthHeader();
       this.$http.post('transactions/', this.transaction, {headers: headers}).then(
         data => {
           this.$router.push({name: 'home'});
         }, err => {
           this.error = err.body.message;
         }
       )
     }
   }
 }
</script>
