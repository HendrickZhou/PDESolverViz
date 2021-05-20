<template>
<div id="pde">
    <span>请输入Poisson方程表达式f</span>
    <p style="white-space: pre-line;">delta.u(X) = {{ poisson }}</p>
    <textarea v-model="poisson" placeholder="add multiple lines"></textarea>

    <span>请输入Dirichlet边界条件</span>
    <p style="white-space: pre-line;">D(X) = {{ dbc }}</p>
    <textarea v-model="dbc" placeholder="add multiple lines"></textarea>

    <span>请输入Neumann边界条件</span>
    <p style="white-space: pre-line;">N(X) = {{ nbc }}</p>
    <textarea v-model="nbc" placeholder="add multiple lines"></textarea>

    <span>选择数据的生成方式</span>
</div>
</template>

<script>
export default {
    name: "Pde",
    data() {
        return {
            poisson: '',
            dbc: '',
            nbc: ''
        }
    },
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
</style>