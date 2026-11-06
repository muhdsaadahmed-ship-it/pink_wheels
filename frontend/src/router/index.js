import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'landing',
    component: () => import('../pages/Landing.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
