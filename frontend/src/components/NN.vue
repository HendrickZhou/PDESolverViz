<template>
<div id="nn">
   <div id="setting"> 
    <Arc ref="arc"></Arc>
    <div class="splitter"></div>
    <h4>参数</h4>
    <div class="item-wrapper">
        <div id="lr">
            <input v-model="lr" placeholder="学习率" class="item">
            <span>学习率:{{ lr }}</span>
        </div>
        <div id="dropout">
            <input v-model="dropout" placeholder="dropout率" min="0" max="1" class="item">
            <span>dropout率:{{ dropout }}</span>
        </div>
        <div id="act">
            <select v-model="act" class="item">
            <option disabled value="">请选择</option>
            <option v-for="option in act_ops" :key="option">
              {{ option }}
            </option>
            </select>
            <span>选择激活函数: {{ act }}</span>
        </div>
        <div id="reg">
            <select v-model="reg">
            <option disabled value="">请选择</option>
            <option v-for="option in reg_ops" v-bind:key="option.text">
              {{ option.value }}
            </option>
            </select>
            <span>选择正则化方法: {{ reg }}</span>
        </div>
        <div id="init">
            <select v-model="init" class="item">
            <option disabled value="">请选择</option>
            <option v-for="option in init_ops" :key="option">
              {{ option }}
            </option>
            </select>
            <span>选择初始化方法: {{ init }}</span>
        </div>
        <div id="batch">
            <select v-model="batch" class="item">
            <option disabled value="">请选择</option>
            <option v-for="option in batch_ops" v-bind:key="option.text">
              {{ option.value }}
            </option>
            </select>
            <span>选择归一化方法: {{ batch }}</span>
        </div>
        <div id="opt">
            <select v-model="opt" class="item">
            <option disabled value="">请选择</option>
            <option v-for="option in opt_ops" v-bind:key="option.text">
              {{ option.value }}
            </option>
            </select>
            <span>选择优化器: {{ opt }}</span>
        </div>
        <div id="loss">
            <select v-model="loss" class="item">
            <option disabled value="">请选择</option>
            <option v-for="option in loss_ops" v-bind:key="option.text">
              {{ option.value }}
            </option>
            </select>
            <span>选择损失函数: {{ loss }}</span>
        </div>

        <div id="domain_dp">
            <input v-model="domain_dp" placeholder="数据量" min="0" class="item">
            <span>计算域中的数据集大小:{{ domain_dp }}</span>
        </div>
        <div id="bc_dp">
            <input v-model="bc_dp" placeholder="数据量" min="0" class="item">
            <span>边界上的数据集大小:{{ bc_dp }}</span>
        </div>
        <div id="test_dp">
            <input v-model="test_dp" placeholder="数据量" min="0" class="item">
            <span>测试集大小:{{ test_dp }}</span>
        </div>
        <div id="dist">
            <select v-model="dist" class="item">
            <option disabled value="">请选择</option>
            <option v-for="option in dist_ops" :key="option">
              {{ option }}
            </option>
            </select>
            <span>选择数据采样分布: {{ dist }}</span>
        </div>
    </div>
    <br>
   </div>

<div class="splitter"></div>
<div id='status-bar'>
    <b-button type='submit' size="sm" v-on:click="saveAndTrain"><b-icon icon="play"></b-icon></b-button>
    <div class="title">开始训练</div>
</div>

<Plot></Plot>

</div>
</template>

<script>
// import MenuIcon from 'vue-material-design-icons/Menu.vue';
import 'vue-material-design-icons/styles.css';
// import Train from '@/components/Train.vue';
import Arc from '@/components/Arc.vue';
import Plot from '@/components/Plot.vue';
import axios from 'axios';

export default {
    name: "NN",
    data() {
        return {
            lr: 1,
            act: "relu",
            reg: "l1",
            init: "LeCun normal",
            batch: "None",
            dropout: 0,
            opt: "adam",
            loss: "MSE",
            domain_dp: 1000,
            bc_dp: 100,
            test_dp: 1200,
            dist: "sobol",
            act_ops: ["relu", "elu", "selu", "sigmoid", "tanh", "sin", "swish"],
            reg_ops: [
                {value: "l1" , text: "L1正则化"},
                {value: "l2", text : "L2正则化"},
                {value: "l1+l2", text : "L1+L2正则化"},
                {value: "None", text : "不使用正则化"},
            ],
            init_ops: [
                "zeros", "He normal", "LeCun normal", "Glorot normal","Orthogonal"
            ],
            batch_ops: [
                {value: "before" , text: "激活函数前使用"},
                {value: "after", text : "激活函数后使用"},
                {value: "None", text : "不使用"},
            ],
            opt_ops: [
                {value: "sgd", text: "SGD"},
                {value: "adam", text: "Adam"},
                {value: "sgdnesterov", text: "SGD-Nesterov"},
                {value: "adagrad", text: "Adagrad"},
                {value: "adadelta", text: "Adadelta"},
                {value: "rmsprop", text: "RmsProp"},
            ],
            loss_ops: [
                {value: "MAE", text: "mean absolute error"},
                {value: "MSE", text: "mean squared error"},
                {value: "MAPE", text: "mean absolute percentage error"},
                {value: "softmax cross entropy", text: "softmax cross entropy"},
                {value: "zero", text: "zero"},
            ],
            dist_ops: [
                "uniform", "pseudo", "sobol" 
            ]
        }
    },
    methods: {
        saveAndTrain() {
            var layer_arr = this.$refs.arc.getLayer();
            const path = 'http://localhost:5000/submitNN';
            var content = {
                "arch": layer_arr,
                "lr": this.lr,
                "act": this.act,
                "reg": this.reg,
                "init": this.init,
                "batch": this.batch,
                "dropout": this.dropout,
                "opt": this.opt,
                "loss": this.loss,
                "n_domain": this.domain_dp,
                "n_bc": this.bc_dp,
                "n_test": this.test_dp,
                "dist": this.dist,
            }
            axios.post(path, content)
            .then((res) => {
                console.log(res);
            })
            .catch((error) => {
                console.error(error);
            });
        },
    },
    components: {
        // MenuIcon,
        // Train,
        Arc,
        Plot,
    }
}
</script>

