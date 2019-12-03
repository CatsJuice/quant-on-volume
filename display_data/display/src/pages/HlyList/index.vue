<template>
  <div id="hly-list-root">
    <div class="loading" v-if="this.loading">
      <span>正在加载...</span>
      <span></span>
    </div>
    <div class="card">
      <header>
        <section>
          <span>根据日期筛选得分最高的：</span>
          <el-select
            style="margin-right:10px;"
            v-model="currentDate"
            filterable
            placeholder="根据日期筛选"
          >
            <el-option label="全部日期" :value="0"></el-option>
            <el-option
              v-for="item in datesOpt"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </section>

        <section>
          <el-select v-model="value" filterable placeholder="选择代码">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
          <el-button
            style="margin:0px 10px;"
            @click="jpToDetail"
            :disabled="!this.value"
            type="primary"
          >Go!</el-button>
        </section>
      </header>

      <div id="main">
        <div
          :class="['code', opt.value==value?'ckd':'']"
          v-for="opt in options"
          :key="opt.value"
          @click="value=opt.value"
        >{{ opt.value }}</div>

        <div v-for="i in 100" :key="i" class="fill"></div>
      </div>
    </div>
  </div>
</template>

<script>
import codes from "@/data/code_list.js";
import { cloneDeep } from 'lodash'
export default {
  name: "codelist",
  data() {
    return {
      value: undefined,
      currentDate: 0,
      loading: false
    };
  },
  computed: {
    options() {
      let opt;
      if (this.currentDate == 0) {
        opt = codes.map(code => {
          return { label: code, value: code };
        });
      } else {
        opt = this.queryByDate[this.currentDate].map(code => {
          return { label: code, value: code };
        });
      }
      // this.loading = false;

      return opt;
    },
    queryByDate() {
      return require("@/data/hly_count_res_max_2_group_by_date.json");
    },

    datesOpt() {
      return Object.keys(this.queryByDate).sort((a, b) => {
        return parseInt(a.split("-").join("")) - parseInt(b.split("-").join(""));
      }).map(date => {
        return { label: date, value: date };
      });
    }
  },
  methods: {
    jpToDetail() {
      this.$router.push({ path: `/hly/${this.value}` });
    }
  }
};
</script>

<style lang="less" scoped>
#hly-list-root {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background-color: #f6f6f6;

  .card {
    height: 90vh;
    margin: 0px auto;
    margin-top: 5vh;
    padding: 0;
    border-radius: 5px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    @media screen and(max-width: 1000px) {
      width: 90%;
    }
    @media screen and(min-width: 1300px) {
      width: 1200px;
    }
    background-color: #fff;

    header {
      margin-top: 10px;
      margin-bottom: 20px;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 50px;
    }
    #main {
      width: 90%;
      margin-left: 5%;
      display: flex;
      flex-wrap: wrap;
      overflow-y: scroll;
      // background-color: aquamarine;
      height: ~"calc(100% - 120px)";
      padding-bottom: 100px;
      box-sizing: content-box;
      align-content: flex-start !important;
      justify-content: space-around;
      .code {
        width: 80px;
        height: 40px;
        line-height: 40px;
        cursor: pointer;
        margin: 5px;
        font-size: 0.8rem;
        // font-weight: bold;
        transition: all 0.3s ease-in-out;
        text-align: center;
        background-color: #f6f6f6;
        border-radius: 5px;
        justify-content: flex-start;
        flex-shrink: 0;
        &:hover,
        &.ckd {
          background-color: rgb(102, 177, 255);
          color: #fff;
          font-weight: bold;
          box-shadow: 0px 0px 10px rgba(102, 177, 255, 0.5);
        }
      }
      .fill {
        width: 80px;
        height: 2px;
        flex-shrink: 0;
        margin: 5px;
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
  z-index: 9999;

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
</style>