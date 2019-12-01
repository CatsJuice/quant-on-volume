<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "app",
  components: {}
};
</script>

<style lang="scss">
* {
  margin: 0;
  padding: 0;
}
html {
  width: 100%;
  height: 100%;
  body {
    width: 100%;
    height: 100%;
    // background-color: #f6f6f6;

    #app {
      width: 100%;
      height: 100%;
      background-color: #f6f6f6;
    }
  }
}
</style>
