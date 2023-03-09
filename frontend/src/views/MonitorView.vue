<template>
  <NavBar/>
  <MonitorTable v-if="isSuperUser"/>
</template>

<script>
import MonitorTable from '@/components/MonitorTable.vue';
import NavBar from '@/components/NavBar.vue';
export default {
name: 'MonitorView',
components: {
  MonitorTable,
  NavBar,
},
  data(){
    return{
      isSuperUser : this.$store.state.isSuperUser,
    }
  },
}
</script>