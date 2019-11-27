<template>
    <div id="app">
        <h1>Sudoku</h1>
        <Sudoku />
    </div>
</template>

<script>
import Sudoku from './components/Sudoku.vue';

export default {
    name: 'app',
    components: {
        Sudoku
    },
}
</script>

<style scoped>
    #app { width: fit-content; margin: 20px auto 20px; }
</style>