import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/HomePage.vue';
import LoginPage from '@/views/Login.vue';
import DashboardPage from '@/views/Dashboard.vue';
import Signin from '@/views/Signup.vue';
import Registration from '@/views/Registration.vue';
import PersonalInfo from '@/views/PersonalInfo.vue';

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage,
  },
  {
    path: '/dashboard',
    name: 'DashboardPage',
    component: DashboardPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/signin',
    name: 'Signin',
    component: Signin,
  },
  {
    path: '/registration',
    name: 'Registration',
    component: Registration,
    meta: { requiresAuth: true }
  },
  {
    path: '/personal-info',
    name: 'PersonalInfoPage',
    component: PersonalInfo,
    meta: { requiresAuth: true }
  },
  {
    path: '/healthz',
    name: 'LivenessProbe',
    component: {
      template: '<div>OK</div>',
    },
  },
  {
    path: '/readiness',
    name: 'ReadinessProbe',
    component: {
      template: '<div>OK</div>',
    },
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'; 
  if (to.matched.some(record => record.meta.requiresAuth) && !isLoggedIn) {
    next({ name: 'LoginPage' });
  } else {
    next();
  }
});

export default router;
