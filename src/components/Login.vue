<template>
  <div class="col-sm-4 col-sm-offset-4">
    <h2>Log In</h2>
    <p>Log in to get information about your accounts</p>
    <div class="form-group">
      <div class="alert alert-danger" v-if="error.username">
        <p v-for="er in error.username">{{ er }}</p>
      </div>
      <input
          type="text"
          class="form-control"
          placeholder="Enter your username"
          v-model="credentials.username"
      >
    </div>
    <div class="form-group">
      <div class="alert alert-danger" v-if="error.password">
        <p v-for="er in error.password">{{ er }}</p>
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
        password: ''
      },
      error: ''
    }
  },

  methods: {

    submit() {

      var credentials = {
        username: this.credentials.username,
        password: this.credentials.password
      }

      auth.login(this, credentials, 'home')
    }
  }

}
</script>
