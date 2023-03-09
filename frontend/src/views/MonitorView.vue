<template>
  <NavBar/>
  <MonitorTable/>
</template>

<script>
import MonitorTable from '@/components/MonitorTable.vue';
import NavBar from '@/components/NavBar.vue';
export default {
name: 'MonitorView',
components: {
  MonitorTable,
  NavBar,
}
}
</script>