<template>
<div id="top-controls">
    <div class="container">
        <div class="timeline-controls">
            <button class="mdl-button mdl-button--fab mdl-button--colored ui-playButton"
                    id="play-pause-button" title="Run/Pause">
                <i class="material-icons">play_arrow</i>
                <i class="material-icons">pause</i>
            </button>
        </div>
        <div class="control">
            <span class="label">Epoch</span>
            <span class="value" id="iter-number"></span>
        </div>
        <div class="control ui-learningRate">
            <label for="learningRate">学习率</label>
            <div class="select">
                <select id="learningRate">
                    <option value="0.001">0.001</option>
                    <option value="0.003">0.003</option>
                    <option value="0.01">0.01</option>
                    <option value="0.03">0.03</option>
                    <option value="0.1">0.1</option>
                    <option value="0.3">0.3</option>
                    <option value="0.5">0.5</option>
                    <option value="1">1</option>
                    <option value="3">3</option>
                    <option value="10">10</option>
                </select>
            </div>
        </div>
        <div class="control ui-activation">
            <label for="activations">激活函数</label>
            <div class="select">
                <select id="activations">
                    <option value="relu">ReLU</option>
                    <option value="tanh">Tanh</option>
                    <option value="sigmoid">Sigmoid</option>
                    <option value="linear">Linear</option>
                    <option value="sinx">Sin(x)</option>
                </select>
            </div>
        </div>
        <div class="control ui-regularization">
            <label for="regularizations">正则化</label>
            <div class="select">
                <select id="regularizations">
                    <option value="none">None</option>
                    <option value="L1">L1</option>
                    <option value="L2">L2</option>
                </select>
            </div>
        </div>
    </div>
</div>
</template>

<script>
export default {
    name: "Train",
}
</script>
<style scoped>
/* Top Controls */
#top-controls {
    border-bottom: 1px solid #ddd;
    padding: 18px 0;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
    background: rgb(255, 255, 255);
}

@media (min-height: 700px) {
    #top-controls {
        padding: 24px 0;
    }
}

#top-controls .container {
    display: -webkit-box;
    display: -moz-box;
    display: -ms-flexbox;
    display: -webkit-flex;
    display: flex;
    /* -webkit-justify-content: space-betweenspace-between; */
    /* justify-content: space-between; */
    align-content: flex-start;
}

#top-controls .timeline-controls {
    display: -webkit-box;
    display: -moz-box;
    display: -ms-flexbox;
    display: -webkit-flex;
    display: flex;
    align-items: center;
    margin-right: 20px;
    /* width: 140px; */
}

#play-pause-button .material-icons {
    color: white;
    font-size: 36px;
    transform: translate(-18px, -12px);
}

#play-pause-button .material-icons:nth-of-type(2) {
    display: none;
}

#play-pause-button.playing .material-icons:nth-of-type(1) {
    display: none;
}

#play-pause-button.playing .material-icons:nth-of-type(2) {
    display: inherit;
}

#top-controls .control {
    flex-grow: 1;
    max-width: 100px;
    min-width: 80px;
    margin-left: 30px;
    margin-top: 6px;
}

#top-controls .control .label,
#top-controls .control label {
    color: #777;
    font-size: 13px;
    display: block;
    margin-bottom: 6px;
    font-weight: 300;
}

#top-controls .control .value {
    font-size: 24px;
    margin: 0;
    font-weight: 300;
}

#top-controls .control .select {
    position: relative;
}

#top-controls .control select {
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    display: block;
    background: none;
    border: none;
    border-radius: 0;
    padding: 6px 0;
    width: 100%;
    font-size: 14px;
    border-bottom: solid 1px #ccc;
    color: #333;
    outline: none;
}

#top-controls .control select:focus {
    border-bottom-color: #183D4E;
}

#top-controls .control .select::after {
    class: "material-icons";
    content: "arrow_drop_down";
    color: #999;
    font-family: 'Material Icons';
    font-weight: normal;
    font-style: normal;
    font-size: 18px;
    line-height: 1;
    letter-spacing: normal;
    text-transform: none;
    display: inline-block;
    white-space: nowrap;
    word-wrap: normal;
    direction: ltr;
    position: absolute;
    right: 0;
    top: 6px;
    pointer-events: none;
}

/* Buttons */

.mdl-button--fab.mdl-button--colored,
.mdl-button--fab.mdl-button--colored:hover,
.mdl-button--fab.mdl-button--colored:active,
.mdl-button--fab.mdl-button--colored:focus,
.mdl-button--fab.mdl-button--colored:focus:not(:active) {
    background: #183D4E;
}

</style>