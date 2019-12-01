<script>
import Echarts from "vue-echarts";
import SettingPanel from "./SettingPanel";
import DragResize from "@/components/DragResize";
import EmptyPage from "../EmptyPage";

import "echarts/";
import { debounce, cloneDeep } from "lodash";
import { Loading } from "element-ui";

const codeList = require("@/data/code_list.js").default;
// const optProcess = require("@/assets/chartOpt/c0001.js");
export default {
  name: "hlyDetail",
  components: {
    Echarts,
    SettingPanel,
    DragResize,
    EmptyPage
  },
  data() {
    return {
      ww: 800,
      hh: 600,
      x: 100,
      y: 100,
      moveable: true,
      opt: {},
      resOpt: {},
      loading: false,
      storedData: undefined,
      currentActive: "echarts"
    };
  },
  computed: {
    code() {
      // this.updateOpt(this.$route.params.code)
      let code = this.$route.params.code;
      this.processByCode(code);
      return code;
    },
    ma() {
      return this.$store.getters["hly/ma"];
    },
    daySum() {
      return this.$store.getters["hly/daySum"];
    },
    currentResType() {
      return this.$store.getters["hly/currentResType"];
    },
    showCount() {
      let show = this.$store.getters["hly/showCount"];
      if (show) this.processResOpt();
      return show;
    }
  },
  mounted() {},
  watch: {
    daySum(val) {
      this.processByCode(this.code);
    },
    ma(val) {
      this.processByCode(this.code);
    },
    currentResType(val) {
      this.processResOpt();
    }
  },
  methods: {
    handleResize: debounce((e, vm, target) => {
      vm.$refs[target].resize();
      vm.currentActive = target;
    }, 10),
    processResOpt() {
      const promisedOptProcesser = () => import("@/assets/chartOpt/c0002.js");
      promisedOptProcesser().then(res => {
        const optProcessor = res.default;
        const newOpt = optProcessor({
          dataPlus: require("@/data/hly_count_res_plus.json"),
          dataReduce: require("@/data/hly_count_res_reduce.json"),
          currentResType: this.currentResType
        });
        this.resOpt = cloneDeep(newOpt);
        console.log(newOpt)
      });
    },
    async processByCode(code) {
      this.loading = true;
      let data = [];

      if (
        this.storedData !== undefined &&
        this.storedData.length > 0 &&
        this.storedData[0]["股票代码"].slice(1) == code
      ) {
        data = this.storedData;
      } else {
        let res = await this.$axios.get("http://stock.catsjuice.top/api/hly", {
          params: {
            code: code
          }
        });
        data = res.data.data;
        this.storedData = data;
      }
      const promisedOptProcesser = () => import("@/assets/chartOpt/c0001.js");
      promisedOptProcesser().then(res => {
        const optProcessor = res.default;
        const newOpt = optProcessor({
          data,
          daySum: this.daySum,
          ma: this.ma
        });

        this.opt = cloneDeep(newOpt);
        this.$store.commit("hly/UPDATE", {
          constant: "selectedData",
          value: data
        });
      });
      this.loading = false;
    },

    smallest() {
      this.ww = 50;
      this.hh = 50;
      this.x = 0;
      this.y = 0;
    },

    switchCurrentActive(tar) {
      this.currentActive = tar;
    }
  },
  render() {
    const { moveable, handleResize, code, ww, hh, x, y } = this;
    const initOptions = {
      render: "canvas"
    };
    if (codeList.filter(e => e === code).length == 0) return <empty-page />;

    let countResult = (
      <transition
        enter-active-class="animated fadeIn"
        leave-active-class="animated fadeOutWithouDelay"
      >
        <drag-resize
          style={this.currentActive == "echarts2" ? "z-index:9999;" : ""}
          ww={800}
          hh={800}
          x={50}
          y={50}
          resizable={true}
          initOptions={initOptions}
          vOn:resizemove={e => handleResize(e, this, "echarts2")}
        >
          <div
            id="print-panel"
            onMousedown={e => this.switchCurrentActive("echarts2")}
          >
            <div class="drag">
              <span class="chart-output-content">
                <span></span>
                <span></span>
              </span>
              <span class="chart-output-content"></span>
              <span class="chart-output-content">
                <span></span>
              </span>
            </div>
            <echarts
              id="echats"
              class="chart-output-content"
              initOptions={initOptions}
              options={this.resOpt}
              autoresize
              ref="echarts2"
            />
          </div>
        </drag-resize>
      </transition>
    );
    return (
      <div class="row">
        <drag-resize
          ww={ww}
          hh={hh}
          x={x}
          y={y}
          resizable={true}
          initOptions={initOptions}
          moveable={moveable}
          style={this.currentActive == "echarts" ? "z-index:9999;" : ""}
          vOn:resizemove={e => handleResize(e, this, "echarts")}
        >
          <div
            id="print-panel"
            onMousedown={e => this.switchCurrentActive("echarts")}
          >
            <div class="drag">
              <span class="chart-output-content">
                <span></span>
                <span></span>
              </span>
              <span class="chart-output-content"></span>
              <span class="chart-output-content" vOn:click={this.smallest}>
                <span></span>
              </span>
            </div>
            <echarts
              id="echats"
              class="chart-output-content"
              initOptions={initOptions}
              options={this.opt}
              ref="echarts"
            />
          </div>
        </drag-resize>

        {this.showCount ? countResult : ""}

        <setting-panel />
        <transition
          enter-active-class="animated slideInDown"
          leave-active-class="animated fadeOut"
        >
          {this.loading ? (
            <div class="loading">
              <span>正在加载...</span>
              <span></span>
            </div>
          ) : (
            ""
          )}
        </transition>
      </div>
    );
  }
};
</script>

