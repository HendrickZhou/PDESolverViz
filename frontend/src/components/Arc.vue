<template>
<div id="architecture">
<h4>Architecture</h4>
<div class="layer">
<div class="entry">
    <div class="input-group">
        <button class="btn btn-secondary btn-remove input-group-prepend"><span class="fa fa-minus"></span></button>
        <input type="number" class="form-control" name="numberOfNodes" step="1" value="16" />
    </div>
</div>
<p>第1层</p>
</div>
<div class="layer">
<div class="entry">
    <div class="input-group">
        <button class="btn btn-secondary btn-remove input-group-prepend"><span class="fa fa-minus"></span></button>
        <input type="number" class="form-control" name="numberOfNodes" step="1" value="12" />
    </div>
</div>
<p>第2层</p>
</div>
<div class="layer">
<div class="entry">
    <div class="input-group">
        <button class="btn btn-primary btn-add input-group-prepend"><span class="fa fa-plus"></span></button>
        <input type="number" class="form-control" name="numberOfNodes" step="1"/>
    </div>
</div>
<p></p>
</div>

</div>
</template>

<script>
export default {
    name: 'Arc'
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