import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import KnowledgeBase from './views/KnowledgeBase.vue'
import './style.css'

// Router setup
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/knowledge'
    },
    {
      path: '/knowledge/:agentId?',
      name: 'KnowledgeBase',
      component: KnowledgeBase
    }
  ]
})

const app = createApp(App)
app.use(router)
app.mount('#app')
