<template>
    <div class="v-drag" 
    @mousedown="mouseDown"></div>
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
      this.lastX = event.screenX;
      this.bc = 'rgb(98, 98, 199)';
      this.bh = 5;
    },
    mouseMove(event) {
      console.log('move');
      // agent.$emit('onDrag', this.lastX - event.screenX);
      this.lastX = event.screenX;
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
.v-drag {
    height: 100%;
    width: 3px;
    background-color: rgb(51, 45, 45);
    cursor: s-resize;
    z-index: 10;
}
</style>
