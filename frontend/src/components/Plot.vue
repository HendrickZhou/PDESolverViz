<template>
<div id="wrapper">
<div id="plot"></div>
</div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';
import * as tfvis from '@tensorflow/tfjs-vis';

export default {
    name: "Plot",
    data() {
        return {
            charts: '',
            timer: '',
            valueList: [
                [ 0, 0 ],
            ],
        }
    },
    methods: {
        initChart() {
            this.charts = echarts.init(document.getElementById('plot'));
            this.charts.setOption({
                height: '180',
                width: 'auto',
                title: {
                    left: 'center',
                    text: '训练Loss曲线'
                },
                visualMap: [{
                    show: false,
                    type: 'continuous',
                    seriesIndex: 0,
                    min: 0,
                    max: 400
                },],
                grid:{
                backgroundColor: 'white',
                show: true
                },
                tooltip: {
                    trigger: 'axis',
                    formatter: function (params) {
                        params = params[0];
                        var date = new Date(params.name);
                        return date.getDate() + '/' + (date.getMonth() + 1) + '/' + date.getFullYear() + ' : ' + params.value[1];
                    },
                    axisPointer: {
                        animation: false
                    }
                },
                xAxis: {
                    splitLine: {
                        show: false
                    }
                },
                yAxis: {
                    type: 'value',
                    boundaryGap: [0, '100%'],
                    splitLine: {
                        show: false
                    }
                },
                series: [{
                    type: 'line',
                    showSymbol: false,
                    data: this.valueList,
                    hoverAnimation: false,
                },],
                animation: false
            })
        },

        // onNewData() {
        //     this.timer = window.setInterval(this.fetchLossData, 5); // 5ms 12fps
        // },
        fetchLossData(){
            const path = 'http://localhost:5000/getLoss';
            axios.get(path)
            .then((res) => {
                // console.log(res);
                // if(res.flag == "over"){
                //     window.clearInterval(this.timer);
                // }
                // else {
                    // append new_data
                    // console.log(this.valueList)
                    this.valueList = this.valueList.concat(res.data.loss)
                    // console.log(this.valueList)
                    this.charts.setOption({
                        series: [{
                            data: this.valueList
                        }]
                    });
                // }
            })
            .catch((error) => {
                console.error(error);
            });
        },

    },
    mounted(){
        this.initChart();
    }

}
</script>

<style>
#wrapper {
    width: 100%;
    height: 40%;
}
#plot {
    width: 100%;
    height: 100%;
}
</style>