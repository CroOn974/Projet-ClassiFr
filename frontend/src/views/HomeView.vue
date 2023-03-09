<template>
  <NavBar/>
  <div class="container flex flex-row w-screen mt-32 m-auto justify-center">
     <router-link class="flex items-center justify-center h-64 w-96 m-10 bg-gray-800 rounded-lg hover:bg-gray-600" to="/pred">
      <h2 class="text-gray-200 text-lg font-medium">Prédiction</h2>
    </router-link>
    <router-link v-if="isSuperUser" class="flex items-center justify-center h-64 w-96 m-auto bg-gray-800 rounded-lg hover:bg-gray-600" to="/model">
      <h2 class="text-gray-200 text-lg font-medium">Modèles</h2>
    </router-link>
    <router-link v-if="isSuperUser" href="#/monitor" class="flex items-center justify-center h-64 w-96 m-10 bg-gray-800 rounded-lg hover:bg-gray-600" to="/monitor">
      <h2 class="text-gray-200 text-lg font-medium">Monitoring</h2>
    </router-link>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
export default {
  name: 'HomeView',
  components:{
    NavBar,
  },
  data(){
    return{
      isSuperUser : this.$store.state.isSuperUser,
    }
  },
}
</script>