<template>
    <div id='sudoku'>
        <table id='grid' class='disable-select' draggable='false'>
            <tr v-for='(row, i) in sudoku' :key='row.id' :id='"r-" + i'>
                <td v-for='(cell, j) in row' :key='cell.id' :id='"c-" + j' class='cell'
                    :class='{ highlight: is_cell_selected(i, j) }'
                    @click="toggle_cell_highlight(i, j)">
                        {{ sudoku[i][j] }}
                </td>
            </tr>
        </table>
    </div>
</template>

<script>
export default {
    name: 'Sudoku',
    data: function() {
        return {
            sudoku: [],
            selected_cells: []
        }
    },
    methods: {
        empty_sudoku(rows=9, columns) {
            // TODO add parameters for custom number of blocks in the row and column, e.g. rows=6, columns=6, h-blocks=2, v-blocks=3 creates 2x3 blocks and values 1-6
            if (columns == undefined) {
                columns = rows;
            }
            if (rows % 3 > 0 || columns % 3 > 0) {
                console.log('Error: rows and columns must be a multiple of 3.')
                return
            }
            // Create sudoku grid
            let sudoku = []
            for(let i=0; i<rows; i++) {
                sudoku[i] = new Array(columns)
                // Fill cells with 0s
                for(let j=0; j<columns; j++) {
                    sudoku[i][j] = '';
                }
            }
            return sudoku
        },
        toggle_cell_highlight(i, j) {
            // Find if selected cell is already highlighted
            let cell_index = this.selected_cells.findIndex(cell => cell.i == i && cell.j == j)
            if(cell_index >= 0) {

                this.selected_cells.splice(cell_index, 1)
            } else {
                let coord = {"i": i, "j": j}
                this.selected_cells.push(coord)
            }
        },
        is_cell_selected(i, j) {
            let cell_index = this.selected_cells.findIndex(cell => cell.i == i && cell.j == j)
            if(cell_index > -1) {
                return true
            }
            return false
        },
        runfunction(e) {
            console.log('up')
        }
    },
    created: function() {
        this.sudoku = this.empty_sudoku()
        
        window.addEventListener('keydown', function(e) {
            if (e.key >= 0 && e.key <= 9) {
                console.log(this.selected_cells)
                // Enter number into selected cells
                
            }
        })
    }
}

</script>

<style scoped>
    #grid { display: inline-block; }
    #grid tr { display: flex; }
    #grid tr:nth-child(3n) .cell { border-bottom: solid 4px; }
    #grid tr:first-child .cell { border-top: solid 4px; }
    #grid tr:last-child .cell { border-bottom: solid 4px; }
    #grid td:nth-child(3n) { border-right: solid 4px; }
    #grid td:first-child { border-left: solid 4px; }
    #grid td:last-child { border-right: solid 4px; }
    .cell { display: inline-block; cursor: pointer; border: solid black; border-width: 0px 1px 1px 0px; width: 50px; height: 50px; text-align: center; font-size: 34px; }

    .highlight {
        background: yellow;
    }
</style>