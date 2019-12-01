import { cloneDeep } from "lodash";

const opt = { 
    "tooltip": { 
        "position": "top" 
    }, 
    "animation": true, 
    "grid": { 
        "height": "70%", 
    }, 
    "xAxis": { 
        "type": "category", 
        "data": [], 
        "splitArea": { "show": true }
    }, 
    "yAxis": { 
        "type": "category", 
        "data": [],
        "splitArea": 
        { 
            "show": true 
        }
    }, 
    "visualMap": { 
        "min": 0, 
        "max": 10, 
        "calculable": true, 
        "orient": "horizontal", 
        "left": "center", 
        "bottom": "5%" 
    }, 
    "series": [
        { 
            "name": "Punch Card", 
            "type": "heatmap", 
            "data": [[]],
            "label": { 
                "normal": { 
                    "show": true 
                } 
            }, 
            "itemStyle": { 
                "emphasis": { 
                    "shadowBlur": 10, 
                    "shadowColor": "rgba(0, 0, 0, 0.5)" 
                } 
            } 
        }] 
    }


export default function ({
    dataPlus,
    dataReduce,
    currentResType
}) {
    const dataSum = mergeMatrix(dataPlus, dataReduce)

    let heatmapData = []
    if (currentResType === 0) heatmapData = cloneDeep(dataPlus) 
    if (currentResType === 1) heatmapData = cloneDeep(dataReduce)
    
    opt.xAxis.data = Object.keys(dataPlus)
    opt.yAxis.data = Object.keys(heatmapData[Object.keys(heatmapData)[0]])

    const max = Object.keys(dataSum[Object.keys(dataPlus)[0]]).map(key => dataSum[Object.keys(dataPlus)[0]][key]).sort((a,b) => b-a)[0]
    opt.visualMap.max = max
    let resData = []
    opt.xAxis.data.forEach(x_key => {
        opt.yAxis.data.forEach(y_key => {
            resData.push([x_key, y_key, heatmapData[x_key][y_key]])
        })
    })
    opt.series[0].data = resData;

    return opt
}


function mergeMatrix(m1,m2){
    let x = Object.keys(m1)
    let y = Object.keys(m1[x[0]])

    let res = {}
    x.forEach(x_key => {
        res[x_key] = {}
        y.forEach(y_key => {
            res[x_key][y_key] = m1[x_key][y_key] + m2[x_key][y_key]
        })
    })
    return res
}