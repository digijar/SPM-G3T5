import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import HRStaffView from '../views/HRStaffView.vue'
import RegStaffView from '../views/RegStaffView.vue'
import TestDBView from '../views/TestDBView.vue'
import newjoblistView from '../views/newjoblistView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/hrstaff',
      name: 'hrstaff',
      component: HRStaffView
    },
    {
      path: '/regstaff',
      name: 'regstaff',
      component: RegStaffView
    },
    {
      path: '/testDB',
      name: 'testDB',
      component: TestDBView
    },
    {
      path: '/hrstaff/newjoblist',
      name: 'newjoblisting',
      component: newjoblistView
    },
  ]
})

export default router
