<template>

  <!-- IMAGES FORM  -->
  <div class="w-96 rounded-lg bg-gray-800 text-slate-50 p-8 mx-auto my-8">
    <form @submit.prevent="submitImage">
      <label for="image">Sélectionner des images :</label>
      <input type="file" id="image" ref="image" accept="image/*" multiple required class="my-4">
      <button type="submit" class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded my-4 mx-24">Soumettre</button>
    </form>
  </div>

  <!-- Affichage images soumises -->
  <div v-if="imageDataList.length > 0" class="w-10/12 bg-gray-800 m-auto p-12 my-4 rounded-2xl">
      <div class="m-4">
          <h3 class="font-bold text-lg text-slate-50 w-12/12">Récapitulatif des images soumises :</h3>
      </div>
      <div class="flex flex-wrap">
          <div v-for="(imageData, index) in imageDataList" :key="index" class="m-4">
              <div class="block w-96 rounded-lg bg-white shadow-lg dark:bg-neutral-700">
                  <a href="#!">
                      <img :src="imageData" alt="Image soumise par l'utilisateur" class="rounded-t-lg h-64 object-cover w-full">
                  </a>
                  <div class="p-6">
                      <h5 class="mb-2 text-xl font-medium leading-tight text-neutral-800 dark:text-neutral-50"> 
                          Label
                      </h5>
                      <p class="mb-4 text-base text-neutral-600 dark:text-neutral-200">
                          Taux de confiance
                      </p>
                      <button type="button" class="inline-block rounded bg-red-500 px-6 pt-2.5 pb-2 mr-4 text-xs font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-red-600" data-te-ripple-init data-te-ripple-color="light">
                          KO
                      </button>
                      <button type="button" class="inline-block rounded bg-green-500 px-6 pt-2.5 pb-2 text-xs font-medium uppercase leading-normal text-white shadow-[0_4px_9px_-4px_#3b71ca] transition duration-150 ease-in-out hover:bg-green-600" data-te-ripple-init data-te-ripple-color="light">
                          OK
                      </button>
                  </div>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
export default {
  name:'PredView',
  data() {
    return {
      imageDataList: []
    }
  },
  methods: {
    async submitImage() {
      const files = this.$refs.image.files;

      for (let i = 0; i < files.length; i++) {
        const file = files[i];

        // Vérifier si le fichier est une image
        if (!file.type.startsWith("image/")) {
          console.error(`Le fichier ${file.name} n'est pas une image.`);
          continue;
        }

        try {
          // Lire le contenu du fichier et le stocker dans la variable imageDataList
          const reader = new FileReader();
          reader.readAsDataURL(file);
          reader.onload = () => {
            this.imageDataList.push(reader.result);
          };
        } catch (error) {
          console.error(error);
        }
      }
    }
  }
}
</script>