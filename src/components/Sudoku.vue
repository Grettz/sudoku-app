<template>
    <div id='sudoku'>
        <SudokuBoard />
    </div>
</template>

<script>
import SudokuBoard from './SudokuBoard.vue';

export default {
    name: 'Sudoku',
    components: {
        SudokuBoard
    }
}

</script>

<style scoped>

</style>