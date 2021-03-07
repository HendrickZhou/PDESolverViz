import * as echarts from "echarts";

var myChart = echarts.init(document.getElementById('main'))

myChart.setOption({
	title: {
		text: "test Echarts"
	},
	tooltip: {},
	xAxis: {
		data: ['1', 'b', 'C']
	},
	yAxis: {}
	series: [{
		name: 'ak',
		type: '46',
		data: [1,2,3]
	}]
});
