<template>
  <div id="app">
    <!-- <router-link to="/">Home</router-link> | -->
    <!-- <router-link to="/about">About</router-link> -->
    <!-- <router-view/> -->
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "app",
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
  position: absolute;
  height: 100%;
  width: 100%;
}
</style>
