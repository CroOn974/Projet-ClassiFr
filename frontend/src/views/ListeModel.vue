<template>
  <div class="home">
    <DataTable/>
  </div>
  <AddModel/>
</template>

<script>
// @ is an alias to /src
import DataTable from '@/components/DataTable.vue';
import AddModel from '@/components/AddModel.vue';

export default {
  name: 'ListeModel',
  components: {
    DataTable,
    AddModel
  }
}
</script>
