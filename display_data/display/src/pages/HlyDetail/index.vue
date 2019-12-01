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
      moveable: true,
      opt: {},
      loading: false,
      storedData: undefined
    };
  },
  computed: {
    code() {
      // this.updateOpt(this.$route.params.code)
      let code = this.$route.params.code;
      this.processByCode(code);
      return code;
    },
    daySum() {
      return this.$store.getters["hly/daySum"];
    }
  },
  mounted() {},
  watch: {
    daySum(val) {
      this.processByCode(this.code);
    }
  },
  methods: {
    handleResize: debounce((e, vm) => {
      vm.$refs.echarts.resize();
    }, 10),

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
          daySum: this.daySum
        });

        this.opt = cloneDeep(newOpt);
        this.$store.commit("hly/UPDATE", {
          constant: "selectedData",
          value: data
        });
      });
      this.loading = false;
    }
  },
  render() {
    const { moveable, handleResize, code } = this;
    const initOptions = {
      render: "canvas"
    };
    if (codeList.filter(e => e === code).length == 0) return <empty-page />;
    return (
      <div class="row">
        <drag-resize
          ww={800}
          hh={600}
          x={100}
          y={100}
          resizable={true}
          initOptions={initOptions}
          moveable={moveable}
          vOn:resizemove={e => handleResize(e, this)}
        >
          <div id="print-panel">
            <div class="drag"></div>
            <echarts
              id="echats"
              class="chart-output-content"
              initOptions={initOptions}
              options={this.opt}
              ref="echarts"
            />
          </div>
        </drag-resize>
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
</style>