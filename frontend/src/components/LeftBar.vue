<template>
<div id="l-nav-bar">
    <div class="tab"><b-icon icon="play">File</b-icon></div>
    <div class="tab"><b-icon icon="play">Geometry</b-icon></div>
    <div class="tab"><b-icon icon="play">PDE</b-icon></div>
    <div class="tab"><b-icon icon="play">NN</b-icon></div>
</div>
</template>

<script>
export default {
  name: 'LeftBar',
};
</script>

<style>
#l-nav-bar {
    /* flex:0; */
    width: 25px;
    background-color: rgb(51, 45, 45);
    display: flex;
    flex-direction: column;;
}

.tab {
    width: 100%;
    height: 50px;
}
</style>>
