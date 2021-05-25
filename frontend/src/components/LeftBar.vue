<template>
<div id="l-nav-bar">
    <router-link to="/geometry" @click.native="geo">
        <div class="tab" v-bind:style="{border_left: border_style_1}">
            <b-icon icon="intersect" v-bind:style="{color: geo_color}">Geometry</b-icon>
        </div>
    </router-link>
    <router-link to="/pde" @click.native="pde">
        <div class="tab" v-bind:style="{border_left: border_style_2}"><b-icon icon="braces" v-bind:style="{color: pde_color}">PDE</b-icon></div>
    </router-link>
    <router-link to="/nn" @click.native="nn">
        <div class="tab" v-bind:style="{border_left: border_style_3}"><b-icon icon="shuffle" v-bind:style="{color: nn_color}">NN</b-icon></div>
    </router-link>
    
    
</div>
</template>

<script>
export default {
    name: 'LeftBar',
    data() {
        return {
            geo_color : 'rgb(112, 112, 112)',
            pde_color : 'rgb(112, 112, 112)',
            nn_color : 'rgb(112, 112, 112)',
        }
    },
    methods: {
        geo() {
            this.geo_color = "white";
            this.pde_color = "rgb(112, 112, 112)";
            this.nn_color = "rgb(112, 112, 112)";
        },
        pde() {
            this.pde_color = "white";
            this.geo_color = "rgb(112, 112, 112)";
            this.nn_color = "rgb(112, 112, 112)";
        },
        nn() {
            this.nn_color = "white";
            this.geo_color = "rgb(112, 112, 112)";
            this.pde_color = "rgb(112, 112, 112)";
        },
    },
};
</script>

<style>
#l-nav-bar {
    /* flex:0; */
    width: 60px;
    background-color: rgb(51, 45, 45);
    display: flex;
    flex-direction: column;;
}

.tab {
    width: 100%;
    height: 60px;
    padding-left: 20px;
    padding-top: 20px;
    /* border-left: 2px solid white; */

}

.b-icon{
    color: rgb(112, 112, 112);
}

.b-icon:hover{
    color: white
}
</style>>
