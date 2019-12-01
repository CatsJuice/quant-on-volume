<template>
  <div id="hly-list-root">
    <div class="card">
      <header>
        <el-select v-model="value" filterable placeholder="请选择">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          ></el-option>
        </el-select>

        <el-button
         style="margin-left:10px;"
          @click="jpToDetail" 
          :disabled="!this.value"
          type="primary">
          Go!
          </el-button>
      </header>

      <main>
          <div 
          :class="['code', opt.value==value?'ckd':'']" 
          v-for="opt in options" 
          :key="opt.value" 
          @click="value=opt.value">
              {{ opt.value }}
          </div>
      </main>
    </div>
  </div>
</template>

<script>
import codes from "@/data/code_list.js";
export default {
  name: "codelist",
  data() {
    return {
      value: undefined
    };
  },
  computed: {
    options() {
      return codes.map(code => {
        return { label: code, value: code };
      });
    }
  },
  methods: {
      jpToDetail() {
         this.$router.push({path:`/hly/${this.value}`})
      }
  },
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
    @media screen and(min-width: 1000px) {
      width: 900px;
    }
    background-color: #fff;

    header {
        width: 100%;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    main {
        width: 90%;
        margin-left: 5%;
        display: flex;
        flex-wrap: wrap;
        cursor: pointer;
            overflow-y: scroll;
        height: ~"calc(100% - 120px)";
        padding-bottom: 100px;
        box-sizing: border-box;
        .code {
            width: 80px;
            height: 40px;
            line-height: 40px;
            margin: 5px;
            font-size: 0.8rem;
            // font-weight: bold;
            transition: all 0.3s ease-in-out;
            text-align: center;
            background-color: #f6f6f6;
            border-radius: 5px;
            justify-content: flex-start;
            &:hover,
            &.ckd {
                background-color: rgb(102,177,255);
                color: #fff;
                font-weight: bold;
                box-shadow:0px 0px 10px rgba(102,177,255,.5);
            }
        }
    }
  }
}
</style>