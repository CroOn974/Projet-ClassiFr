<template>
    <!-- DATATABLE -->
    <div class="flex flex-col w-auto mx-24 mt-10">
      <div class="flex justify-end mb-4">
        <label class="mr-2">Filtrer par id_modele:</label>
        <input type="text" v-model="filterBy" class="border rounded-md px-2 py-1">
      </div>
      <div class="overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="inline-block min-w-full py-2 sm:px-6 lg:px-8">
          <div class="overflow-hidden">
            <table class="min-w-full text-left text-sm font-light">
              <thead class="border-b bg-gray-800 font-medium text-white dark:border-neutral-500 dark:bg-neutral-900">
                <tr>
                  <th scope="col" class="px-6 py-4">Image</th>
                  <th scope="col" class="px-6 py-4">Label</th>
                  <th scope="col" class="px-6 py-4">Prediction</th>
                  <th scope="col" class="px-6 py-4">FeedBack</th>
                </tr>
              </thead>
              <tbody v-for="predict in predictions" :key="predict.id_predict">
                <tr class="border-b dark:border-neutral-500">
                  <td class="whitespace-nowrap px-6 py-4"><img :src="predict.image" alt=""></td>
                  <td class="whitespace-nowrap px-6 py-4">{{ predict.libele }}</td>
                  <td class="whitespace-nowrap px-6 py-4">{{ predict.bonne_pred }}</td>
                  <td class="whitespace-nowrap px-6 py-4">{{ predict.feedback }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "MonitorTable",
    data() {
      return {
        predict: {
          image: "",
          libele: "",
          bonne_pred: "",
          feedback: "",
          id_modele: "",
        },
        predictions: [],
        filterBy: "",
      };
    },
    async created() {
      var response = await fetch("http://localhost:8000/api/monitor");
      this.predictions = await response.json();
    },
    computed: {
      filteredPredictions() {
        return this.predictions.filter(
          (predict) =>
            predict.id_modele.toString().indexOf(this.filterBy.toLowerCase()) !== -1
        );
      },
    },
  };
  </script>