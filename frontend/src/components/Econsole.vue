<template>
    <div id="e-console">
        <div id='status-bar'>
            <b-button type='submit' size="sm" v-on:click="Run"><b-icon icon="play"></b-icon></b-button>
            <div class="title">Console</div>
        </div>
        <div class="splitter"></div>
        <div id='console'><span>{{prompt}}</span></div>
    </div>
</template>

<script>
export default {
    name: 'Econsole',
    data() {
        return {
            prompt: '>>>',
        };
    },
    methods: {
        Run() {
            this.$emit('onClickRun');
        },
        newPrompt(newVal) {
            this.prompt = newVal;
        },
    }
}
</script>

<style scoped>
#e-console {
    flex: 3;
}
#status-bar {
    height: 30px;
    display: flex;
    flex-direction: row;
    align-items:space-between;
}
#console {
    color: white;
}
.splitter {
    height: 1px;
    background-color: rgb(51, 45, 45);
}
.title {
    text-align: center;
    color: white;
}
</style>