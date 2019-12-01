import { cloneDeep } from "lodash";

const opt = {
    backgroundColor: '#21202D',
    legend: {
        data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30'],
        inactiveColor: '#777',
        textStyle: {
            color: '#fff'
        }
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            animation: false,
            type: 'cross',
            lineStyle: {
                color: '#376df4',
                width: 2,
                opacity: 1
            }
        },
        // formatter: '{b0}: {c0}<br />{b1}: {c1}'
    },
    xAxis: [{
        type: 'category',
        // data: dates,
        axisLine: { lineStyle: { color: '#8392A5' } }
    },
    {
        type: "category",
        axisLine: { lineStyle: { color: '#8392A5' } },
        gridIndex: 1
    },
    {
        type: "category",
        axisLabel: { show: false },
        gridIndex: 2
    }
    ],
    yAxis: [{
        scale: true,
        axisLine: { lineStyle: { color: '#8392A5' } },
        splitLine: { show: false }
    },
    {
        id: "sumY",
        scale: true,
        axisLine: { lineStyle: { color: '#8392A5' } },
        splitLine: { show: false },
        gridIndex: 1
    },
    {
        scale: true,
        axisLine: { show: false, onZeroAxisIndex: "sumY" },
        axisLabel: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },

        gridIndex: 2,

    }
    ],
    grid: [
        // k 线区域
        {
            left: '5%',
            right: '5%',
            height: '50%'
        },
        // 胡立阳打分结果
        {
            left: '5%',
            right: '5%',
            bottom: '20%',
            height: '15%'
        },
        // 胡立阳盈利结果
        {
            left: '5%',
            right: '5%',
            bottom: '20%',
            height: '15%'
        }
    ],
    dataZoom: [{
        textStyle: {
            color: '#8392A5'
        },
        startValue: 200,
        endValue: 250,
        handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
        handleSize: '80%',
        dataBackground: {
            areaStyle: {
                color: '#8392A5'
            },
            lineStyle: {
                opacity: 0.8,
                color: '#8392A5'
            }
        },
        xAxisIndex: [0, 1, 2],
        handleStyle: {
            color: '#fff',
            shadowBlur: 3,
            shadowColor: 'rgba(0, 0, 0, 0.6)',
            shadowOffsetX: 2,
            shadowOffsetY: 2
        }
    }, {
        type: 'inside'
    }],
    animation: false,
    series: [
        {
            type: 'candlestick',
            name: '日K',
            itemStyle: {
                normal: {
                    color: '#FD1050',
                    color0: '#0CF49B',
                    borderColor: '#FD1050',
                    borderColor0: '#0CF49B'
                }
            }
        },
    ]
};


export default function ({
    data,
    daySum,
    ma,
}) {
    const sortedData = cloneDeep(data)
    sortedData.sort(compareDate)

    // X 轴
    opt.xAxis.forEach(item => {
        item.data = sortedData.map(row => row['日期'])
    })

    const init_days = 40
    opt.dataZoom[0].startValue = sortedData.length - init_days
    opt.dataZoom[0].endValue = sortedData.length

    opt.series = []

    // 日 K
    opt.series.push({
        type: 'candlestick',
        name: '日K',
        data: sortedData.map(row => [row['开盘价'], row['收盘价'], row['最低价'], row['最高价']]),
        itemStyle: {
            normal: {
                color: '#FD1050',
                color0: '#0CF49B',
                borderColor: '#FD1050',
                borderColor0: '#0CF49B'
            }
        }
    })

    // 胡立阳打分数据
    opt.legend.data = Object.keys(sortedData[0]).map(key => {
        if (key === `sum_${daySum}`)
            return key
    }).filter(key => key != undefined)
    opt.series = opt.series.concat(opt.legend.data.map(key => {
        return {
            name: key,
            type: "line",
            data: sortedData.map(row => row[key]),
            smooth: true,
            xAxisIndex: 1,
            yAxisIndex: 1,
        }
    }))
    let sum_max = opt.series[1].data.reduce((prev, curr) => {
        if (curr > prev) return curr
        return prev
    }, -Infinity)
    let sum_min = opt.series[1].data.reduce((prev, curr) => {
        if (curr < prev) return curr
        return prev
    }, Infinity)
    let sum_abs_max = Math.max(Math.abs(sum_max), Math.abs(sum_min))
    opt.yAxis[1].max = Math.abs(sum_abs_max)
    opt.yAxis[1].min = -1 * Math.abs(sum_abs_max)

    // 增长 / 减少的价格
    opt.series = opt.series.concat({
        name: "priceChange",
        type: "bar",
        data: sortedData.map((row, index) => {
            if (!index) return 0
            return parseInt((row['收盘价'] - sortedData[index - 1]['收盘价']) * 100) / 100
        }),
        xAxisIndex: 2,
        yAxisIndex: 2,
        label: {
            show: false
        }
    })
    let delta_max = opt.series[2].data.reduce((prev, curr) => {
        if (curr > prev) return curr
        return prev
    }, -Infinity);
    let delta_min = opt.series[2].data.reduce((prev, curr) => {
        if (curr < prev) return curr
        return prev
    }, Infinity)
    let delta_abs_max = Math.max(Math.abs(delta_max), Math.abs(delta_min))
    opt.yAxis[2].max = Math.abs(delta_abs_max)
    opt.yAxis[2].min = -1 * Math.abs(delta_abs_max)

    opt.series = opt.series.concat(ma.map(val => {
        return {
            name: `MA${val}`,
            type: 'line',
            data: calculateMA(val, sortedData),
            smooth: true,
            lineStyle: {
                normal: {opacity: 0.5}
            }
        }
    }))

    return opt
}

function compareDate(d1, d2) {
    // let d1 = new Date(a['日期']);
    // let d2 = new Date(b['日期']);
    // return d1.getTime() < d2.getTime();
    return parseInt(d1['日期'].split("-").join("")) - parseInt(d2['日期'].split("-").join(""))
}

function calculateMA(dayCount, data) {
    var result = [];
    for (var i = 0, len = data.length; i < len; i++) {
        if (i < dayCount) {
            result.push('-');
            continue;
        }
        var sum = 0;
        for (var j = 0; j < dayCount; j++) {
            sum += data[i - j]['收盘价'];
        }
        result.push(+(sum / dayCount).toFixed(3));
    }
    return result;
}