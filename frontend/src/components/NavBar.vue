<template>
    <nav class="bg-gray-800 w-screen h-20">
      <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
        <div class="flex justify-between">
          <div class="flex-shrink-0">
            <a href="/"><img class=" absolute top-0 w-16 mt-3" src="../assets/Classifr_logo.png" alt="Workflow logo"></a> 
          </div>
          <div class="hidden md:block">
            <div class="ml-10 flex items-baseline space-x-4">
              <a href="#/pred" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Prédiction</a>
              <a href="#/model" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Modèles</a>
              <a href="#/monitor" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Monitoring</a>
              <a href="#" class="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Logout</a>
            </div>
          </div>
        </div>
      </div>
    </nav>
</template>
<script>
    export default {
        name: 'NavBar',
    }
</script>