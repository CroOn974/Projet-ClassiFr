import PredView from '../views/PredView.vue'
import ListeModel from '../views/ListeModel.vue'
import MonitorView from '../views/MonitorView.vue'
import HomeView from '../views/HomeView.vue'

import { createRouter, createWebHashHistory } from 'vue-router'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/pred',
    name: 'Predictions Page',
    component: PredView
  },
  {
    path: '/monitor',
    name: 'Monitoring Page',
    component: MonitorView
  },
  {
    path: '/model',
    name: 'Model Management Page',
    component: ListeModel
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
