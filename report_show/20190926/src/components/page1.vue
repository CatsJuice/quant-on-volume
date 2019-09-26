<template>
  <div id="page1" :class="current?'current':''">
    <div class="big-title">
      <p>基于成交量的</p>
      <p>股票数据分析系统</p>
      <p>Stock Data Analysis System Based on Trading Volume</p>
    </div>

    <div class="person-info">
      <p>2019年9月26日 2020春·毕业设计开题报告</p>
      <p>&copy; 16905833 徐志剑</p>
    </div>
  </div>
</template>

<script>
export default {
  props: ["current"]
};
</script>

<style lang="scss" scoped>
* {
  transition: all 0.3s ease-in-out;
}
#page1 {
  width: 100vw;
  height: 100vh;
  padding: 100px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  .big-title {
    & > p:nth-child(1) {
      font-size: 5rem;
      font-weight: 1000;
      position: relative;
      display: inline-block;
      border-left: 20px solid #000;
      line-height: 55px;
      padding-left: 20px;
      vertical-align: baseline;
    }
    & > p:nth-child(2) {
      font-size: 3rem;
    }
    & > p:nth-child(3) {
      font-size: 1.6rem;
    }
    & > p {
      transform: translateY(100px);
    }
  }

  .person-info {
    p:nth-child(1) {
      font-size: 1.6rem;
      font-weight: 600;
    }
    p:nth-child(2) {
      font-size: 1.4rem;
    }
    p {
      transform: translateY(100px);
    }
  }
}

// 动画
.current {
  .big-title {
    p:nth-child(1) {
      transform: translateY(0px) !important;
      transition: all 0.6s ease 0.6s !important;
    }
    p:nth-child(2) {
      transform: translateY(0px) !important;
      transition: all 0.6s ease 0.7s !important;
    }
    p:nth-child(3) {
      transform: translateY(0px) !important;
      transition: all 0.6s ease 0.8s !important;
    }
  }
  .person-info {
    p:nth-child(1) {
      transform: translateY(0px) !important;
      transition: all 0.6s ease 0.6s !important;
    }
    p:nth-child(2) {
      transform: translateY(0px) !important;
      transition: all 0.6s ease 0.7s !important;
    }
  }
}

@media screen and(max-width: 400px) {
  #page1 {
    padding: 50px 20px;
    .big-title {
      & > p:nth-child(1) {
        font-size: 3rem;
        font-weight: 600;
        padding-left: 10px;
        border-left: 16px solid #000;
        line-height: 36px;
      }

      & > p:nth-child(2) {
          font-size: 2.4rem;
      }
      & > p:nth-child(3) {
          font-size: 1rem;
      }
    }
  }
}
</style>