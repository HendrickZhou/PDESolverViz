import Vue from 'vue';
import Router from 'vue-router';
import Studio from '../components/Studio.vue';
import Editor from '@/components/Editor.vue';
import Pde from '@/components/Pde.vue';
import NN from '@/components/NN.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Studio,
      redirect: 'geometry',
      children: [
        {
          path: 'geometry',
          name: 'Geometry',
          component: Editor,
        },
        {
          path: 'pde',
          name: 'PDE',
          component: Pde,
        },
        {
          path: 'nn',
          name: 'NN',
          component: NN,
        },
      ]
    },
  ],
});
