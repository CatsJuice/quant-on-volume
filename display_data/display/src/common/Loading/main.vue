<template>
  <transition name="el-message-fade">
    <div
      :class="[
        'el-message',
        type && !iconClass ? `el-message--${ type }` : '',
        center ? 'is-center' : '',
        showClose ? 'is-closable' : '',
        customClass
      ]"
      v-show="visible"
      @mouseenter="clearTimer"
      @mouseleave="startTimer"
      role="alert">
        <!--自定义图标存在时显示-->
      <i :class="iconClass" v-if="iconClass"></i>
        <!--自定义图标不存在时根据type显示图标-->
      <i :class="typeClass" v-else></i>
      <slot>
          <!--用户设置的message的参数为字符串时，显示字符串-->
        <p v-if="!dangerouslyUseHTMLString" class="el-message__content">{{ message }}</p>
        <!--用户设置的message的参数为VNode时，在此处显示-->
        <p v-else v-html="message" class="el-message__content"></p>
      </slot>
        <!--当用户设置的关闭按钮显示为true时，显示关闭图标-->
      <i v-if="showClose" class="el-message__closeBtn el-icon-close" @click="close"></i>
    </div>
  </transition>
</template>

<script type="text/babel">
  const typeMap = {
    success: 'success',
    info: 'info',
    warning: 'warning',
    error: 'error'
  };

  export default {
    data() {
      return {
        visible: false,
        message: '', //消息文字
        duration: 3000, //显示时间, 毫秒。设为 0 则不会自动关闭
        type: 'info',
        iconClass: '', //自定义图标的类名，会覆盖 type
        customClass: '', //自定义类名
        onClose: null,
        showClose: false, //是否显示关闭按钮
        closed: false, //用来判断消息提示弹窗是否关闭
        timer: null,
        dangerouslyUseHTMLString: false, //是否将 message 属性作为 HTML 片段处理
        center: false
      };
    },

    computed: {
      // 根据type返回对应的图标类名
      typeClass() {
        return this.type && !this.iconClass
          ? `el-message__icon el-icon-${ typeMap[this.type] }`
          : '';
      }
    },

    watch: {
      closed(newVal) {
        if (newVal) {
          this.visible = false;
          //transitionend事件在 CSS 完成过渡后触发。
          this.$el.addEventListener('transitionend', this.destroyElement);
        }
      }
    },

    methods: {
      destroyElement() {
        this.$el.removeEventListener('transitionend', this.destroyElement);
        //完全销毁一个实例。清理它与其它实例的连接，解绑它的全部指令及事件监听器。
        // 在vue v1.x中$destroy(true)的参数为true时，则从DOM中删除其关联的DOM元素或片段；在vue2.0中不需要加参数
        this.$destroy(true);
        this.$el.parentNode.removeChild(this.$el);
      },

      close() {
        this.closed = true;
        if (typeof this.onClose === 'function') {
          this.onClose(this);
        }
      },
      //鼠标进入消息提示弹窗时，定时器清空，弹窗一直显示
      clearTimer() {
        clearTimeout(this.timer);
      },
      // 鼠标离开消息提示弹窗时，设置定时器，弹窗在this.duration关闭
      startTimer() {
        if (this.duration > 0) {
          this.timer = setTimeout(() => {
            if (!this.closed) {
              this.close();
            }
          }, this.duration);
        }
      },
      // esc关闭消息
      keydown(e) {
        if (e.keyCode === 27) {
          if (!this.closed) {
            this.close();
          }
        }
      }
    },
    mounted() {
      this.startTimer();
      document.addEventListener('keydown', this.keydown);
    },
    beforeDestroy() {
      document.removeEventListener('keydown', this.keydown);
    }
  };
</script>