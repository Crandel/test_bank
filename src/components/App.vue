<template>
  <div>
    <nav class="navbar navbar-default">
      <div class="container">
        <ul class="nav navbar-nav">
          <li><router-link :to="{name: 'home'}">Home</router-link></li>
          <li><router-link :to="{name: 'login'}" v-if="!user.authenticated">Login</router-link></li>
          <li><router-link :to="{name: 'signup'}" v-if="!user.authenticated">Sign Up</router-link></li>
          <li><router-link :to="{name: 'transaction'}" v-if="user.authenticated">New Transaction</router-link></li>
          <li><a v-if="user.authenticated" @click="logout">Logout</a></li>
        </ul>
      </div>
    </nav>
    <div class="container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import auth from '../auth'

export default {
  data() {
    return {
      user: auth.user
    }
  },

  methods: {
    logout() {
      auth.logout()
      this.$router.push({name: 'login'})
    }
  }
}
</script>
