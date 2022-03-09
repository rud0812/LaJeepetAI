<template>

  <v-stepper-content step="2" style="height: 100%">
    <v-toolbar flat color="#5DC9C9">
      <v-toolbar-title color="#000000">
        Your Beats
      </v-toolbar-title>
      <v-spacer></v-spacer>
      Number of notes:
      <textarea class="form-control mx-2" v-model="lengthVal" rows="1" ref="lengthArea" id="lengthArea"
                placeholder="Length"
                style="margin-left: 12px; width: 75px; background-color:white; resize: none; height: 36px"></textarea>
      <v-btn color="#f2ff00" elevation="2" large @click="addBeat" :disabled="get_disabled" style="height: 36px">
        Generate New Beat
      </v-btn>
    </v-toolbar>
    <v-card>
      <v-tabs vertical class="adapt">
        <v-tab key="started">
          Get Started
        </v-tab>
        <v-tab v-for="(beat, id) in beats" :key="id">
          {{ beat.title }}
        </v-tab>
        <v-tab-item style="height: calc(100vh - 455px);">
          <div class="center-text">
            <div style="width:100%">
              <h5><b>Click the button to generate your first beat.</b></h5>
            </div>
          </div>
        </v-tab-item>
        <v-tab-item v-for="(beat, id) in beats" :key="id" style="height: 100%">
          <div>
            <div class="row">
              <div class="col-10">
                <div class="row">
                  <div class="col-2 mt-2">
                    <b>Title</b>
                  </div>
                  <div class="col-10">
                    <textarea class="form-control" v-model="beat.title" ref="titleArea" id="titleArea" rows="1"
                              style="resize: none;"></textarea>
                  </div>
                </div>
                <div class="row">
                  <div class="col-2 mt-2" >
                    <b>Beats</b>
                  </div>
                  <div class="col-10">
                    <midi-player :src="beat.content" sound-font></midi-player>
                  </div>
                </div>
              </div>
              <div class="col-2 mt-2">
                <v-card flat>
                  <div style="padding: 5px;">
                    <v-btn @click="saveBeat()" color="#f2ff00" block>
                      Save
                    </v-btn>
                  </div>
                  <div style="padding: 5px;">
                    <v-btn :href="myUrl" :download="myfilename" @click="downloadBeat(beat.title, beat.content)"
                           color="#C0FCFC" block>
                      Download
                    </v-btn>
                  </div>
                  <div style="padding: 5px;">
                    <v-btn @click="removeBeat(id)" outlined color="red" block>
                      Remove
                    </v-btn>
                  </div>
                </v-card>
              </div>
            </div>
          </div>
        </v-tab-item>
      </v-tabs>
    </v-card>
    <v-footer color="#5DC9C9">
      <div class="footcol2">
        <v-btn class="button-basic button-nasty-green" @click="$emit('prev', 1)"
               style="margin-right: 8px; height: 36px; min-width: 128px;">Previous
        </v-btn>
        <v-btn color="#f2ff00" class="button-basic button-nasty-green" @click="$emit('next', 1)" style="height: 36px; min-width: 128px;">
          Next
        </v-btn>
      </div>
    </v-footer>
  </v-stepper-content>
</template>

<script>
import {axios} from '@/plugins/axios'

export default {
  name: 'Step2',
  data() {
    return {
      beats: [],
      myUrl: "",
      myfilename: "",
      player: "",
      disabled_val: false,
      lengthVal: 1000,
    }
  },

  mounted() {
    if (localStorage.getItem('beats')) {
      try {
        this.beats = JSON.parse(localStorage.getItem('beats'))
      } catch (e) {
        localStorage.removeItem('beats')
      }
    }
  },

  computed: {
    get_disabled() {
      return this.disabled_val;
    }
  },

  methods: {
    async addBeat() {
      this.disabled_val = true;
      let content = await axios.get('/new_beat', {

        params: {
          'length': this.lengthVal

        }
      })
      let newBeat = {
        'title': 'Beat ' + this.beats.length,
        'content': '/midi?src=' + content['data'],
      }
      this.beats.push(newBeat)
      this.saveBeats()
      this.disabled_val = false;
    },
    removeBeat(x) {
      this.beats.splice(x, 1)
      this.saveBeats()
    },
    saveBeat() {
      this.saveBeats()
    },
    downloadBeat(title, content) {
      this.myUrl = content
      this.myfilename = title + '.mid'
    },
    saveBeats() {
      const parsed = JSON.stringify(this.beats)
      localStorage.setItem('beats', parsed)
    },
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

.beat_bloc {
  height: 100%;
}

.column-1 {
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  float: left;
  width: calc(100% - 180px)
}

.column-2 {
  float: left;
  width: 180px;
}
</style>
