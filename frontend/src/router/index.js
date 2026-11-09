import { createRouter, createWebHistory } from 'vue-router'

import PassengerHome from '../pages/passenger/Home.vue'
import PassengerStatus from '../pages/passenger/RideStatus.vue'
import PassengerHistory from '../pages/passenger/RideHistory.vue'
import DriverDashboard from '../pages/driver/DriverDashboard.vue'
import DsaDashboard from '../pages/admin/DsaDashboard.vue'

const routes = [
  {
    path: '/',
    redirect: '/passenger',
  },
  {
    path: '/passenger',
    name: 'passenger-home',
    component: PassengerHome,
  },
  {
    path: '/passenger/status/:id',
    name: 'passenger-status',
    component: PassengerStatus,
  },
  {
    path: '/passenger/history',
    name: 'passenger-history',
    component: PassengerHistory,
  },
  {
    path: '/driver',
    name: 'driver-dashboard',
    component: DriverDashboard,
  },
  {
    path: '/admin/dsa',
    name: 'dsa-dashboard',
    component: DsaDashboard,
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/passenger',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
