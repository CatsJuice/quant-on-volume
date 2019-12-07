<template>
  <div id="hly-list-root">
    <div class="loading" v-if="this.loading">
      <span>正在加载...</span>
      <span></span>
    </div>
    <div class="card">
      <header>
        <section>
          <!-- 选择筛选方式 -->
          <el-select style="margin-right:10px;" v-model="query" filterable placeholder="选择筛选的方式">
            <el-option
              v-for="item in queryOpt"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>

          <!-- 筛选综合选项 -->
          <el-select
            style="margin-right:10px;"
            v-model="currentHlyZLJCDate"
            filterable
            placeholder="根据日期筛选"
            v-if="query == 2"
          >
            <el-option label="全部日期" :value="0"></el-option>
            <el-option
              v-for="item in hly_ZLJC_dates_opt"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>

          <!-- 筛选得分最高的 -->
          <el-select
            style="margin-right:10px;"
            v-model="currentDate"
            filterable
            placeholder="根据日期筛选"
            v-if="query == 0"
          >
            <el-option label="全部日期" :value="0"></el-option>
            <el-option
              v-for="item in datesOpt"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>

          <!-- 筛选得分稳定增加的 -->
          <el-select
            style="margin-right:10px;"
            v-model="raiseDate"
            filterable
            placeholder="根据日期筛选"
            v-if="query == 1"
          >
            <el-option label="全部日期" :value="0"></el-option>
            <el-option
              v-for="item in raiseDatesOpt"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>

          <!-- 筛选得分稳定增加的 (筛选天数)-->
          <el-select
            style="margin-right:10px;"
            v-model="day"
            filterable
            placeholder="筛选连续打分天数"
            v-if="query == 1 && raiseDate != 0"
          >
            <el-option
              v-for="item in days"
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
import { cloneDeep } from "lodash";
export default {
  name: "codelist",
  data() {
    return {
      value: undefined,
      currentDate: 0,
      raiseDate: 0,
      loading: false,
      queryOpt: [
        { label: "根据日期筛选得分最高的", value: 0 },
        { label: "根据日期筛选得分稳定增加的", value: 1 },
        { label: "根据 hly 打分和 ZLJC ", value: 2 }
      ],
      query: 0,
      day: undefined,
      currentHlyZLJCDate: 0
    };
  },
  computed: {
    options() {
      let opt;
      if (this.query == 0) {
        if (this.currentDate == 0) {
          opt = codes.map(code => {
            return { label: code, value: code };
          });
        } else {
          opt = this.queryByDate[this.currentDate].map(code => {
            return { label: code, value: code };
          });
        }
      } else if (this.query == 1) {
        if (this.raiseDate == 0) {
          opt = codes.map(code => {
            return { label: code, value: code };
          });
        } else {
          if (this.day) {
            if (!this.queryByDateRaise[this.raiseDate][this.day]) {
              this.day = undefined;
              opt = codes.map(code => {
                return { label: code, value: code };
              });
            }
            opt = this.queryByDateRaise[this.raiseDate][this.day].map(code => {
              return { label: code, value: code };
            });
          } else {
            return [];
          }
        }
      } else if (this.query == 2) {
        if (this.currentHlyZLJCDate == 0) {
          opt = codes.map(code => {
            return { label: code, value: code };
          });
        } else {
          return this.hlyZLJCRes[this.currentHlyZLJCDate].map(code => {
            return { label: code, value: code };
          });
        }
      }
      // this.loading = false;

      return opt;
    },
    queryByDate() {
      return require("@/data/hly_count_res_max_2_group_by_date.json");
    },

    queryByDateRaise() {
      return require("@/data/up_res_group_by_date_strict_mode.json");
    },
    hlyZLJCRes() {
      return require("@/data/hly_and_zljc_res.json");
    },

    datesOpt() {
      return Object.keys(this.queryByDate)
        .sort((a, b) => {
          return (
            parseInt(b.split("-").join("")) - parseInt(a.split("-").join(""))
          );
        })
        .map(date => {
          return { label: date, value: date };
        });
    },

    raiseDatesOpt() {
      return Object.keys(this.queryByDateRaise)
        .sort((a, b) => {
          return (
            parseInt(b.split("-").join("")) - parseInt(a.split("-").join(""))
          );
        })
        .map(date => {
          return { label: date, value: date };
        });
    },

    days() {
      return Object.keys(this.queryByDateRaise[this.raiseDate]).map(day => {
        return { label: `sum_${day.slice(1)}`, value: day };
      });
    },
    hly_ZLJC_dates_opt() {
      return Object.keys(this.hlyZLJCRes)
        .sort((a, b) => {
          return (
            parseInt(b.split("-").join("")) - parseInt(a.split("-").join(""))
          );
        })
        .map(date => {
          return { label: date, value: date };
        });
    }
  },
  methods: {
    jpToDetail() {
      this.$router.push({ path: `/hly/${this.value}` });
    },
    confirmQuery() {
      console.log(this.raiseDate, this.day);
      // this.option = this.queryByDateRaise[this.raiseDate][this.day].map(code => {
      //   return { label: code, value: code}
      // })
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