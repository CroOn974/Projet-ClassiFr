<template>
    <nav class="bg-gray-800 w-screen h-20">
      <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
        <div class="flex justify-between">
          <div class="flex-shrink-0">
            <a href="/"><img class="  w-16 mt-2" src="../assets/Classifr_logo.png" alt="Workflow logo"></a> 
          </div>
          <div class="">
            <div class="mt-5 text-lg ml-10 flex items-baseline space-x-4">
              <router-link class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium" to="/pred">Prédiction</router-link>
              <router-link v-if="isSuperUser" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium" to="/model">Modèles</router-link>
              <router-link v-if="isSuperUser" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium" to="/monitor">Monitoring</router-link>
              <router-link class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium" to="/logout">Log Out</router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>
</template>
<script>

export default {
  name: 'NavBar',
  data(){
    return{
      isSuperUser : this.$store.state.isSuperUser,
    }
  },
}
</script>