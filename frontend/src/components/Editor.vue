<template>
<div id="editor" ref="ed">
    <div id="epad-header">GeoScript Editor</div>
    <Epad v-bind:style="{height: epadH + '%'}" ref="formCode"></Epad>
    <HDrag @onDrag='onDrag'></HDrag>
    <Econsole @onClickRun="onClickRun"></Econsole>
</div>
</template>

<script>
import HDrag from '@/components/drag/HDrag.vue';
import Epad from './epad.vue';
import Econsole from './Econsole.vue';

export default {
    name: 'Editor',
    mounted() {
        this.getHeight();
    },
    data() {
        return {
            epadH: 70,
            code: '',
        };
    },
    components: {
        HDrag,
        Epad,
        Econsole,
    },
    methods: {
        onClickRun() {
            this.$refs.formCode.runCode();
        },
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
    display: flex;
    flex-direction: column;
    align-items: stretch;
}

#e-pad {
    color: aqua;
    width: 100%;
}

#epad-header {
    text-align: center;
    color: white;
    height: 25px;
}

</style>
