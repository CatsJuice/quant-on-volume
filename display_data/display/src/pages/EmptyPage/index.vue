<template>
    <div id="not-found">
        <h2>404 NOT FOUND</h2>
        <hr>
        <span>Change Code And Try Again</span>
    </div>
</template>

<script>
export default {
    
}
</script>

<style lang="less" scoped>
#not-found {
    width: 30%;
    margin: 0 auto;
    // display: flex;
    padding: 120px 100px;
    text-align: center;
    font-size: 1rem;
    color: #bdbdbd;
    
    hr {
        margin: 10px;
        transform: scaleY(0.5);
    }
    h2 {
        color: #505050;
    }
    
}
</style>