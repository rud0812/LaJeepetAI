<template>
  <div>
    <div style="width:100%; height:560px">
      <center><img id="logo" :src="require('../assets/big_logo.jpeg')"/></center>
    </div>
    <div class="container mx-auto">
      <h3 style="text-align: center; font-weight: bold">Our Team</h3>
      <div class="row" style="">
        <div class="column my-5 mx-auto" v-for="(m, index) in members" :key="m.id">

          <div class="mx-auto my-12 neoCard text-center">

            <v-avatar size="196" style="margin-top:16px; margin-bottom:16px;">
              <img :src=getImage(index) class="card-img-top" style="border-radius: 10px; object-fit: contain" >
            </v-avatar>

            <v-card-text>
              <h4 style="color: #ffffff; font-weight: bold">{{ m.name }}</h4>

              <div style="color: #397D7D;" class="my-4 text-subtitle-1">{{ m.function }}</div>
              <div style="color: #397D7D;" class="my-4 text-subtitle-1">{{ m.function2 }}</div>

              <v-divider class="mx-4"></v-divider>

              <div style="color: #397D7D;">{{ m.description }}</div>
            </v-card-text>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'team',
  data() {
    return {
      members: [
        {
          'name': 'María Vivó',
          'function': 'Product Owner',
          'function2': 'Beats Model Developer',
          'description': "NLP researcher, passionate about good literature as the one we generate with this amazing model. She loves using most of her creativity to come up with ideas as this crazy project, imagine what's following this one..."
        },
        {
          'name': 'Núria Camí',
          'function': 'Data Engineer',
          'function2': '',
          'description': "She's an M&M, aka mathematician and musician, the perfect combo for a person that is involved in a project as LaJeepetAI. She's the data engineering team chief, the quality of our hits generator relies directly on her work!"
        },
        {
          'name': 'Rodolfo Castro',
          'function': 'Lyrics Model Chief',
          'function2': 'Reggaeton connoisseur',
          'description': "DL and CR7 freak, always tuned about the latest model releases (and the freshest memes), he's the genius that updated our traditional LSTM-based lyrics model to fit the GPT-2 beast. Because of it he deserves the medal of Lyrics Model Developer."
        },
        {
          'name': 'Qijun Jin',
          'function': 'Full Stack Developer',
          'function2': '',
          'description': "Mastering anything that can be done with a computer, he's always ready to give a helping hand to any of the members that has ran out of ideas of is stucked in the track."
        },
        {
          'name': 'Luís Rodríguez',
          'function': 'Chief Beats Model',
          'function2': '',
          'description': "Theoretical fella, he loves quantum hypothesis nearly as much as his reggaeton projects with LaJeepetAI. He's the brain behind the beat model, one of the pilars of this project!"
        },
        {
          'name': 'Lorenzo Vigo',
          'function': 'Full Stack Engineer',
          'function2': 'Heroku Lover (DevOps)',
          'description': "From a family of literates Lorenzo is a concentration of all the programming skills that their family members lack. Luckily for us he is specially fond of full stack programming, in fact he has hand-crafted this stunning platform for LaJeepetAI, unbelivable right?",
        },
        {
          'name': 'Marcel Vilasís',
          'function': 'Researcher',
          'function2': '',
          'description': "The nerve, always in eveything, among others, in 2 masters in parallel and working full time. On the grounds that he's a truly passionate learner soul, he's responsible of the role of researching innovative ways of doing the same, but better. And he nails it!",
        }
      ]
    }
  },

  methods: {
    getImage(index) {
      let i = index % 7
      return 'https://qijunJin.github.io/' + (i + 1) + '.png'
    },
  }
}

</script>

<style scoped>
.row {
  width: 100%
}

.column {
  width: calc(25% - 32px);
  margin-left: 16px;
  margin-right: 16px;
}

.column-whitespace {
  width: calc(12.5%);
}

.container {
  width: 100%;
  margin-left: 90px;
  margin-right: 90px;
  margin-bottom: 90px;
}

.neoCard {
  min-width: 250px;
  border-radius: 20px;
  background-color: #5DC9C9;
  align-items: center;
  color: #444;
  box-shadow: 6px 6px 10px -1px rgba(0, 0, 0, 0.15), -6px -6px 10px -1px rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(0, 0, 0, 0);
  transition: transform 0.5s;
}

.neoCard:hover {
  box-shadow: inset 4px 4px 6px -1px rgba(0, 0, 0, 0.2), -4px -4px 6px -1px rgba(255, 255, 255, 0.7), -0.5px -0.5px 0px rgba(255, 255, 255, 1), 0.5px 0.5px 0px rgba(0, 0, 0, 0.15), 0px 12px 10px -10px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.01);
  transform: translateY(2px);
  color: black;
}

</style>
