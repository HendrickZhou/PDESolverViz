<template>
<div id="plot"></div>
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
            sample: [
                { index: 0, value: 50 },
                { index: 1, value: 100 },
                { index: 2, value: 150 },
            ],
        }
    },
    methods: {
        sampleViz() {
            tfvis.render.linechart(document.getElementById('plot'), this.sample, {width:400});
        },
        initLine(id) {
            this.charts = echarts.init(document.getElementById(id))
            this.charts.setOption({
                title: {
                    text: 'Dynamic data + time axis'
                },
                tooltip: {
                    trigger: 'axis',
                    formatter: function (params) {
                        params = params[0]
                        return params.value[0] + ' : ' + params.value[1]
                    },
                    axisPointer: {
                        animation: false
                    }
                },
                xAxis: {
                    type: 'time',
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
                animation: false
            })
        },
    },
    mounted(){
        // this.$nextTick(function() {
        //     this.initLine('plot')
        //     this.charts.setOption({
        //         series : [
        //             {
        //                 name: 'Analog data 0',
        //                 type : 'line',
        //                 showSymbol : false,
        //                 hoverAnimation : false,
        //                 data : [['2018-01-02', '3'],['2018-01-05', '4']]
        //             }
        //         ]
        //     })
            
        //     setTimeout(() => {
        //         this.charts.appendData({
        //             seriesIndex:0,
        //             data : [['2018-01-03', '1'],['2018-01-07', '2']]
        //         })
        //     },2000)
            
        //     setTimeout(() => {
        //         this.charts.resize();    
        //     },4000)

        //     setTimeout(() => {
        //         this.charts.setOption({
        //             series : [
        //                 {},
        //                 {
        //                                                         name: 'Analog data 1',
        //                     type : 'line',
        //                     showSymbol : false,
        //                     hoverAnimation : false,
        //                     data : [['2018-01-02', '5'],['2018-01-05', '10']]
        //                 }
        //             ]
        //         })
        //         this.charts.appendData({
        //             seriesIndex:1,
        //             data : [['2018-01-03', '11'],['2018-01-10', '2']]
        //         })
        //     },6000) 
        //     setTimeout(() => {
        //         this.charts.resize();    
        //     },8000)
        // })
        this.sampleViz()
    }

}
</script>

<style scoped>
#plot {
    width: 100%;
    height: 40%;
}
</style>