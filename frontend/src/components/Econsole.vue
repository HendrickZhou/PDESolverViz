<template>
    <div id="e-console">
        <div id='status-bar'>
            <v-btn elevation="2" icon rounded></v-btn>
        </div>
        <div class="splitter"></div>
        <div id='console'></div>
    </div>
</template>

<script>
export default {
    name: 'Econsole',
}
</script>

<style scoped>
#e-console {
    flex: 3;
}
#status-bar {
    height: 30px;
}
.splitter {
    height: 1px;
    background-color: rgb(51, 45, 45);
}
</style>