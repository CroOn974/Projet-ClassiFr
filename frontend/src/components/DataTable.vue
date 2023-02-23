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
                        <th scope="col" class="px-6 py-4">Info</th>
                        <th scope="col" class="px-6 py-4">Status</th>
                        <th scope="col" class="px-6 py-4"></th>
                        </tr>
                    </thead>
                    <tbody v-for= "model in models" :key = "model.id_model" >
                        <tr class="border-b dark:border-neutral-500">
                            <td class="whitespace-nowrap px-6 py-4">{{model.name}}</td>
                            <td class="whitespace-nowrap px-6 py-4">{{model.jour}}</td>
                            <td class="whitespace-nowrap px-6 py-4">{{model.accuracy}}</td>
                            <td class="whitespace-nowrap px-6 py-4">{{model.info}}</td>
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
                                
                                <!-- BOUTOUN UPDATE -->

                                <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                                Edit
                                </button>

                                <!-- BOUTOUN DELETE -->

                                <button class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
                                Delete
                                </button>

                                <!-- BOUTOUN AFFICHAGE -->

                                <button class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded" @click="toggleChildRow(model.id_model)" >
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


    

</template>
  
<script>
// import { response } from 'express';

export default {
    name : 'DataTable',
    data(){
        return {
        models: []
        }
    },
    async created(){
        var response = await fetch('http://localhost:8000/api/admin/model');
        this.models = await response.json();
    },
    methods: {
        async switch_etat(event) {
            const modelId = event.target.id;
            
            const model = this.models.find(m => m.id === modelId);
            console.log(model)

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
        toggleChildRow(id) {
            let children = document.getElementsByClassName("child");
            for (let i = 0; i < children.length; i++) {
                if (children[i].id == id) {
                children[i].classList.toggle("hidden");
                break;
                }
            }
            }
    }
};
</script>