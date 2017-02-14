<template>
  <div id="app">
    <p>Some text {{ message }}</p>
    <b-button>
      Reverse Message
    </b-button>
    <b-form-input v-model="message"
                  type="text"
                  placeholder="Enter message"
    ></b-form-input>
    <p v-if="seen">Now you see me</p>
    <ol>
      <todo-item v-for="item in todos" v-bind:todo="item"></todo-item>
    </ol>
    <button v-on:click="updateTodos">Update Todos</button>
  </div>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
      message: 'Hello Vue.js! world',
      seen: true,
      todos: [
        {text: 'some text 1'},
        {text: 'some text 2'},
        {text: 'some text 3'}
      ]
    }
  },
  methods: {
    reverseMessage: function () {
      this.message = this.message.split('').reverse().join('');
    },
    updateTodos: function () {
      this.todos.push({text: this.message});
    }
  },
  components: {
    'todo-item': {
      props: ['todo'],
      template: '<li>{{todo.text}}</li>'
    }
  },
}
</script>

<style src="bootstrap/dist/css/bootstrap.min.css"></style>
<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
