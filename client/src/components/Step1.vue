<template>
  <v-stepper-content step="1" style="height: 100%">
    <v-toolbar flat color="#5DC9C9">
      <v-toolbar-title color="#000000">
        Your Lyrics
      </v-toolbar-title>
      <v-spacer></v-spacer>
      Number of words:
      <textarea class="form-control mx-2" v-model="lengthVal" rows="1" ref="lengthArea" id="lengthArea"
                placeholder="Length"
                style="width: 75px; height: 36px; background-color:white; resize: none;"></textarea>
      First words:
      <textarea class="form-control mx-2" v-model="seedVal" rows="1" ref="seedArea" id="seedArea"
                placeholder="Custom Seed"
                style="width: 160px;height: 36px;  background-color:white; resize: none;"></textarea>
      <v-btn height="36px" color="#f2ff00" elevation="2" large @click="addLyric" :disabled="get_disabled">
        Generate New Lyrics
      </v-btn>
    </v-toolbar>

    <v-card>
      <v-tabs vertical class="adapt" v-model="activetab">
        <v-tab key="started">
          Get Started
        </v-tab>
        <v-tab v-for="(lyric, id) in lyrics" :key="id">
          {{ lyric.title }}
        </v-tab>
        <v-tab-item style="height: calc(100vh - 455px);">
          <div class="center-text">
            <div style="width:100%">
              <h5><b>Click the button to generate your first lyric.</b></h5>
            </div>
          </div>
        </v-tab-item>
        <v-tab-item v-for="(lyric, id) in lyrics" :key="id" style="height: 100%">
          <div>
            <div class="row">
              <div class="col-10">
                <div class="row">
                  <div class="col-2 mt-2">
                    <b>Title</b>
                  </div>
                  <div class="col-10">
                    <textarea class="form-control" v-model="lyric.title" ref="titleArea" id="titleArea" rows="1"
                              style="resize: none;"></textarea>
                  </div>
                </div>
                <div class="row">
                  <div class="col-2 mt-2">
                    <b>Lyrics</b>
                  </div>
                  <div class="col-10">
                    <textarea class="form-control mt-1" v-model="lyric.content" ref="contentArea" id="contentArea"
                              rows="20"
                              style=" resize: none;"></textarea>
                  </div>
                </div>
              </div>

              <div class="col-2 mt-2">
                <v-card flat class="mr-4">

                  <v-btn @click="saveLyric()" color="#f2ff00" block class="mb-2 mx-1 mt-1">Save</v-btn>
                  <v-btn :href="myUrl" :download="myfilename" @click="downloadLyric(lyric.title, lyric.content)"
                         color="#C0FCFC" block class="my-2 mx-1">
                    Download
                  </v-btn>
                  <v-btn @click="removeLyric(id)" outlined color="red" block class="my-2 mx-1">
                    Remove
                  </v-btn>

                </v-card>
              </div>
            </div>
          </div>
        </v-tab-item>
      </v-tabs>
    </v-card>
    <v-footer color="#5DC9C9">
      <div class="footcol2">
        <v-btn color="#f2ff00" class="button-basic button-nasty-green" @click="$emit('next', 1)"
               style="height: 36px; min-width: 128px;">
          Next
        </v-btn>
      </div>
    </v-footer>
  </v-stepper-content>
</template>


<script>
import {axios} from '@/plugins/axios'

/* eslint-disable */
export default {
  name: 'Step1',
  data() {
    return {
      lyrics: [],
      myUrl: "",
      myfilename: "",
      seedVal: "",
      disabled_val: false,
      lengthVal: 100,
    }
  },

  mounted() {

    if (localStorage.getItem('lyrics')) {
      try {
        this.lyrics = JSON.parse(localStorage.getItem('lyrics'))
      } catch (e) {
        localStorage.removeItem('lyrics')
      }
    }
  },

  computed: {
    get_disabled() {
      return this.disabled_val;
    }
  },

  methods: {
    async addLyric() {
      this.disabled_val = true;
      let content = await axios.get('/new_lyrics', {
        params: {
          'seed': this.seedVal,
          'length': this.lengthVal
        }
      })
      let newLyric = {
        'title': content['data']['title'],
        'content': content['data']['lyrics'],
      }
      this.lyrics.push(newLyric)
      this.saveLyrics()
      this.disabled_val = false;
    },
    removeLyric(x) {
      this.lyrics.splice(x, 1)
      this.saveLyrics()
    },
    saveLyric() {
      this.saveLyrics()
    },
    downloadLyric(title, content) {
      this.myUrl = `data:text/plain;charset=utf-8,${content}`
      this.myfilename = title + '.txt'
    },
    saveLyrics() {
      const parsed = JSON.stringify(this.lyrics)
      localStorage.setItem('lyrics', parsed)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.center-text {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.footcol2 {
  margin-left: auto;
  margin-right: 0;
  width: max-content;
}

.adapt {
  height: calc(100vh - 180px - 216px)
}

.lyric_bloc {
  height: 100%;
}

.column-1 {
  float: left;
  width: calc(100% - 180px)
}

.column-2 {
  float: left;
  width: 180px;
}

</style>
