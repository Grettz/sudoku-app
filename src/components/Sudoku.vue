<template>
    <div id='sudoku'>
        <table id='grid' class='disable-select' draggable='false'>
            <tr v-for='(row, i) in sudoku' :key='row.id' :id='"r-" + i'>
                <td v-for='(cell, j) in row' :key='cell.id' :id='"c-" + j' @click="select_cell(i, j)" class='cell'>{{ sudoku[i][j] }}</td>
            </tr>
        </table>
        <p>{{ selected_cells }}</p>
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
        select_cell(i, j) {
            console.log(this.is_cell_selected(i, j))
            if(this.is_cell_selected(i, j) == true) {
                console.log('Pop')
                return
            }
            let coord = {"i": i, "j": j}
            this.selected_cells.push(coord)
        },
        is_cell_selected(i, j) {
            this.selected_cells.forEach(function(cell) {
                console.log(cell)
                if(cell.i == i || cell.j == j) {
                    console.log('TRUE')
                    return
                }
            })
            return false
        }
    },
    created: function() {
        this.sudoku = this.empty_sudoku()
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
</style>