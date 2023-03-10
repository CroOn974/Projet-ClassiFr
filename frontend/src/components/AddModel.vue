<template>

      <button type="button" class="bg-gray-800 text-white rounded-md px-3 py-1 mt-2 absolute right-24" @click="toggleModal()">Ajouter</button>

    <div class="hidden flex items-center justify-center" id="modal">
      <div
        class="fixed z-10 inset-0 overflow-y-auto"
        aria-labelledby="modal-title"
        role="dialog"
        aria-modal="true"
      >
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div
            class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"
            aria-hidden="true"
          ></div>
          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
          <div
            class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
            role="dialog"
            aria-modal="true"
            aria-labelledby="modal-title"
          >
            <div>
              <div class="mt-3 text-center sm:mt-5">
                <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                  Ajouter un modèle
                </h3>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    Veuillez renseigner toutes les informations nécessaire pour l'utilisation du modèle
                  </p>
                </div>
              </div>
              <div class="mt-5 sm:mt-6">
                <form class="flex flex-col">
                  <label for="model_name" class="my-3">Nom</label>
                  <input v-model="model.name" type="text" name="Nom du modèle" id="model_name" class="rounded-md border border-gray-300">
                  <div class="relative inline-block mt-6">
                    <div x-data="{show: false}">
                        <button type="button" x-on:click="show = !show" class="inline-flex justify-between w-48 rounded border border-gray-600 px-4 py-2 bg-white text-gray-700 focus:outline-none focus:border-blue-500 focus:shadow-outline-blue active:bg-gray-100 active:text-gray-700 transition duration-150 ease-in-out">
                        <span class="block truncate">Select Labels</span>
                        <svg class="w-4 h-4 fill-current flex-shrink-0 ml-2 -mr-1" viewBox="0 0 20 0">
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M75 200 L225 200 L150 0 Z" />
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M10 1a9 9 0 100 18 9 9 0 000-18zM3.27 10.77a7 7 0 1113.46 0l-1.54 1.16a5 5 0 10-9.38 0l-1.54-1.16z" />
                        </svg>
                        </button>
                        <div x-show="show" x-on:click.away="show = false" class="z-20 mt-2 py-2 w-48 bg-white rounded-md shadow-lg">
                        <div v-for="(label, index) in labels" :key="index" class="py-1">
                            <div class="flex items-center ml-2">
                                <label class="inline-flex items-center">
                                <input type="checkbox" name="type[]" :value="label.libele" class="form-checkbox mr-2" />
                                <span>{{label.libele}}</span>
                            </label>
                            </div>
                        </div>
                        </div>
                    </div>
                  </div>
                </form>
              </div>
            </div>
            
            <div>
              <button
                type="button"
                class="inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 text-base font-medium text-gray-700 m-3"
                @click="createModel"
              >
                Ajouter
              </button>

              <button
                type="button"
                class="inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700"
                @click="toggleModal"
              >
                Annuler
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data(){
        return {
            model: {
                'name':'',
                'mod_file':'aucun',
                'accuracy':0,
                'jour':'',
                'status': false,
                'info':'',
                'labels': [],
            },
            models: [], 
            labels: [], 
        }   
    },
    methods: {    
    /**
     * Récupère la liste de tous les labeles
     * 
     * 
     */
    async getLabel(){
      var response = await fetch('http://localhost:8000/api/label');
      this.labels = await response.json();
    },
    /**
     * Permet de crée un model
     * 
     * 
     */
    async createModel(){
      // récupère les elements selectionné
      const checkboxes = document.querySelectorAll('input[name="type[]"]:checked');
      const selectedLabels = Array.from(checkboxes).map(cb => cb.value);
      this.model.labels = selectedLabels

      var response = await fetch('http://localhost:8000/api/admin/model/',{
          method:'post',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.model)   
      });

      const newModel = await response.json()
      this.models.push(newModel)
      document.getElementById('modal').classList.toggle("hidden")

      await this.getModels();
      },
      toggleModal(){
        document.getElementById('modal').classList.toggle("hidden")
      }
    },
    mounted(){
      this.getLabel()
      console.log(this.labels);
    }
  };
  </script>