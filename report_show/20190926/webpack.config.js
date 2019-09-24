const path = require('path');
const webpack = require('webpack');

// 导入 html-webpack-plugin
const htmlWebpackPlugin = require('html-webpack-plugin');

// 导入 VueLoaderPlugin
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
    entry: path.join(__dirname, './src/main.js'),      // 入口
    output: {
        path: path.join(__dirname, './dist'),           // 输出路径
        filename: 'bundle.js'                           // 输出文件名
    },
    devServer: {                  // 配置 dev-server
        open: true,               // 自动打开浏览器
        port: 9998,               // 端口
        contentBase: 'src',       // 托管的根目录
        hot: true                 // 启用热更新
    },
    plugins: [      // 插件配置
        new webpack.HotModuleReplacementPlugin(),                 // 热更新模块对象
        new htmlWebpackPlugin({                                   // 在内存中生成 html 页面的插件
            template: path.join(__dirname, './src/index.html'),   // 指定模板页面， 根据指定页面生成内存中的页面
            filename: 'index.html'                                // 指定生成的页面名称
        }),
        new VueLoaderPlugin()
    ],

    module: {   // 配置第三方模块加载器
        rules: [
            { test: /\.css$/, use: ['style-loader', 'css-loader'] },
            { test: /\.less$/, use: ['style-loader', 'css-loader', 'less-loader'] },
            { test: /\.scss$/, use: ['style-loader', 'css-loader', 'sass-loader'] },
            { test: /\.(jpg|png|gif|bmp|jpeg)$/, use: 'url-loader?limit=10000' },    // &name=[name].[ext] 图片名不变
            { test: /\.(eot|svg|ttf|woff|woff2)$/, use: 'url-loader' },              // 处理字体文件
            { test: /\.js$/, use: 'babel-loader', exclude: /node_modules/ },         // 配置 babel 来转换高级的ES语法
            { test: /\.vue$/, use: 'vue-loader' }
        ]
    },
    resolve: {
        alias: {    // 修改 vue 导入时的路径
            // 'vue$': "vue/dist/vue.js"
        }
    }
};