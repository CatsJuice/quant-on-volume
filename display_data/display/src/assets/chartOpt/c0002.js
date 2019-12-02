import { cloneDeep } from "lodash";

const opt_3d_scatter = {
    tooltip: {},
    // visualMap: [{
    //     top: 10,
    //     calculable: true,
    //     dimension: 3,
    //     // max: max.color / 2,
    //     inRange: {
    //         color: ['#1710c0', '#0b9df0', '#00fea8', '#00ff0d', '#f5f811', '#f09a09', '#fe0300'],
    //         symbolSize: [0,100]
    //     },
    //     textStyle: {
    //         color: '#fff'
    //     }
    // }, {
    //     bottom: 10,
    //     calculable: true,
    //     dimension: 3,
    //     // max: max.symbolSize / 2,
    //     inRange: {
    //         symbolSize: [10, 40]
    //     },
    //     textStyle: {
    //         color: '#fff'
    //     }
    // }],

    visualMap: [{
        bottom: 10,
        calculable: true,
        dimension: 3,
        // max: max.color / 2,
        inRange: {
            color: ['#1710c0', '#0b9df0', '#00fea8', '#00ff0d', '#f5f811', '#f09a09', '#fe0300'],
            symbolSize: [0, 100]
        },
        textStyle: {
            color: '#fff'
        }
    }],
    xAxis3D: {
        name: "连续打分天数",
        type: 'value'
    },
    yAxis3D: {
        name: "用于计算的 MA 天数",
        type: 'value'
    },
    zAxis3D: {
        name: "得分结果",
        type: 'value'
    },
    grid3D: {
        axisLine: {
            lineStyle: {
                color: '#fff'
            }
        },
        axisPointer: {
            lineStyle: {
                color: '#ffbd67'
            }
        },
        viewControl: {
            // autoRotate: true
            // projection: 'orthographic'
        }
    },
    series: [{
        type: 'scatter3D',
        data: [],
        symbolSize: 12,
        // symbol: 'triangle',
        itemStyle: {
            borderWidth: 1,
            borderColor: 'rgba(255,255,255,0.8)'
        },
        emphasis: {

            itemStyle: {
                color: '#fff'
            }
        }
    }]
}


const opt_htmap = {
    tooltip: {
        position: 'top'
    },
    animation: false,
    grid: {
        height: '80%'
    },
    xAxis: {
        name: "得分和",
        type: 'category',
        // data: hours,
        splitArea: {
            show: true
        },
        nameTextStyle: {
            color:"#fff"
        },
        axisLine: {
            lineStyle: {
                color: "#fff",
            }
        },
        axisTick: {
            lineStyle: {
                color: "#fff"
            }
        },
        axisLabel: {
            lineStyle:{
                color: "#fff"
            }
        },
    },
    yAxis: {
        name: "计算的天数",
        nameTextStyle: {
            color:"#fff"
        },
        axisLine: {
            lineStyle: {
                color: "#fff",
            }
        },
        axisTick: {
            lineStyle: {
                color: "#fff"
            }
        },
        axisLabel: {
            lineStyle:{
                color: "#fff"
            }
        },
        type: 'category',
        // data: days,
        splitArea: {
            show: true
        }
    },
    visualMap: {
        // min: 0,
        // max: 10,
        calculable: true,
        dimension: 2,
        orient: 'horizontal',
        left: 'center',
        bottom: '2%',
        textStyle: {
            color: "#fff"
        }
    },
    series: [{
        name: 'value',
        type: 'heatmap',
        // data: data,
        label: {
            normal: {
                show: true
            }
        },
        itemStyle: {
            emphasis: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
        }
    }]
};



