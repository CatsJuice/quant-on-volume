<script>
import interact from "interactjs";
import { throttle } from "lodash";
//   import { events } from '@interactjs/utils';
export default {
  name: "ct-drag-resize",
  funtional: true,
  props: {
    ww: {
      type: Number,
      default: 0
    },
    hh: {
      type: Number,
      default: 0
    },
    x: {
      type: Number,
      default: 0
    },
    y: {
      type: Number,
      default: 0
    },
    resizable: {
      type: Boolean,
      default: true
    },
    moveable: {
      type: Boolean,
      default: true
    }
  },
  mounted() {
    this.$nextTick(() => {
      //   const isHittingParentBound = self => {
      //     if (self.left < 0) {
      //       self.left = 0;
      //       return true;
      //     } else if (self.top < 0) {
      //       self.top = 0;
      //       return true;
      //     } else {
      //       return false;
      //     }
      //   };

      const self = this;
      interact(this.$el)
        .resizable({
          inertia: false,
          edges: {
            top: false,
            left: false,
            bottom: true,
            right: true
          }
        })
        .on(
          "resizemove",
          throttle(({ rect: { width, height } }) => {
            self.height = height;
            self.width = width;
            self.$emit("resizemove", { width, height });
          }, 16)
        )
        .draggable({
          //   inertia: false,
          //   modifiers: [
          //     interact.modifiers.restrictRect({
          //       restriction: "parent",
          //       endOnly: true
          //     })
          //   ],
          //   autoScroll: true,
          //   onmove: self.dragMoveListener
          listeners: {
            start() {
              const path = event.path;
              const classNamesInPath = path.reduce((res, { classList }) => {
                if (!classList) return res;
                return res.concat(classList.value.split(" "));
              }, []);

              const dragCancelClassName = "chart-output-content";
              const dragCancelClassNameIndex = classNamesInPath.indexOf(
                dragCancelClassName
              );

              self.isDragCancel = dragCancelClassNameIndex !== -1;
            },
            move: ({ target, dx, dy }) => {
              if (self.isDragCancel) return;
              //   if (isHittingParentBound(self)) return;
              var x =
                (parseFloat(target.getAttribute("data-x")) || 0) + dx;
              var y =
                (parseFloat(target.getAttribute("data-y")) || 0) + dy;
              self.left += x;
              self.top += y;
            }
          }
        });
    });
  },
  methods: {
    dragMoveListener(event) {
      if (!this.moveable) return;
      var target = event.target;
      // keep the dragged position in the data-x/data-y attributes
      var x = (parseFloat(target.getAttribute("data-x")) || 0) + event.dx;
      var y = (parseFloat(target.getAttribute("data-y")) || 0) + event.dy;

      this.left = x + this.x;
      this.top = y + this.y;

      // update the posiion attributes
      target.setAttribute("data-x", x);
      target.setAttribute("data-y", y);
    }
  },
  data() {
    return {
      top: this.y,
      left: this.x,
      width: this.w,
      height: this.h,
      isDragCancel: false
    };
  },
  render() {
    const { hh, ww, top, left, height, width, resizable } = this;

    const fineHeight = height ? `${height}px` : `${hh}px`,
      fineWidth = width ? `${width}px` : `${ww}px`,
      fineLeft = `${left}px`,
      fineTop = `${top}px`;

    return (
      <div
        class={{ "ct-drag-resize": true }}
        style={{
          width: fineWidth,
          height: fineHeight,
          left: fineLeft,
          top: fineTop,
          position: "absolute"
        }}
      >
        {this.$slots.default}
        {resizable ? <div class="cdr-handle cdr-handle-br"></div> : ""}
      </div>
    );
  }
};
</script>

<style lang="scss" scoped>
.ct-drag-resize {
  position: relative;
  user-select: none;
  touch-action: none;
  padding:3px;

  &:hover {
    cursor: move;
    .cdr-handle {
      transform: scale(1);
    }
  }

  .cdr-handle {
    position: absolute;
    border: 1px solid rgba(0,0,0,.4);
    border-radius: 50%;
    height: 20px;
    width: 20px;
    transform: scale(0.6);
    &:hover {
      transform: scale(1.4);
    }
    &.cdr-handle-tl {
      top: -5px;
      left: -5px;
      cursor: nw-resize;
    }
    &.cdr-handle-tr {
      top: -5px;
      right: -5px;
      cursor: ne-resize;
    }
    &.cdr-handle-bl {
      bottom: -5px;
      left: -5px;
      cursor: sw-resize;
    }
    &.cdr-handle-br {
      bottom: -5px;
      right: -5px;
      cursor: se-resize;
    }
  }
}
</style>
