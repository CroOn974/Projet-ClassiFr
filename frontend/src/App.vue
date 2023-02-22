<template>
  <div id="app">

  </div>
</template>

<script>


export default {
  name: 'App',
  data(){
    return {
      models: []
    }
  },
  async created(){
    var response = await fetch('http://localhost:8000/api/admin/model');
    this.models = await response.json();
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
