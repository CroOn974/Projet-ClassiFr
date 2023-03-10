<template>
    <!-- DATATABLE -->
    <div class="flex flex-col w-auto mx-24 mt-10">
      <div class="flex justify-end mb-4">
        <label class="mr-2">Filtrer par id_modele:</label>
        <select v-model="filterBy" @change="filteredPredictions()" class="border rounded-md px-2 py-1">
          <option v-for="model in modelList" :key="model.id_model" :value="model.id_model">{{ model.id_model }}</option>
        </select>
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
              <tbody :id="predict.id_predict" v-for="predict in predictions" :key="predict.id_predict">
                <tr class="border-b dark:border-neutral-500">
                  <td class="whitespace-nowrap px-6 py-4"><img :src="predict.image" alt=""></td>
                  <td class="whitespace-nowrap px-6 py-4">{{ predict.libele }}</td>
                  <td class="whitespace-nowrap px-6 py-4">{{ predict.bonne_pred }}</td>
                  <td class="whitespace-nowrap px-6 py-4 flex center">
                    <textarea 
                      type="textarea" 
                      name="feedback" 
                      id="feedback" 
                      v-model = "predict.feedback"
                      class="border w-8/12 rounded-md h-24 px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent overflow-auto"
                    ></textarea>
                    <div class="m-auto">
                      <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" type="submit" @click="saveFeedback(predict)">Envoyer</button>
                      <br><br>
                      <button class="bg-red-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" type="submit" @click="deletePredict(predict)">Delete</button>
                    </div>
                    
                  </td>
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
        model:{
          id_model:"",
        },
        modelList: [],
        predictions: [],
        filterBy: "0",
      };
    },
    /**
     *  Récupère la liste de prédiction et de modèles
     *  Liste de modèle -> modelList
     *  Liste de prédiction -> predictions
     * 
     */
    async created() {
      var response = await fetch("http://localhost:8000/api/monitor");
      this.predictions = await response.json();

      var models = await fetch("http://localhost:8000/api/admin/model");
      this.modelList = await models.json()
      console.log(this.modelList);
    },
    methods: {
      /**
       * Permet de sauvegardé le feedback sur un prédiction
       * @param {object} predict 
       */
      async saveFeedback(predict) {
        const response = await fetch(`http://localhost:8000/api/monitor/${predict.id_predict}`+'/', {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ feedback: predict.feedback }),
        });
        if (response.ok) {
          console.log('Feedback saved successfully!');
        } else {
          console.error('Error saving feedback:', response.status);
        }
      },
      /**
       * Permet de filtrer le tableau selon le modèle selectionner
       * 
       */
      async filteredPredictions() {
        var id = this.filterBy
        console.log(id);
        var models = await fetch("http://localhost:8000/api/monitor/" + id + "/moniModel/");
        this.predictions = await models.json()


      },
      async deletePredict(predict){

        const response = await fetch(`http://localhost:8000/api/monitor/${predict.id_predict}`+'/',{
                method:'delete',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(predict)
        });
        if (response.ok) {
          console.log('Prediction deleted successfully!');
          // Remove the deleted prediction from the DOM
          const predictionElement = document.getElementById(predict.id_predict);
          predictionElement.remove();
        } else {
          console.error('Error deleting prediction:', response.status);
        }



      }
    },
    computed: {

    },
};
</script>