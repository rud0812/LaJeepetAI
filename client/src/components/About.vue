<template>
  <div class="container mx-auto">
    <h3 style="text-align: center; font-weight: bold">About LaJeepetAI</h3>
    <br>
    <div class="mx-auto" style="width: 80%;">
      {{ about }}
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      about: 'LaJeepetAI is conformed by an ensemble of quite diverse scientists that share their passion in AI applications and music (not reggaeton specially, this decision was made just for fun\'s sake). We have decided to team up to work in an utterly challenging project: music generation. This platform is the first attempt to the final product, a music generator that can be used by a user to generate lyrics, beat and voice for a brand-new reggaeton song, with the possibility to tune a number of parameters to customize the final song. Therefore, this platform is a powerful tool for music developers, aka dj\'s, and also singers that need some inspiration for their next hit. Creating a breathtaking reaggaeton song had never been this easy, don\'t wait and click!'
    }
  }
}

</script>

<style scoped>
.container {
  display: table;
  width: 100%;
  margin-top: 90px;
  margin-bottom: 90px;
  margin-left: 90px;
  margin-right: 90px;
}
</style>
