import { createRouter, createWebHistory } from 'vue-router';
import CaseListView from './components/CaseListView.vue';
import CaseDetails from './components/CaseDetails.vue';

const routes = [
  {
    path: '/',
    redirect: '/cases'
  },
  {
    path: '/cases',
    name: 'CaseList',
    component: CaseListView
  },
  {
    path: '/cases/:id',
    name: 'CaseDetails',
    component: CaseDetails,
    props: true
  },
  {
    path: '/cases/new',
    name: 'CaseCreate',
    component: CaseDetails,
    props: false
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
