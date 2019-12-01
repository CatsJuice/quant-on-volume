<template>
  <div id="setting-panel" :class="`${showPanel?'show':''}`">
    <div class="toggle-btn">
      <input type="checkbox" v-model="showPanel" />
      <span></span>
      <span></span>
      <span></span>
    </div>

    <div class="title">Setting Panel</div>

    <div class="setting-items">
      <!-- 设置项 -->
      <div class="setting-item">
        <div class="label">
          <span>连续打分的天数</span>
          <el-tooltip class="item" effect="dark" content="选择连续统计几天的打分和" placement="top">
            <img src="@/assets/images/icon/wh.svg" />
          </el-tooltip>
        </div>
        <el-select v-model="selectedDaySum" placeholder="请选择">
          <el-option
            v-for="item in daySumOption"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>
      </div>

      <!-- 设置项 -->
      <div class="setting-item">
        <div class="label">
          <span>要显示的 MA</span>
          <el-tooltip class="item" effect="dark" content="输入以添加更多选项，取值范围为5-100" placement="top">
            <img src="@/assets/images/icon/wh.svg" />
          </el-tooltip>
        </div>
        <el-select
          :multiple="true"
          :filterable="true"
          :allow-create="true"
          :default-first-option="true"
          v-model="selectedMA"
          placeholder="请选择 MA "
          @change="handleMASelect"
        >
          <el-option v-for="ma in maOption" :key="ma.value" :label="ma.label" :value="ma.value"></el-option>
        </el-select>

        <!-- <el-button style="margin: 10px 0;">确认MA</el-button> -->
      </div>

      <div class="setting-item" style="align-items:stretch;">
        <div class="row">
          <span style="font-szie:0.9rem;font-weight:bold;">显示打分统计结果</span>
          <div style="flex-grow:1;"></div>
          <el-switch v-model="showResult" active-color="#45B39D" inactive-color="#CD6155"></el-switch>
        </div>
      </div>

      <div class="setting-item" v-if="showResult">
        <div class="label">
          <span>选择结果类别</span>
          <el-tooltip class="item" effect="dark" content="查看上升趋势或下降趋势的统计" placement="top">
            <img src="@/assets/images/icon/wh.svg" />
          </el-tooltip>
        </div>
        <el-select @change="handleResTypeChange" v-model="selectedResType" placeholder="请选择类别 ">
          <el-option
            v-for="restype in resTypeOption"
            :key="restype.value"
            :label="restype.label"
            :value="restype.value"
          ></el-option>
        </el-select>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showPanel: true,
      selectedDaySum: undefined,
      selectedMA: [],
      maOption: [
        { label: 5, value: 5 },
        { label: 10, value: 10 },
        { label: 15, value: 15 },
        { label: 20, value: 20 }
      ],
      showResult: false,

      selectedResType: 0,
      resTypeOption: [
        { label: "上升趋势", value: 0 },
        { label: "下降趋势", value: 1 },
        { label: "上升百分比", value: 2 }
      ]
      // daySumOption: [{ label: "", value: "" }]
    };
  },
  computed: {
    selectedData() {
      return this.$store.getters["hly/selectedData"];
    },
    daySumOption() {
      if (this.selectedData.length == 0) return [];
      return Object.keys(this.selectedData[0])
        .map(key => {
          if (key.substr(0, 3) === "sum") return { label: key, value: key };
        })
        .filter(item => item != undefined);
    }
  },
  watch: {
    selectedData: {
      handler(val) {},
      deep: true,
      immediate: true
    },

    selectedDaySum(val) {
      this.$store.commit("hly/UPDATE", {
        constant: "daySum",
        value: parseInt(val.replace("sum_", ""))
      });
    },
    showResult(value) {
      this.$store.commit("hly/UPDATE", {
        constant: "showCount",
        value
      });
    }
  },
  methods: {
    handleMASelect(val) {
      if (val.length != 0 && isNaN(parseInt(val[val.length - 1]))) {
        this.$message.error("请输入 5 - 100 之间的整数");
        this.selectedMA.pop();
      } else {
        if (parseInt(val[val.length - 1]) + "" !== val[val.length - 1]) {
          this.$message.warn(
            `输入${val[val.length - 1]}包含字符,已转换为${parseInt(
              val[val.length - 1]
            )}`
          );
        }
        this.selectedMA[val.length - 1] = parseInt(val[val.length - 1]);

        if (
          this.selectedMA[val.length - 1] > 100 ||
          this.selectedMA[val.length - 1] < 5
        ) {
          this.$message.error("请输入 5 -100 之间的整数");
          this.selectedMA.pop();
        }
      }

      this.$store.commit("hly/UPDATE", {
        constant: "ma",
        value: val
      });
    },
    handleResTypeChange(value) {
      this.$store.commit("hly/UPDATE", {
        constant: "currentResType",
        value
      });
    }
  }
};
</script>

<style lang="scss" scoped>
* {
  transition: all 0.3s ease-in-out;
}
#setting-panel {
  position: fixed;
  right: -300px;
  width: 280px;
  height: 100%;
  background-color: #fff;
  box-shadow: -3px 0px 10px rgba(0, 0, 0, 0.1);

  .setting-items {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 50px 20px;

    .setting-item {
      display: flex;
      width: 100%;
      flex-direction: column;
      margin: 10px 0;

      .label {
        display: flex;
        height: 40px;
        line-height: 40px;
        font-size: 0.9rem;
        font-weight: bold;
        color: #505050;
        img {
          width: 16px;
          margin-left: 10px;
          cursor: pointer;
        }
      }
    }
  }

  &.show {
    right: 0;
  }

  .toggle-btn {
    width: 50px;
    height: 50px;
    right: 10px;
    top: 10px;
    cursor: pointer;
    &:hover {
      background-color: rgba(0, 0, 0, 0.09);
    }
    position: fixed;
    span {
      display: inline-block;
      width: 25px;
      height: 2px;
      background-color: rgb(48, 48, 48);
      position: absolute;
      top: 50%;
      left: 50%;
      margin-left: -15px;
      margin-top: -1px;
      &:nth-child(2) {
        margin-top: -8px;
        // margin-top: -7px;
        // margin-left: 0px;
        // width: 17px;
        // transform: rotate(45deg);
      }
      &:nth-child(3) {
        margin-top: 7px;
        // margin-left: 0px;
        // width: 17px;
        // transform: rotate(-45deg);
      }
    }
    input[type="checkbox"] {
      position: absolute;
      width: 100%;
      height: 100%;
      z-index: 1100;
      opacity: 0;
      cursor: pointer;

      &:checked ~ span {
        &:nth-child(2) {
          // margin-top: -10px;
          margin-top: -7px;
          margin-left: -4px;
          width: 17px;
          transform: rotate(45deg);
        }
        &:nth-child(3) {
          margin-top: 5px;
          margin-left: -4px;
          width: 17px;
          transform: rotate(-45deg);
        }
      }
    }
  }

  .title {
    box-sizing: content-box;
    width: 100%;
    height: 50px;
    margin-top: 10px;
    line-height: 50px;
    font-size: 1.1rem;
    font-weight: bold;
    border-left: 7px solid rgb(50, 24, 196);
    padding-left: 20px;
  }
}
</style>