<template>
  <div class="container flex flex-row w-screen mt-32 m-auto">
    <a href="#/pred" class="flex items-center justify-center h-64 w-96 m-10 bg-gray-800 rounded-lg hover:bg-gray-600">
      <h2 class="text-gray-200 text-lg font-medium">Prédiction</h2>
    </a>
    <a href="#/model" class="flex items-center justify-center h-64 w-96 m-auto bg-gray-800 rounded-lg hover:bg-gray-600">
      <h2 class="text-gray-200 text-lg font-medium">Modèles</h2>
    </a>
    <a href="#/monitor" class="flex items-center justify-center h-64 w-96 m-10 bg-gray-800 rounded-lg hover:bg-gray-600">
      <h2 class="text-gray-200 text-lg font-medium">Monitoring</h2>
    </a>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
}
</script>