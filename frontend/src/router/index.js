import PredView from '../views/PredView.vue'
import ListeModel from '../views/ListeModel.vue'
import MonitorView from '../views/MonitorView.vue'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import LogoutView from '@/views/LogoutView.vue'
import store from '@/store'

import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
    meta: { requiresAuth: true }
  },
  {
    path: '/pred',
    name: 'Predictions Page',
    component: PredView,
    meta: { requiresAuth: true }
  },
  {
    path: '/monitor',
    name: 'Monitoring Page',
    component: MonitorView,
    meta: { requiresAuth: true }
  },
  {
    path: '/model',
    name: 'Model Management Page',
    component: ListeModel,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
},
{
    path: '/logout',
    name: 'logout',
    component: LogoutView
},
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isAuthenticated = store.getters.loggedIn;

  if (requiresAuth && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
})


export default router
