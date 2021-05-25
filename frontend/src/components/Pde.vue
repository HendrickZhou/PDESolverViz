<template>
<div id="pde">
    <span>请输入Poisson方程表达式f</span>
    <p style="white-space: pre-line;">delta.u({{ var_names }}) = {{ poisson_main() }}</p>
    <textarea v-model="poisson" placeholder="add multiple lines"></textarea>

    <span>请输入Dirichlet边界条件</span>
    <p style="white-space: pre-line;">D({{var_names}}) = {{ dbc }}</p>
    <textarea v-model="dbc" placeholder="add multiple lines"></textarea>

    <span>请输入Neumann边界条件</span>
    <p style="white-space: pre-line;">N({{var_names}}) = {{ nbc }}</p>
    <textarea v-model="nbc" placeholder="add multiple lines"></textarea>

    <br>
    <br>
    <div id='status-bar'>
        <b-button type='submit' size="sm" v-on:click="savePde"><b-icon icon="play"></b-icon></b-button>
        <div class="title">保存方程</div>
    </div>
</div>
</template>

<script>
import axios from 'axios';
export default {
    name: "Pde",
    data() {
        return {
            poisson: '',
            var_names: '',
            poisson_body: '',
            dbc: '',
            nbc: ''
        }
    },
    methods: {
        savePde() {
            const path = 'http://localhost:5000/submitPDE';
            var content = {
                "var_str" : this.var_names,
                "poisson" : this.poisson_body,
                "dbc" : this.dbc,
                "nbc" : this.nbc,
            }
            axios.post(path, content)
            .then((res) => {
                console.log(res);
                alert("方程构建成功")
            })
            .catch((error) => {
                console.error(error);
            });
        },
        poisson_main() {
            var split = this.poisson.split(',');
            var idx1 = 0;
            var idx2 = 0;
            for(let i = 0; i < this.poisson.length; i++) {
                if(this.poisson[i] == '{'){
                    idx1 = i
                }
                if(this.poisson[i] == '}') {
                    idx2 = i
                }
            }
            this.var_names = this.poisson.substring(idx1+1,idx2);
            this.poisson_body = this.poisson.substring(idx2+2);
            return this.poisson.substring(idx2+2);
        }
    }
}
</script>

<style scoped>
#pde {
    color: white;
    width: 50%;
    display: flex;
    flex-direction: column;
    align-items: stretch;
}

#status-bar {
    height: 30px;
    display: flex;
    flex-direction: row;
    align-items:space-between;
}
</style>