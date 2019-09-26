<template>
  <div
    id="root"
    :style="{'top': current*(-100) + 'vh', 'transform': 'translateY(' + temp_offset + 'px)', 'transition': 'all '+switch_time/1000+'s ease-in-out'}"
  >
    <div class="page">
      <!-- <page-start></page-start> -->
      <div id="start-page-btn" @click="current=1">
        <span>Starts Here</span>
        <span></span>
      </div>
    </div>
    <div class="page">
      <page-1 :current="current==1?true:false"></page-1>
    </div>
    <div class="page">
      <page-2 :current="current==2?true:false"></page-2>
    </div>
    <div class="page">
      <!-- <page-1 :current="current==3?true:false"></page-1> -->
    </div>
    <div class="page">
      <!-- <page-1 :current="current==4?true:false"></page-1> -->
    </div>
  </div>
</template>

<script>
// import pageStart from './components/pageStart.vue'
import page1 from "./components/page1.vue";
import page2 from "./components/page2.vue";

export default {
  data() {
    return {
      current: 0,
      scroll_lock: false,
      touch_start: undefined,
      temp_offset: 0,

      switch_time: 700
    };
  },
  components: {
    "page-1": page1,
    "page-2": page2
    // "page-start": pageStart
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
    go_last_page() {
      this.current = this.current - 1 < 0 ? 0 : this.current - 1;
    },
    go_next_page() {
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
        this.go_next_page();
      } else {
        // console.log("UP:" + ev.wheelDelta);
        this.go_last_page();
      }
      setTimeout(() => {
        this.scroll_lock = false;
      }, this.switch_time);
    },

    touchStart(e) {
      e.preventDefault();
      this.touch_start = e.touches[0].clientY;
    },
    touchMove(e) {
      e.preventDefault();
      let y = e.touches[0].clientY;
      this.temp_offset = y - this.touch_start;
    },
    touchEnd(e) {
      let offset = this.temp_offset;
      if (Math.abs(offset) > 200) {
        if (offset > 0) this.go_last_page();
        else this.go_next_page();
      }
      this.touch_start = undefined;
      this.temp_offset = 0;
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

  .page {
    width: 100vw;
    height: 100vh;
    overflow: hidden;
  }
}

#start-page-btn {
  transition: all 0.2s ease-in-out;
  margin-left: 50vw;
  margin-top: 50vh;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 300px;
  height: 60px;
  border-radius: 50px;
  background-image: linear-gradient(to right, #6a11cb 0%, #2575fc 100%);
  color: #fff;
  font-size: 2rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0px 10px 40px rgba(37, 117, 252, 0.5);

  
  &>span:nth-child(1) {
    margin-left: 20px;
  }
  &>span:nth-child(2) {
    background-image: url(./imgs/down_arrow.png);
    display: inline-block;
    width: 60px;
    height: 60px;
    background-size: 50%;
    background-position: center;
    background-repeat: no-repeat;
  }
  &:hover {
    box-shadow: 0px 10px 40px rgba(37, 117, 252, 0.7);
    letter-spacing: 2px; 
  }
}
</style>