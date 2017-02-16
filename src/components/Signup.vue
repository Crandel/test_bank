<template>
  <div class="col-sm-4 col-sm-offset-4">
    <h2>Sign Up</h2>
    <p>Sign up to get information about your accounts.</p>
    <div class="form-group">
      <div class="alert alert-danger" v-if="error.username">
        <p v-for="err in error.username">{{ err }}</p>
      </div>
      <input
          type="text"
          class="form-control"
          placeholder="Enter your username"
          v-model="credentials.username"
      >
    </div>
    <div class="form-group">
      <div class="alert alert-danger" v-if="error.email">
        <p v-for="err in error.email">{{ err }}</p>
      </div>

      <input
          type="email"
          class="form-control"
          placeholder="Enter your email"
          v-model="credentials.email"
      >
    </div>
    <div class="form-group">
      <div class="alert alert-danger" v-if="error.password">
        <p v-for="err in error.password">{{ err }}</p>
      </div>
      <input
          type="password"
          class="form-control"
          placeholder="Enter your password"
          v-model="credentials.password"
      >
    </div>
    <button class="btn btn-primary" @click="submit()">Access</button>
  </div>
</template>

<script>
 import auth from '../auth'

 export default {

   data() {
     return {
       credentials: {
         username: '',
         email: '',
         password: ''
       },
       error: ''
     }
   },

   methods: {

     submit() {

       var credentials = {
         username: this.credentials.username,
         email: this.credentials.email,
         password: this.credentials.password
       }

       auth.signup(this, credentials, 'home')
     }
   }
 }
</script>
