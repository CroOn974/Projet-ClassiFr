<template>

      <button type="button" class="bg-gray-800 text-white rounded-md px-3 py-1 mt-10" @click="toggleModal()">Ajouter</button>

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
                        <label for="model_name" class="">Nom</label>
                        <input type="text" name="Nom du modèle" id="model_name" class="rounded-md border border-gray-300">
                        <label for="model_name" class="mt-5">Accuracy</label>
                        <input type="text" name="Nom du modèle" id="model_acc" class="rounded-md border border-gray-300">
                        <label for="model_name" class="mt-5">Info</label>
                        <input type="text" name="Nom du modèle" id="model_info" class="rounded-md border border-gray-300">
                  
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
    methods: {
      createModel() {
        // Code to create a new model goes here
        // You can access the form fields using Vue's data object
        this.closeModal();
      },
      toggleModal(){
        document.getElementById('modal').classList.toggle("hidden")
      }
    },
  };
  </script>