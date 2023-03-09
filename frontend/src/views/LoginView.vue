<template>
  <div class="min-h-screen flex bg-gray-800 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full mx-auto">

      <img class="w-72 mx-auto" src="../assets/Classifr_logo.png" alt="Workflow logo">

      <div class="bg-gray-50 py-4 pb-12 rounded-lg items-center h-3/5 pt-16" :class="{'rotate-card': showSignup, 'invert-card': !showSignup}">

        <h1 class="mt-6 text-center text-3xl font-extrabold text-gray-900" :class="{'rotate-card': showSignup, 'invert-card': !showSignup}">
          {{ showSignup ? 'Inscription' : 'Connexion' }}
        </h1>

        <p v-if="incorrectAuth" class="text-center text-red-500" :class="{'rotate-card': showSignup, 'invert-card': !showSignup}">Identifiants incorrects - veuillez réessayer</p>


        <form v-on:submit.prevent=authentication class="mt-8 space-y-6 flex flex-col" :class="{'rotate-card': showSignup, 'invert-card': !showSignup}">
          <div class="mx-auto">
            <input type="text" name="username" id="user" v-model="username" class="rounded-md shadow-sm -space-y-px p-2 bg-gray-200" placeholder="Nom d'utilisateur">
          </div>
          <div class="mx-auto">
            <input type="password" name="password" id="pass" v-model="password" class="rounded-md shadow-sm -space-y-px p-2 bg-gray-200" placeholder="Mot de passe">
          </div>
          
          <div v-if="showSignup" class="mx-auto">
            <input type="password" class="rounded-md shadow-sm -space-y-px p-2 bg-gray-200" id="confirmPassword" v-model="confirmPassword" placeholder="Confirm Password">
          </div>

          <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded w-6/12 mx-auto">
            {{ showSignup ? 'S\'inscrire' : 'Se connecter' }}
          </button>
        </form>
        <div class="mt-4 text-center">
          <button class="text-blue-500 hover:underline" @click="showSignup = !showSignup" :class="{'rotate-card': showSignup, 'invert-card': !showSignup}">
            {{ showSignup ? 'Déjà inscrit ? Connectez-vous' : 'Pas encore inscrit ? Inscrivez-vous' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
  
  <script>
    export default {
      name: 'LoginView',
      data () {
        return {
          username: '',
          password: '',
          incorrectAuth: false,
          confirmPassword: '',
          showSignup: false
        }
      },
      methods: {
        authentication() { 
          if (!this.showSignup) {
            this.$store.dispatch('userLogin', {
            username: this.username,
            password: this.password
          })
          .then(() => {
            this.$router.push({ name: 'Home' })
          })
          .catch(err => {
            console.log(err)
            this.incorrectAuth = true
          })
          }else{
            // Check if the passwords match
          if (this.password !== this.confirmPassword) {
            alert("Passwords don't match!")
            return
          }
          console.log(this.username)
          console.log(this.confirmPassword)
          
          // Call the API to sign up the user
          this.$store.dispatch('userSignup', {
            username: this.username,
            password: this.password
          })
          .then(() => {
            // Handle successful sign up
            this.$router.push({ name: 'Home' })

          })
          .catch(err => {
            // Handle sign up error
            console.log(err);
          })
          }
          
        },
      }
    }
  </script>

<style>
.rotate-card {
  transition: transform 0.3s ease-out;
  transform: rotateY(180deg);
}
.invert-card {
  transition: transform 0.3s ease-out;
  transform: rotateY(0deg);
}
</style>