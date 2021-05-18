<template>
<div id="main">
    <!--topbar-->
    <div id="topbar">PDESolver</div>
	<!--col-based content-->
	<div id="content">
		<!--left nav bar-->
        <LeftBar></LeftBar>
		<!--打开默认是explorer + 说明-->
		<!--选择完project后，默认展开editor+graph-->
		<!--除此外的组合：PDE builder+graph; NN+graph; 或者单独graph+info tab-->
		<!--explorer+spec-->
		<!-- <div id="explorer"></div>
		<div class="v-handler"></div>
		<div id="spec"></div> -->

		<!--editor+equation+nn-->
		<Editor></Editor>
		<!--equation-->
		<div id="equation"></div>
		<!--nn-->
		<div id="nn"></div>

		<!--graph-->
		<VDrag></VDrag>
        <Graph></Graph>
	</div>

	<!--bottom info bar-->
	<div id="bt-info-bar"></div>
</div>
</template>

<script>
import LeftBar from '@/components/LeftBar.vue';
import Editor from '@/components/Editor.vue';
import Graph from '@/components/Graph.vue';
import VDrag from '@/components/drag/VDrag.vue';
// import axios from 'axios';

export default {
    name: 'Studio',
    components: {
        LeftBar,
        Editor,
        Graph,
        VDrag,
    },

};
</script>

<style>
#main {
    position: absolute;
    display: flex;
    flex-direction: column;
    align-content: space-between;
    height: 100vh;
    width: 100vw;
}
#topbar {
    height: 25px;
    width: 100%;
}
#content {
    flex: 1;
    height: 100%;
    width: 100%;
    flex-direction: row;
    display: flex;
}
#bt-info-bar {
    height: 25px;
    width: 100%;
}

#topbar {
    background-color: rgb(53, 41, 41);
    color:#fff;
}

#content {
    background-color: rgb(51, 27, 27);

    display: flex;
    flex-direction: row;
    align-items: stretch;
    justify-content: space-between;
}

#explorer {
    width: 50%;
    background-color: rgb(240, 216, 216);
}
#spec {
    width: 50%;
    background-color: rgb(185, 80, 80);
}

#bt-info-bar {
    background-color: rgb(98, 98, 199);
}
</style>
