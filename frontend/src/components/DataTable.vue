<template>
  <!-- DATATABLE -->
  <div class="flex flex-col w-auto mx-24 mt-10">
    <div class="overflow-x-auto sm:-mx-6 lg:-mx-8">
      <div class="inline-block min-w-full py-2 sm:px-6 lg:px-8">
        <div class="overflow-hidden">
          <table class="min-w-full text-left text-sm font-light">
            <thead class="border-b bg-gray-800 font-medium text-white dark:border-neutral-500 dark:bg-neutral-900">
              <tr>
                <th scope="col" class="px-6 py-4">Modèle</th>
                <th scope="col" class="px-6 py-4">Date</th>
                <th scope="col" class="px-6 py-4">Accuracy</th>
                <th scope="col" class="px-6 py-4">Label</th>
                <th scope="col" class="px-6 py-4">Status</th>
                <th scope="col" class="px-6 py-4"></th>
              </tr>
            </thead>
            <tbody v-for= "model in models" :key = "model.id_model" >
              <tr class="border-b dark:border-neutral-500">
                <td class="whitespace-nowrap px-6 py-4">{{model.name}}</td>
                <td class="whitespace-nowrap px-6 py-4">{{model.jour}}</td>
                <td class="whitespace-nowrap px-6 py-4">{{model.accuracy}}</td>
                <td class="whitespace-nowrap px-6 py-4">{{model.labels}}</td>
                <td class="whitespace-nowrap px-6 py-4">
                  <div>
                    <input
                    class="mt-[0.3rem] mr-2 h-3.5 w-8 appearance-none rounded-[0.4375rem] bg-[rgba(0,0,0,0.25)] outline-none before:pointer-events-none before:absolute before:h-3.5 before:w-3.5 before:rounded-full before:bg-transparent before:content-[''] after:absolute after:z-[2] after:-mt-[0.1875rem] after:h-5 after:w-5 after:rounded-full after:border-none after:bg-white after:shadow-[0_0px_3px_0_rgb(0_0_0_/_7%),_0_2px_2px_0_rgb(0_0_0_/_4%)] after:transition-[background-color_0.2s,transform_0.2s] after:content-[''] checked:bg-primary checked:after:absolute checked:after:z-[2] checked:after:-mt-[3px] checked:after:ml-[1.0625rem] checked:after:h-5 checked:after:w-5 checked:after:rounded-full checked:after:border-none checked:after:bg-primary checked:after:shadow-[0_3px_1px_-2px_rgba(0,0,0,0.2),_0_2px_2px_0_rgba(0,0,0,0.14),_0_1px_5px_0_rgba(0,0,0,0.12)] checked:after:transition-[background-color_0.2s,transform_0.2s] checked:after:content-[''] hover:cursor-pointer focus:before:scale-100 focus:before:opacity-[0.12] focus:before:shadow-[3px_-1px_0px_13px_rgba(0,0,0,0.6)] focus:before:transition-[box-shadow_0.2s,transform_0.2s] focus:after:absolute focus:after:z-[1] focus:after:block focus:after:h-5 focus:after:w-5 focus:after:rounded-full focus:after:content-[''] checked:focus:border-primary checked:focus:bg-primary checked:focus:before:ml-[1.0625rem] checked:focus:before:scale-100 checked:focus:before:shadow-[3px_-1px_0px_13px_#3b71ca] checked:focus:before:transition-[box-shadow_0.2s,transform_0.2s]"
                    type="checkbox"
                    role="switch"
                    :id="model.id_model"
                    checked
                    v-if="model.status"
                    @click="switch_etat"
                    />
                    <input
                    class="mt-[0.3rem] mr-2 h-3.5 w-8 appearance-none rounded-[0.4375rem] bg-[rgba(0,0,0,0.25)] outline-none before:pointer-events-none before:absolute before:h-3.5 before:w-3.5 before:rounded-full before:bg-transparent before:content-[''] after:absolute after:z-[2] after:-mt-[0.1875rem] after:h-5 after:w-5 after:rounded-full after:border-none after:bg-white after:shadow-[0_0px_3px_0_rgb(0_0_0_/_7%),_0_2px_2px_0_rgb(0_0_0_/_4%)] after:transition-[background-color_0.2s,transform_0.2s] after:content-[''] checked:bg-primary checked:after:absolute checked:after:z-[2] checked:after:-mt-[3px] checked:after:ml-[1.0625rem] checked:after:h-5 checked:after:w-5 checked:after:rounded-full checked:after:border-none checked:after:bg-primary checked:after:shadow-[0_3px_1px_-2px_rgba(0,0,0,0.2),_0_2px_2px_0_rgba(0,0,0,0.14),_0_1px_5px_0_rgba(0,0,0,0.12)] checked:after:transition-[background-color_0.2s,transform_0.2s] checked:after:content-[''] hover:cursor-pointer focus:before:scale-100 focus:before:opacity-[0.12] focus:before:shadow-[3px_-1px_0px_13px_rgba(0,0,0,0.6)] focus:before:transition-[box-shadow_0.2s,transform_0.2s] focus:after:absolute focus:after:z-[1] focus:after:block focus:after:h-5 focus:after:w-5 focus:after:rounded-full focus:after:content-[''] checked:focus:border-primary checked:focus:bg-primary checked:focus:before:ml-[1.0625rem] checked:focus:before:scale-100 checked:focus:before:shadow-[3px_-1px_0px_13px_#3b71ca] checked:focus:before:transition-[box-shadow_0.2s,transform_0.2s]"
                    type="checkbox"
                    role="switch"
                    :id="model.id_model"
                    v-else
                    @click="switch_etat"
                    />
                  </div>
                </td>
                <td class="whitespace-nowrap px-6 py-4">
                  <div class="flex items-center space-x-4">
                    
                    <!-- BOUTON UPDATE -->
                    
                    <button 
                    class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" 
                    @click="updateModel(model.id_model)">
                      Edit
                    </button>
                  
                  <!-- BOUTON DELETE -->
                  
                  <button 
                  class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded" 
                  @click="deleteModal(model.id_model)">
                    Delete
                  </button>
                
                <!-- BOUTON AFFICHAGE -->
                
                <button 
                class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded" 
                @click="toggleChildRow(model.id_model)" >
                  Show details
                </button>
            </div>
            
          </td>
          
        </tr>
        <!-- CHILD ROW  -->
        <tr class="child hidden" :id = "model.id_model">
          <td colspan="6">
            <div class="flex items-center justify-center bg-gray-100">
              <div class="px-4 py-2">
                <p class="text-lg font-medium text-gray-900">Details:</p>
                <p class="mt-1 text-sm text-gray-600">{{model.info}}</p>
              </div>
            </div>
          </td>
        </tr>
        
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>



  <div class="hidden flex items-center justify-center" id="UpdateModal">
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
                Modifier un modèle
              </h3>
              <div class="mt-2">
                <p class="text-sm text-gray-500">
                  Veuillez renseigner toutes les informations nécessaire pour l'utilisation du modèle
                </p>
              </div>
            </div>
            <div class="mt-5 sm:mt-6">
              <form class="flex flex-col">
                <label for="model_info" class="my-3">Info</label>
                <input v-model="model.info" type="text" name="Info du modèle" id="model_info" class="rounded-md border border-gray-300">
              </form>
            </div>
          </div>

          <div>
            <button
              type="button"
              class="inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 text-base font-medium text-gray-700 m-3"
              @click="updateInfo()"
            >
              Modifier
            </button>

            <button
              type="button"
              class="inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700"
              @click="updateModel"
            >
              Annuler
            </button>
          </div>

        </div>
      </div>
    </div>
  </div>
  
  <div class="hidden flex items-center justify-center" id="deleteModal">
      <div class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true">
            <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
            <div class="inline-block align-bottom bg-white rounded-lg py-5 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full" role="dialog" aria-modal="true" aria-labelledby="modal-title">
              <div class="space-y-8">
                <div class="mt-3 text-center sm:mt-5">
                  <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                    Voulez-vous supprimer ce modèle ?
                  </h3>
                </div>
                <div class="w-fit mx-auto space-x-3">
                  <button
                    type="button"
                    class="inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 text-base font-medium text-gray-700"
                    @click="deleteModal('')"
                  >
                    Annuler
                  </button>

                  <button
                    type="button"
                    class="inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700"
                    @click="deleteModel(toDelete)"
                  >
                    Supprimer
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
  </div>

