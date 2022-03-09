<template>
  <div>
    <div>
      <nav class="navbar navbar-dark bg-dark navbar-expand-md py-5">
        <img id="logo" class="logo" :src="require('./assets/logo.png')" height="100"/>
      </nav>
    </div>
    <div id="app">
      <v-app>
        <div align="center" class="step">
          <div style="grid-area: 1 / 1;">
            <StepContainer/>
          </div>
          <div style="grid-area: 1 / 1; z-index: 10; height: 100%; width: 100%; position: relative; background-color: #FFFFFF" v-show="loading_val">
            <div class="center-hints">
              <img :src="require('./assets/loading.gif')" height="44"/>
              <div id="load_hint" style="margin-left: 10px; margin-top:10px; margin-bottom:10px" v-html="message"></div>
            </div>
          </div>
        </div>
        <div class="about">
          <About/>
          <Team/>
        </div>
      </v-app>
    </div>
  </div>
</template>

<script>
import { axios } from '@/plugins/axios'

import StepContainer from './components/StepContainer.vue'
import About from './components/About.vue'
import Team from './components/Team.vue'

export default {
  name: 'App',
  title: 'LaJeepetAI',
  data() {
    return {
      loading: true,
      message: "Initializing app..."
    }
  },
  components: {
    StepContainer,
    About,
    Team
  },
  async created() {
    axios.defaults.timeout = 180000;
    await axios.get("/snoop")

    await new Promise(resolve => setTimeout(resolve, 1500));
    this.message = "Loading lyrics model..."

    for (var i = 0; i < 1; i++) {
      await axios.get("/lyrics_weights", {
        params: {
          portion: i
        },
        timeout: 180000
      });
    }

    await new Promise(resolve => setTimeout(resolve, 1000));
    this.message = "Loading beats model..."

    await new Promise(resolve => setTimeout(resolve, 1500));
    this.loading = false;
  },
  computed: {
    loading_val() {
      return this.loading;
    }
  }
}
</script>

<style>
.about {
    background-color: #FFFFFF;
    margin-top: 48px;
    width: 100%;
}

.center-hints {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100% - 180px);
  width: 100%
}

.navbar {
    position: relative;
    height: 180px;
}

.logo {
    position: absolute;
    left: 50%;
    margin-left: -218px !important;  /* 50% of your logo width */
    display: block;
}

.step {
    display: grid;
    height: calc(100% - 180px);
    margin: 0 auto;
    width: 70%;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #212529;
}
</style>
