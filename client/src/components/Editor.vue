<template>
<div id="editor" ref="ed">
    <!-- <div id="e-pad" v-bind:style="{height: epadH + '%'}"></div>
     -->
    <Epad v-bind:style="{height: epadH + '%'}"></Epad>
    <HDrag @onDrag='onDrag'></HDrag>
    <div id="e-console"></div>
</div>
</template>

<script>
import HDrag from '@/components/drag/HDrag.vue';
import Epad from './epad.vue';

export default {
    name: 'Editor',
    mounted() {
        this.getHeight();
    },
    data() {
        return {
            epadH: 70,
        };
    },
    components: {
        HDrag,
        Epad,
    },
    methods: {
        getHeight() {
            this.boxHeight = this.$refs.ed.clientHeight; 
            console.log(this.boxHeight);
        },
        onDrag(deltaH) {
            this.epadH -= 100 * (deltaH / this.boxHeight);
            if (this.epadH > 80) {
                this.epadH = 80;
            }
            if (this.epadH < 40) {
                this.epadH = 40;
            }
        },
    },
};
</script>

<style>
#editor {
    width: 50%;
}

#e-pad {
    color: aqua;
    width: 100%;
}

#e-console {
}
</style>