</template>
  
<script>


export default {
    name : 'DataTable',
    components :{

    },
    data(){
        return {
            model: {
                'name':'',
                'mod_file':'',
                'accuracy':'',
                'status':'',
                'info':'',
                'toDelete':''
            },
            models: [],
            selectModel: ''
            
        }
    },
    async created(){
        var response = await fetch('http://localhost:8000/api/admin/model');
        this.models = await response.json();
    },

    methods: {
        async getModels(){
            var response = await fetch('http://localhost:8000/api/admin/model');
            this.models = await response.json();
        },
        async switch_etat(event) {
            const modelId = event.target.id;
            
            const model = this.models.find(m => m.id === modelId);

            var response = await fetch('http://localhost:8000/api/admin/model/'+ modelId +'/etatStatus/',{
                method:'post',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(model)
            });


            const updatedModel = await response.json();
            const index = this.models.findIndex(m => m.id === updatedModel.id);
            this.models.splice(index, 1, updatedModel);
        },

        deleteModal(id){

          let delModal = document.getElementById('deleteModal')
          delModal.classList.toggle("hidden")
          this.toDelete = id

        },

        async deleteModel(id){
            
            const model = this.models.find(m => m.id === id);
            
            await fetch('http://localhost:8000/api/admin/model/'+ id,{
                method:'delete',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(model)
            });

            await this.getModels();
            this.toDelete = ''
            let delModal = document.getElementById('deleteModal')
            delModal.classList.toggle("hidden")
        },
        
        toggleChildRow(id) {
            let children = document.getElementsByClassName("child");
            for (let i = 0; i < children.length; i++) {
                if (children[i].id == id) {
                children[i].classList.toggle("hidden");
                break;
                }
            }
        },
        updateModel(id){
            console.log(id)
            this.selectModel = id
            document.getElementById('UpdateModal').classList.toggle("hidden")


        },
        async updateInfo(){
          
            document.getElementById('UpdateModal').classList.toggle("hidden")

            var id = this.selectModel
            
            var response = await fetch('http://localhost:8000/api/admin/model/'+ id +'/updateInfo/',{
                method:'post',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.model)
                
              });
              
              const updatedModel = await response.json();
              const index = this.models.findIndex(m => m.id === updatedModel.id);
              this.models.splice(index, 1, updatedModel);

        },
        
    },

    
};
</script>