<style lang="less">
@drag-height: 50px;

.row {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  #print-panel {
    width: 100%;
    height: 100%;
    background-color: #fff;
    box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    overflow: hidden;
    #echats {
      width: 100%;
      height: ~"calc(100% - @{drag-height})";
      box-shadow: 0px -1px 10px rgba(0, 0, 0, 0.3);
    }
  }
  .drag {
    width: 100%;
    background-color: #d3d6e0;
    height: @drag-height;
    // box-shadow: 0px 10px 10px rgba(0,0,0,.1) inset;
    display: flex;
    align-items: center;
    flex-direction: row;
    padding-left: 10px;
    overflow: hidden;
    span {
      display: block;
      width: 16px;
      height: 16px;
      margin: 0 2px;
      border-radius: 50%;
      background-color: aqua;
      cursor: pointer;
      transition: all 0.2s ease-in-out;
      position: relative;

      &:hover {
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
      }
      &:nth-child(1) {
        background-color: #cd6155;

        & > span {
          position: absolute;
          width: 60%;
          height: 1px;
          background-color: #fff;
          transform-origin: center;
          margin-top: 50%;
          margin-left: 20%;
          opacity: 0;
          top: -1px;
          &:nth-child(1) {
            transform: rotate(45deg);
          }
          &:nth-child(2) {
            transform: rotate(-45deg);
          }
        }
        &:hover {
          background-color: #832f26;
          & > span {
            opacity: 1;
          }
        }
      }
      &:nth-child(2) {
        background-color: #f5b041;
        &:hover {
          background-color: #d39430;
        }
      }
      &:nth-child(3) {
        background-color: #45b39d;

        span {
          width: 66%;
          height: 2px;
          background-color: #fff;
          position: absolute;
          top: 50%;
          left: 17%;
          margin: 0;
          margin-top: -1px;
          opacity: 0;
        }
        &:hover {
          background-color: #349e89;
          & > span {
            opacity: 1;
          }
        }
      }
    }
  }

  .loading {
    transition: all 0.3s ease-in-out;
    position: absolute;
    top: 70px;
    left: 50%;
    margin-left: -100px;
    box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
    width: 200px;
    height: 55px;
    border-radius: 5px;
    background-color: #fff;
    z-index: 9000;

    display: flex;
    justify-content: center;
    align-items: center;
    span {
      display: inline-block;
      font-size: 0.8rem;

      &:nth-child(2) {
        border: 2px solid transparent;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        border-top: 2px solid rgb(78, 78, 78);
        border-right: 2px solid rgb(78, 78, 78);
        margin-left: 20px;
        animation: rotate 1s linear 0s infinite normal;
      }
      @keyframes rotate {
        from {
          transform: rotate(0deg);
        }
        to {
          transform: rotate(360deg);
        }
      }
    }
  }
}

.slideInDown {
  animation: slideInDown 0.2s ease 0s 1;
}
@keyframes slideInDown {
  from {
    transform: translateY(-55px);
  }
  to {
    transform: translateY(0px);
  }
}
.fadeOut {
  animation: fadeOut 0.5s ease 0.2s 1 forwards;
}
.fadeOutWithouDelay {
  animation: fadeOut 0.5s ease 0s 1 forwards;
}
@keyframes fadeOut {
  0% {
    opacity: 1;
    transform: translateY(0px);
  }
  100% {
    transform: translateY(-10px) scale(0.9);
    opacity: 0;
  }
}
.fadeIn {
  animation: fadeIn 0.5s ease 0s 1 forwards;
}
@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(-10px) scale(0.9);
  }
  100% {
    transform: translateY(0px);
    opacity: 1;
  }
}
</style>