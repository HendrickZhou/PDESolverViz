<template>
    <div class="h-drag" 
    @mousedown="mouseDown" 
    v-bind:style="{'background-color': bc, height: bh + 'px'}"></div>
</template>

<script>
export default {
  name: 'HDrag',
  data() {
      return {
          lastY: '',
          bc: 'rgb(51, 45, 45)',
          bh: 2,
      };
  },
  created() {
      document.addEventListener('mouseup', this.mouseUp);
  },
  unmounted() {
      document.removeEventListener('mouseup', this.mouseUp);
  },
  methods: {
    mouseDown(event) {
      document.addEventListener('mousemove', this.mouseMove);
      this.lastY = event.screenY;
      this.bc = 'rgb(98, 98, 199)';
      this.bh = 5;
    },
    mouseMove(event) {
      console.log('move');
      this.$emit('onDrag', this.lastY - event.screenY);
      this.lastY = event.screenY;
    },
    mouseUp() {
      this.lastY = '';
      document.removeEventListener('mousemove', this.mouseMove);
      this.bc = 'rgb(51, 45, 45)';
      this.bh = 2;
    },
  },
};
</script>

<style scoped>
.h-drag {
    height: 1px;
    width: 100%;
    background-color: rgb(51, 45, 45);
    cursor: s-resize;
    z-index: 10;
}
</style>
