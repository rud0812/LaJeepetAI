import { mdiAccount } from '@mdi/js'
<template>
  <v-stepper-content step="3">

    <div>
      <v-toolbar flat color="#5DC9C9">
        <v-toolbar-title color="#000000">
          Song Preview
        </v-toolbar-title>
        <v-spacer></v-spacer>
        Load your recently generated lyrics and beats:
        <v-btn color="#f2ff00" elevation="2" large @click="refresh" style="  height: 36px" class="mx-2">
          Refresh
        </v-btn>
      </v-toolbar>

      <div class="row mt-2">
        <div class="col-6" style="height: 100%; text-align: left">
          Select one of your lyrics:
          <br/>
          <v-select :options="lyrics" label="title" v-model="selectedLyric" attach></v-select>
          <textarea disabled class="form-control lyric_bloc" v-model="get_selected_content" ref="contentArea"
                    id="contentArea"
                    style="height: calc(100vh - 500px); display: block; resize: none; margin-top:12px; margin-bottom:12px"></textarea>
        </div>

        <div class="col-6">
          <v-card flat>
            <div style="width:100%;">

              <div class="mb-5">
                <div style="text-align: left">Select one of your beats:</div>
                <v-select :options="beats" label="title" v-model="selectedBeat" attach></v-select>
                <div style="width:100%; margin-top:48px; margin-bottom:48px">
                  <div style="width: 50%; margin: 0 auto;">
                    <midi-player :src="get_selected_beat" sound-font></midi-player>
                  </div>
                </div>
              </div>


              <div style="text-align: left">
                Generate a Text-To-Speech of your lyrics with a selected voice:
              </div>

              <v-select :options="voices" label="title" v-model="selectedVoice" style="margin-top:8px;"
                        attach></v-select>

              <v-btn color="#f2ff00" elevation="2" large @click="getTTS" :disabled="get_disabled" class="mt-4">
                Generate TTS
              </v-btn>

              <div class="mt-4">
                <audio controls id="tts-player">
                  <source :src='src' type='audio/wav'>
                </audio>
              </div>
            </div>
          </v-card>
        </div>
      </div>
    </div>


    <v-footer color="#5DC9C9">
      <div class="footcol2">
        <v-btn class="button-basic button-nasty-green" @click="$emit('prev', 1)" style="height: 36px">Previous
        </v-btn>
      </div>
    </v-footer>

  </v-stepper-content>
</template>

<script>
import {axios} from '@/plugins/axios'

export default {
  name: 'Step3',
  data() {
    return {
      lyrics: [],
      selectedLyric: null,
      beats: [],
      selectedBeat: null,
      voices: [{name: '2pac-chill', title: '2pac'}, {name: '50-cent', title: '50 Cent'}, {
        name: 'billy-joel',
        title: 'Billy Joel'
      }, {name: 'dababy', title: 'DaBaby'}, {name: 'drake', title: 'Drake'}, {
        name: 'elton-john',
        title: 'Elton John'
      }, {name: 'eminem', title: 'Eminem'}, {name: 'faustao', title: 'Fausto Silva'}, {
        name: 'freddiemercury',
        title: 'Freddie Mercury'
      }, {name: 'justin-bieber', title: 'Justin Bieber'}, {
        name: 'kanye-west-rap',
        title: 'Kanye West'
      }, {name: 'kendrick-lamar', title: 'Kendrick Lamar'}, {
        name: 'lil-uzi-vert',
        title: 'Lil Uzi Vert'
      }, {name: 'marvin-gaye', title: 'Marvin Gaye'}, {name: 'mj', title: 'Michael Jackson'}, {
        name: 'paco-bravo',
        title: 'Paco Bravo'
      }, {name: '6ix9ine', title: 'Tekashi 6ix9ine'}, {name: 'the-weeknd', title: 'The Weeknd'},],
      selectedVoice: null,
      src: "",
      disabled_val: false,
      items: [
        {
          'title': 'song 1',
          'likes': 0,
          'dislikes': 0
        },
      ]

    }
  },
  computed: {
    get_disabled() {
      return this.disabled_val || !this.selectedLyric || !this.selectedVoice;
    },
    get_selected_content() {
      if (this.selectedLyric) {
        return this.selectedLyric['content'];
      } else {
        return "";
      }
    },
    get_selected_beat() {
      if (this.selectedBeat) {
        return this.selectedBeat['content'];
      } else {
        return "";
      }
    }
  },
  methods: {
    async getTTS() {
      this.disabled_val = true;
      let content = await axios.get('/tts', {

        params: {
          'text': this.selectedLyric['content'],
          'voice': this.selectedVoice['name']

        }
      })
      console.log(content)
      this.src = 'wav?src=' + content['data']
      this.disabled_val = false;

      var audio = document.getElementById("tts-player");
      audio.load()
      this.$forceUpdate();
    },
    refresh() {
      if (localStorage.getItem('lyrics')) {
        try {
          this.lyrics = JSON.parse(localStorage.getItem('lyrics'))
        } catch (e) {
          localStorage.removeItem('lyrics')
        }
      }
      if (localStorage.getItem('beats')) {
        try {
          this.beats = JSON.parse(localStorage.getItem('beats'))
        } catch (e) {
          localStorage.removeItem('beats')
        }
      }
      this.$forceUpdate();

    },
    addLike(index) {
      this.items[index].likes += 1
    },
    addDislike(index) {
      this.items[index].dislikes += 1
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.footcol2 {
  margin-left: auto;
  margin-right: 0;
  width: max-content;
}

.column-1 {
  float: left;
  width: 45%
}

.column-2 {
  float: left;
  width: 55%;
  text-align: left;
}

.column-3 {
  float: left;
  width: calc(100% - 175px)
}

.column-4 {
  float: left;
  width: 175px;
  text-align: left;
}
</style>
