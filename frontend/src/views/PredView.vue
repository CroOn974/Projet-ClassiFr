<template>

  <!-- IMAGES FORM  -->
  <div class="w-96 rounded-lg bg-gray-800 text-slate-50 p-8 mx-auto my-8">
    <form @submit.prevent="submitImage">
      <label for="select-option">Sélectionnez une option :</label>
        <select class="text-black my-4 form-select block w-full bg-white border border-gray-400 hover:border-gray-500 px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline" id="select-option" v-model="selectedOption">
          <option disabled value="">Choisissez une option</option>
          <option class="text-black" v-for="(option, index) in options" :key="index" :value="option.id_model">{{ option.name }}</option>
        </select>
      <label for="image">Sélectionner des images :</label>
      <input type="file" id="image" ref="image" accept="image/*" multiple required class="my-4">
      <button type="submit" class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded my-4 mx-24">Soumettre</button>
    </form>
  </div>

  <!-- Affichage images soumises -->
  <div v-if="pret" class="w-10/12 bg-gray-800 m-auto p-12 my-4 rounded-2xl">
      <div class="m-4">
          <h3 class="font-bold text-lg text-slate-50 w-12/12">Récapitulatif des images soumises :</h3>
      </div>
      <div class="flex flex-wrap">
        <div v-for="(item, index) in combinedList" :key="index" class="m-4">
              <div :id="index" class="block w-96 rounded-lg bg-white shadow-lg dark:bg-neutral-700">
                  <a href="#!">
                      <img :src="item.image" alt="Image soumise par l'utilisateur" class="rounded-t-lg h-64 object-cover w-full">
                  </a>
                  <div class="p-6" :id="index">
                      <h5 class="mb-2 text-xl font-medium leading-tight text-neutral-800 dark:text-neutral-50"> 
                        {{ item.prediction.label  }}
                      </h5>
                      <p class="mb-4 text-base text-neutral-600 dark:text-neutral-200">
                        {{ item.prediction.pourcentage }}%
                      </p>
                      <button @click="userFeedback(false,index)" type="button" class="inline-block rounded bg-red-500 px-6 pt-2.5 pb-2 mr-4 text-xs font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-red-600" data-te-ripple-init data-te-ripple-color="light">
                          KO
                      </button>
                      <button @click="userFeedback(true,index)" type="button" class="inline-block rounded bg-green-500 px-6 pt-2.5 pb-2 text-xs font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-green-600" data-te-ripple-init data-te-ripple-color="light">
                          OK
                      </button>
                  </div>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
// Définit un composant Vue appelé "PredView"
export default {
  name:'PredView',
  data() {
    return {
      // Initialise les données du composant avec des tableaux vides et des chaînes de caractères vides
      imageList: [],
      predList: [],
      selectedOption: '',
      options: [],
      pret: false,
      feedback:{
        image : '',
        bonne_pred: false,
        libele : '',
        jour : '',
        id_model : '',
        feedback : '',
      }
    }
  },
  computed: {
    // Combinée des images et de leurs prédictions en utilisant les tableaux imageList et predList
    combinedList() {
      return this.imageList.map((item, index) => {
        return {
          image: item,
          prediction: this.predList[index].prediction
        }
      })
    },
    
  },
  // Exécute une requête asynchrone pour récupérer une liste de modèles à partir de l'API
  async mounted() {
    try {
      const response = await fetch('http://localhost:8000/api/model');
      const data = await response.json();
      // Met à jour les options disponibles avec les modèles récupérés
      this.options = data;
    }catch(error){
      console.log(error);
    }
  },
  methods: {
  // Soumet les images sélectionnées pour prédiction en utilisant l'API
  async submitImage() {
    this.imageList= [];
    this.predList= [];
    this.pret = false
    // Récupère les images sélectionnées dans le formulaire
    const files = this.$refs.image.files;

    // Crée un objet FormData pour envoyer les données du formulaire
    const formData = new FormData();
    for(let i = 0; i < files.length; i++){
      const file = files[i];
      // Ajoute chaque image sélectionnée à l'objet FormData
      formData.append('images', file);

      const reader = new FileReader();
      reader.readAsDataURL(file);
      // Ajoute chaque image sélectionnée à la liste des images pour affichage
      reader.onload = () => {
        this.imageList.push(reader.result);
      };
    }
    // Ajoute l'option sélectionnée à l'objet FormData
    formData.append('selectedOption', this.selectedOption);

    try {
      // Envoie une requête asynchrone pour prédire les images sélectionnées à l'aide de l'API
      const response = await fetch('http://localhost:8000/api/predict', {
        method: 'POST',
        body: formData,
      });
      const json = await response.json();
      // Met à jour la liste des prédictions avec les résultats de l'API
      this.predList = JSON.parse(json);
    }catch(error){
      console.log(error);
    }
    this.pret = true
  },
  // Feedback sur une image
  async userFeedback(avis,index){
    
    let img_pred = this.combinedList[index].image;
    let label = this.combinedList[index].prediction.label
    let model = this.selectedOption;

    this.feedback.image_file = img_pred
    this.feedback.id_model = model
    this.feedback.bonne_pred = avis
    this.feedback.libele = label

    try {
        // Envoie une requête asynchrone pour prédire les images sélectionnées à l'aide de l'API
      await fetch('http://localhost:8000/api/monitor/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.feedback),
        })
    } catch (error) {
      console.log(error);
    }

    // enlève élement 
    const element = document.getElementById(index);
    element.parentNode.removeChild(element);
    
  }
}

}
</script>