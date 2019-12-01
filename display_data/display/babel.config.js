module.exports = {
  presets: [
    '@vue/cli-plugin-babel/preset'
  ],
  "plugins": [
    [
      "component",
      {
        "libraryName": "element-ui",
        "styleLibraryName": "theme-chalk"
      }
    ],
    /* ant-design-vue-component-import */
    [
      "import",
      { libraryName: "ant-design-vue", libraryDirectory: "es", style: true }
    ],
  ]
}