export default function ({
    dataPlus,
    dataReduce,
    currentDataType,
    currentResType,
    resDay,
    resMA,
}) {
    let sum_data = mergeData(dataPlus, dataReduce)
    let data
    if (currentDataType == 0)
        data = transformData(dataPlus)
    else if (currentDataType == 1)
        data = transformData(dataReduce)
    else if (currentDataType == 2)
        data = transformData(calcPercent(dataPlus, sum_data))
    else if (currentDataType == 3)
        data = transformData(calcPercent(dataReduce, sum_data))


    // VisualMap
    if (currentDataType == 2 || currentDataType == 3) {
        opt_3d_scatter.visualMap[0].max = 100
        opt_htmap.visualMap.max = 100
    } else {
        opt_3d_scatter.visualMap[0].max = getMaxInMatrix(matrixParseNumber(transformData(sum_data)))
        opt_htmap.visualMap.max = getMaxInMatrix(matrixParseNumber(transformData(sum_data)))
    }
    
    if (currentResType == 0) {
        // 3D 散点图
        data = matrixParseNumber(data)
        opt_3d_scatter.series[0].data = cloneDeep(data)
        return cloneDeep(opt_3d_scatter)
    } else if (currentResType == 1) {
        // 热力图
        opt_htmap.xAxis.data = Array.from(new Set(matrixParseNumber(data).map(row => row[2])))
        opt_htmap.yAxis.data = Array.from(new Set(matrixParseNumber(data).map(row => row[0])))
        
        opt_htmap.xAxis.data = opt_htmap.xAxis.data.sort((a,b) => a-b)
        opt_htmap.yAxis.data = opt_htmap.yAxis.data.sort((a,b) => a-b)
        
        opt_htmap.series[0].data = matrixParseNumber(data).filter(e => {
            return e[1] == parseInt(resMA.replace("ma_", "")) 
        }).map(row => {
            return [
                opt_htmap.xAxis.data.indexOf(row[2]), 
                opt_htmap.yAxis.data.indexOf(row[0]),
                row[3]
            ]
        })

        return cloneDeep(opt_htmap)
    }

}

function transformData(dic) {
    let res = []

    Object.keys(dic).forEach(sum_key => {
        Object.keys(dic[sum_key]).forEach(ma_key => {
            Object.keys(dic[sum_key][ma_key]).forEach(score_key => {
                res.push([sum_key, ma_key, score_key, dic[sum_key][ma_key][score_key]])
            })
        })
    })
    return res
}

function mergeData(a, b) {
    const res = cloneDeep(a)
    Object.keys(a).forEach(sum_key => {
        Object.keys(a[sum_key]).forEach(ma_key => {
            Object.keys(a[sum_key][ma_key]).forEach(score_key => {
                if (b[sum_key] && b[sum_key][ma_key] && b[sum_key][ma_key][score_key]) {
                    res[sum_key][ma_key][score_key] = a[sum_key][ma_key][score_key] + b[sum_key][ma_key][score_key]
                }
            })
        })
    })
    return res
}

function calcPercent(a, b) {
    const res = cloneDeep(a)
    Object.keys(a).forEach(sum_key => {
        Object.keys(a[sum_key]).forEach(ma_key => {
            Object.keys(a[sum_key][ma_key]).forEach(score_key => {
                if (b[sum_key] && b[sum_key][ma_key] && b[sum_key][ma_key][score_key]) {
                    res[sum_key][ma_key][score_key] = (a[sum_key][ma_key][score_key] / b[sum_key][ma_key][score_key] * 100).toFixed(3)
                }
            })
        })
    })
    return res
}

function matrixParseNumber(m) {
    return m.map(row => {
        return row.slice(0, 3).map(val => {
            return parseFloat(val.replace("sum_", "").replace("ma_", "").replace("_", ""))
        }).concat(parseFloat(row[3]))
    })
}

function getMaxInMatrix(dic) {
    // let TEMP_MAX = -Infinity
    // return innerFuc(dic)
    // function innerFuc(dic) {
    //     if (Object.prototype.toString.call(dic) == "[Object Object]") {
    //         Object.keys(dic).forEach(e => {
    //             return innerFuc(dic[e])
    //         })
    //     } else {
    //         if (e > TEMP_MAX) TEMP_MAX = e
    //     }
    // }
    let max = -Infinity
    dic.forEach(row => {
        if (row[3] > max)
            max = row[3]
    })
    return max
}