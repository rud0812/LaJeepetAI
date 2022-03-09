<template>
    <v-stepper v-model="step" class="rounded-0 adapt" style="height: 100%">
        <v-stepper-header>
            <v-stepper-step :complete="step > 1" step="1" @click="step=1">Lyrics</v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step :complete="step > 2" step="2" @click="step=2">Beats</v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step :complete="step > 3" step="3" @click="step=3">Final Result</v-stepper-step>
        </v-stepper-header>
        <v-stepper-items style="height: 100%">
            <Component v-for="i in 3" :key="i"
                :ref="'formActivity'+i"
                v-bind:is="'Step' + i"
                @prev="step--"
                @next="step++"
                style="height: 100%"
            />
       </v-stepper-items>
    </v-stepper>
</template>

<script>
import Step1 from './Step1.vue'
import Step2 from './Step2.vue'
import Step3 from './Step3.vue'

export default {
    name: 'StepContainer',
    components: {
        Step1,
        Step2,
        Step3
    },
    data: function() {
        return {
            step: 1
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.adapt {
    height: 100%;
}
</style>
