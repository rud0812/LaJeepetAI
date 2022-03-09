import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import {BootstrapVue, IconsPlugin} from 'bootstrap-vue'
import Vuetify from 'vuetify'
import VueAxios from './plugins/axios'

//import VueAudio from 'vue-audio-better'
import titleMixin from './mixins/titleMixin'
import vSelect from "vue-select";
import VueAudio from 'vue-audio';


import "vuetify/dist/vuetify.min.css";
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import "vue-select/dist/vue-select.css";

Vue.use(VueRouter)
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(Vuetify)
Vue.use(VueAxios)
Vue.use(VueAudio)
Vue.mixin(titleMixin)
Vue.component("v-select", vSelect);
Vue.component("vue-audio", VueAudio)

export default new Vuetify({
    icons: {
        iconfont: 'fa', // 'mdi' || 'mdiSvg' || 'md' || 'fa' || 'fa4' || 'faSvg'
    },
})

Vue.config.productionTip = false

const routes = [
    {path: '/', component: App},
]

const router = new VueRouter({
    routes
})

new Vue({
    el: "#app",
    router,
    vuetify: new Vuetify(),
    render: h => h(App),
}).$mount('#app')
