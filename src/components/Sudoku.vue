<template>
    <div id='sudoku'>
        <h1>Sudoku</h1>
        <SudokuBoard />
    </div>
</template>

<script>
import SudokuBoard from './SudokuBoard.vue';

export default {
    name: 'Sudoku',
    components: {
        SudokuBoard
    },
    data: function() {
        return {
            sudoku: SudokuBoard.sudoku
        }
    }
}

</script>

<style scoped>
    #sudoku {
        padding: 30px;
    }
</style>