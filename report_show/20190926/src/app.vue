<template>
  <div id="root" :style="{'top': current*(-100) + 'vh', 'transform': 'translateY(' + temp_offset + 'px)'}">
    <div class="page">
        <page-1></page-1>
    </div>
    <div class="page">

    </div>
    <div class="page">

    </div>
    <div class="page">

    </div>
  </div>
</template>

<script>
import page1 from './components/page1.vue'

export default {
  data() {
    return {
      current: 0,
      scroll_lock: false,
      touch_start: undefined,
      temp_offset: 0,
    };
  },
  components: {
    "page-1": page1
  },
  mounted() {
    this.addEvent(window, "mousewheel", this.onMouseWheel); // Chrome
    this.addEvent(window, "DOMMouseScroll", this.onMouseWheel); // FireFox
    window.addEventListener("touchstart", this.touchStart, { passive: false });
    window.addEventListener("touchmove", this.touchMove, { passive: false });
    window.addEventListener("touchend", this.touchEnd, { passive: false });
  },
  methods: {
    // 增加事件
    addEvent(obj, xEvent, fn) {
      if (obj.attachEvent) {
        // IE
        obj.attachEvent("on" + xEvent, fn);
      } else {
        obj.addEventListener(xEvent, fn, false);
      }
    },
    go_last_page(){
      this.current = this.current - 1 < 0 ? 0 : this.current - 1;
    },
    go_next_page(){
        this.current = this.current + 1 > 3 ? 3 : this.current + 1;
    },
    onMouseWheel(ev) {
      if (this.scroll_lock) return;
      this.scroll_lock = true;
      var ev = ev || window.event;
      var down = true;
      down = ev.wheelDelta ? ev.wheelDelta < 0 : ev.detail > 0;
      if (down) {
        // console.log("DOWN:" + ev.wheelDelta);
        this.go_next_page()
      } else {
        // console.log("UP:" + ev.wheelDelta);
        this.go_last_page()
      }
      setTimeout(() => {
        this.scroll_lock = false;
      }, 600);
    },

    touchStart(e) {
      e.preventDefault();
      this.touch_start = e.touches[0].clientY;
    },
    touchMove(e) {
      e.preventDefault();
      let y = e.touches[0].clientY;
      this.temp_offset = y-this.touch_start
    },
    touchEnd(e) {
      let offset = this.temp_offset
      if (Math.abs(offset) > 200) {
        if (offset>0)
          this.go_last_page()
        else
          this.go_next_page()
      } 
      this.touch_start = undefined
      this.temp_offset = 0
    
    }
  }
};
</script>

<style lang="scss" scoped>
#root {
  width: 100vw;
  height: 100vh;
  position: fixed;
  // background-color: cadetblue;
  transition: all 0.5s ease-in-out;

  .page {
    width: 100vw;
    height: 100vh;
    overflow: hidden;
  }
}
</style>