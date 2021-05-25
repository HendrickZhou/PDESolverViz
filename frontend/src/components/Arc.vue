<template>
<div id="architecture">
<h4>网络结构</h4>
<ul style="list-style-type:none;">
    <li v-for="(node_num, index) in layers" :key="index"> 
        <div class="layer">
            <div class="entry">
            <div class="input-group">
                <button class="btn btn-secondary btn-remove input-group-prepend" v-on:click="delLayer(index)">删除层</button>
                <input type="number" class="form-control" name="numberOfNodes" step="1" v-model="node_num.value" min="1"/>
            </div>
        </div><p>第{{index + 1}}层</p>
        </div>
    </li>
</ul>
<div class="layer" style="padding-left:50px;">
    <div class="entry">
        <div class="input-group">
            <button class="btn btn-primary btn-add input-group-prepend" v-on:click="addLayer">增加层</button>
        </div>
    </div>
</div>

</div>
</template>

<script>
export default {
    name: 'Arc',
    data() {
        return {
            layers : [
                {"value": 10},
                {"value": 5},
                {"value": 2}
            ],
        }
    },
    methods: {
        addLayer() {
            this.layers.push({"value":3});
        },
        delLayer(index) {
            this.layers.splice(index, 1);
        },
        getLayer() {
            var layers_arr = [];
            for(const layer of this.layers){
                layers_arr.push(layer["value"])
            }
            return layers_arr
        }
    },
}
</script>

<style scoped>
h4 {
    color: white;
}
p {
    color: white;
}
#architecture .layer {
    display: flex;
    flex-direction: row;
    /* justify-content: space-between; */
}
#architecture {
    display: flex;
    flex-direction: column;
    text-align: center;
}
</style>