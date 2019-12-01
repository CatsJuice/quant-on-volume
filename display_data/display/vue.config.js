// vue.config.js
module.exports = {
  publicPath:"./",
    // 输出文件目录
  outputDir: 'dist',
  devServer: {
    proxy: 'http://localhost:3000'
  },
  chainWebpack: config => {
    // json5 Loader
    config.module
      .rule('json5')
      .test(/\.json5$/)
      .use('json5-loader')
      .loader('json5-loader')
      .end()
  },
  transpileDependencies: [
    'vue-echarts',
    'resize-detector'
  ],
  runtimeCompiler: false,
  css: {
    loaderOptions: {
      less: {
        javascriptEnabled: true
      }
    }
  }
}
