<template>
<div id="nn">
    <Train></Train>
    <Arc></Arc>
    <div class="splitter"></div>
</div>
</template>

<script>
// import MenuIcon from 'vue-material-design-icons/Menu.vue';
import 'vue-material-design-icons/styles.css';
import Train from '@/components/Train.vue';
import Arc from '@/components/Arc.vue';

export default {
    name: "NN",
    components: {
        // MenuIcon,
        Train,
        Arc,
    }
}
</script>

<style scoped>
.splitter {
    height: 3px;
    width: 70%;
    background-color: rgb(51, 45, 45);
}
#nn {
    width: 50%;
    display: flex;
    flex-direction: column;
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