<style scoped>
#setting {
    width: 100%;
    height: 60%;
    overflow-y: scroll;
}

.item-wrapper {
    padding-left: 50px;
}
.item {
    max-width: 100px;
}

h4 {
    color: white;
    text-align: center;
}
p {
    color: white;
}
#status-bar {
    height: 30px;
    display: flex;
    flex-direction: row;
    align-items:space-between;
}
.splitter {
    height: 3px;
    width: 100%;
    background-color: rgb(51, 45, 45);
}
#nn {
    width: 50%;
    display: flex;
    flex-direction: column;;
    align-items: stretch;
}


/* Hover card */
#hovercard {
    display: none;
    position: absolute;
    padding: 5px;
    border: 1px solid #aaa;
    z-index: 1000;
    background: #fff;
    cursor: default;
    border-radius: 5px;
    left: 240px;
    width: 170px;
    top: -20px;
}

#hovercard input {
    width: 60px;
}

/* Material Overrides */

/* Checkbox */

.mdl-checkbox__box-outline {
    border-color: rgba(0, 0, 0, 0.5);
}

.mdl-checkbox.is-checked .mdl-checkbox__tick-outline {
    background-color: #183D4E;
}

.mdl-checkbox.is-checked .mdl-checkbox__tick-outline {
    background-color: #183D4E;
}

.mdl-checkbox.is-checked .mdl-checkbox__box-outline {
    border-color: #183D4E;
}

.mdl-checkbox__ripple-container .mdl-ripple {
    background-color: #183D4E;
}

/* Slider */

#main-part .mdl-slider.is-upgraded {
    color: #183D4E;
}

#main-part .mdl-slider__background-lower {
    background-color: #183D4E;
}

#main-part .mdl-slider.is-upgraded::-webkit-slider-thumb {
    background-color: #183D4E;
}

#main-part .mdl-slider.is-upgraded::-moz-range-thumb {
    background-color: #183D4E;
}

#main-part .mdl-slider.is-upgraded::-ms-thumb {
    background-color: #183D4E;
}

#main-part .mdl-slider.is-upgraded.is-lowest-value::-webkit-slider-thumb {
    border-color: #183D4E;
}

#main-part .mdl-slider.is-upgraded.is-lowest-value::-moz-range-thumb {
    border-color: #183D4E;
}

/* Keep grey focus circle for non-start values */
#main-part .mdl-slider.is-upgraded:focus:not(:active)::-webkit-slider-thumb {
    box-shadow: 0 0 0 10px rgba(0, 0, 0, 0.12);
}

/* Toolboxes */
span.title {
    font-weight: bold;
    font-size: 16px;
}

h3.popover-header {
    margin: 0px 0;
    background-color: #f1f1f1 !important;
}

a.info {
    vertical-align: bottom;
    position:absolute; /* Anything but static */
    width: 1.2em;
    height: 1.2em;
    text-indent: -9999em;
    display: inline-block;
    color: white;
    font-weight:normal;
    font-size:0.9em;
    line-height:1em;
    background-color: #c6c6c6;
    margin-left: .25em;
    margin-top: 0.2em;
    -webkit-border-radius:.75em;
    -moz-border-radius:.75em;
    border-radius:.7em;
}
a.info:hover {
    background-color: #a5a5a5;
    cursor: pointer;
}
a.info:before {
    content:"?";
    position: absolute;
    top: .2em;
    color: white;
    left:0;
    text-indent: 0;
    display:block;
    width:1.15em;
    text-align:center;
}

.popover{
    max-width: 30%; /* Max Width of the popover (depending on the container!) */
}


/* Feedback button */
#extra-info .basic-button {
    font-family: "Roboto", "Helvetica", "Arial", sans-serif;
    margin-top: 10px;
    margin-bottom: 25px;
    height: 34px;
    width: 130px;
    margin-right: 0;
    display: block;
    border: none;
    color: rgba(0, 0, 0, 0.6);
    background: rgba(0, 204, 102, .3);
    border-radius: 3px;
    padding: 5px;
    font-size: 12px;
    text-transform: uppercase;
    font-weight: 500;
    outline: none;
    transition: background 0.3s linear;
    cursor: pointer;
}

#extra-info .basic-button:hover {
    background: rgba(0, 204, 102, .6);
    color: rgba(0, 0, 0, 0.7);
}

#extra-info .basic-button:focus {
    background: rgba(0, 204, 102, .7);
    color: rgba(0, 0, 0, 0.7);
}

#extra-info .basic-button:active {
    background: rgba(0, 204, 102, 1);
    color: rgba(0, 0, 0, 0.7);
}
</style>