import Vue from 'vue';
import Main from './main.vue';

let MessageConstructor = Vue.extend(Main);

let instance;
let instances = []; // 存放当前未close的message
let seed = 1;

const Message = function(options) {
  // 当前 Vue 实例是否运行于服务器
  if (Vue.prototype.$isServer) return;
  options = options || {};
  if (typeof options === 'string') {
    options = {
      message: options
    };
  }
  //userOnClose用来存放用户设置关闭时的回调函数, 参数为被关闭的 message 实例
  let userOnClose = options.onClose;
  let id = 'message_' + seed++;

  // 重写options.onClose
  options.onClose = function() {
    Message.close(id, userOnClose);
  };
   // 创建message实例,此时数据还没有挂载呢，$el 属性目前不可见，无法访问到数据和真实的dom
  instance = new MessageConstructor({
    data: options
  });
  instance.id = id;


   //手动地挂载一个未挂载的实例。$mount(param)中param不存在时，模板将被渲染为文档之外的的元素，并且你必须使用原生 DOM API 把它插入文档中。
  instance.vm = instance.$mount();
  //用原生DOM API把它插入body中
  document.body.appendChild(instance.vm.$el);
  instance.vm.visible = true;
  instance.dom = instance.vm.$el;
  // css z-index层级叠加，覆盖之前已出现但还未close的message
  instance.dom.style.zIndex = 9999;
  instances.push(instance);
  return instance.vm;
};

// 给Message增加四个直接调用的方法
// 支持this.$message.success('xxx')方式调用，等同于this.$message({type: 'success',message: 'xxx'})
['success', 'warning', 'info', 'error'].forEach(type => {
  Message[type] = options => {
    if (typeof options === 'string') {
      options = {
        message: options
      };
    }
    options.type = type;
    return Message(options);
  };
});

// 组件的close方法中调用onClose再调该方法
Message.close = function(id, userOnClose) {
  for (let i = 0, len = instances.length; i < len; i++) {
    if (id === instances[i].id) { // 通过id找到该message实例
      if (typeof userOnClose === 'function') {
        userOnClose(instances[i]);
      }
      instances.splice(i, 1);  // 移除message实例
      break;
    }
  }
};
//关闭所有的消息提示弹窗
Message.closeAll = function() {
  for (let i = instances.length - 1; i >= 0; i--) {
    instances[i].close();
  }
};

export default Message;