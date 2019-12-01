import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)


const state = {

}

const getters = {}
for (const constantName in state) {
  if (state.hasOwnProperty(constantName)) {
    getters[constantName] = state => {
      return state[constantName];
    }
  }
}

const mutations = {
  
}


const modulesFiles = require.context('./modules', true, /\.js$/)


const modules = modulesFiles.keys().reduce((modules, modulePath) => {
  // set './app.js' => 'app'
  const moduleName = modulePath.replace(/^\.\/(.*)\.\w+$/, '$1')
  const value = modulesFiles(modulePath)
  modules[moduleName] = value.default
  return modules
}, {})
export default new Vuex.Store({
  state,
  getters,
  mutations,
  // actions,
  modules,
})
