<template>
  <NavBar/>
  
  <div v-if="isSuperUser" class="home">
    <AddModel/>
    <DataTable/>
  </div>
  


</template>

<script>
// @ is an alias to /src
import DataTable from '@/components/DataTable.vue';
import AddModel from '@/components/AddModel.vue';
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';

export default {
  name: 'ListeModel',
  components: {
    DataTable,
    AddModel,
    NavBar,
  },
  methods: {
    fetchData() {
      axios.get()
        .then(response => {
          this.dataList = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  data(){
    return{
      isSuperUser : this.$store.state.isSuperUser,
    }
  },
}
</script>
