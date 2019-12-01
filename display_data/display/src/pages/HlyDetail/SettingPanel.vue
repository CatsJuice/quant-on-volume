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
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showPanel: true,
      selectedDaySum: undefined
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
      handler(val) {
      
      },
      deep: true,
      immediate: true
    },

    selectedDaySum(val) {
      this.$store.commit("hly/UPDATE", {
        constant: "daySum",
        value: parseInt(val.replace("sum_", ""))
      })
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
      flex-direction: column;

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