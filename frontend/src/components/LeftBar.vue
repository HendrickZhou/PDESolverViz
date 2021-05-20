<template>
<div id="l-nav-bar">
    <router-link to="/geometry">
        <div class="tab"><b-icon icon="play">Geometry</b-icon></div>
    </router-link>
    <router-link to="/pde">
        <div class="tab"><b-icon icon="play">PDE</b-icon></div>
    </router-link>
    <router-link to="/nn">
        <div class="tab"><b-icon icon="play">NN</b-icon></div>
    </router-link>
    
    
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
    width: 40px;
    background-color: rgb(51, 45, 45);
    display: flex;
    flex-direction: column;;
}

.tab {
    width: 100%;
    height: 50px;
}
</style>>
