const state = {
    daySum: 7,
    selectedData: [],
    ma: [],
    showCount: false,
    currentDataType: 0,
    currentResType: 0,
    resMA: undefined,
    resDay: undefined,
    forceResPos: {
        max: false,
        min: false,
    },
    forcePos: {
        max: false,
        min: false
    }
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
    'UPDATE'(state, {
        constant,
        value
    }) {
        state[constant] = value;
    },
    'RESET_RES'(state) {
        state["showCount"] = false;
        state["currentDataType"] = 0;
        state["currentResType"] = 0;
        state["resMA"] = undefined;
        state["resDay"] = undefined;

    },
}


const actions = {

}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}
