import Vue from 'vue';
import Router from 'vue-router';
import Dashboard from '../components/Dashboard.vue';
import Post from '../components/Post.vue';
import User from '../components/User.vue';
import EditProfile from '../components/EditProfile.vue';
import LoginProfile from '../components/Login.vue';
import RegisterProfile from '../components/Register.vue';
import SelfTimeline from '../components/SelfTimeline.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard,
    },
    {
      path: '/posts/:post_id',
      name: 'Post',
      component: Post,
    },
    {
      path: '/users/:username',
      name: 'User',
      component: User,
    },
    {
      path: '/profilesettings',
      name: 'EditProfile',
      component: EditProfile,
    },
    {
      path: '/',
      name: 'Login',
      component: LoginProfile,
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterProfile,
    },
    {
      path: '/timeline/:username',
      name: 'SelfTimeline',
      component: SelfTimeline,
    },
  ],
});
