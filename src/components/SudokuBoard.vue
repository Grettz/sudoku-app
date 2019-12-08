<template>
    <table id='SudokuBoard' class='disable-select' draggable='false'>
        <tr v-for='(row, i) in sudoku' :key='row.id' :id='"r-" + i'>
            <td v-for='(cell, j) in row' :key='cell.id' :id='"c-" + j' class='cell'
                :class='{ active: is_cell_active(i, j), locked: sudoku[i][j].isLocked }'
                @mouseenter="mouse_enter(i, j, $event)"
                @mousedown="set_active_cell(i, j, $event)">
                    {{ sudoku[i][j] }}
            </td>
        </tr>
    </table>
</template>

<script>
export default {
    name: 'SudokuBoard',
    data: function() {
        return {
            sudoku: [],
            selected_cells: [],
            active_cells: document.getElementsByClassName('active'),
            _mouse: false,
            _shift: false,
            _ctrl: false
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
        set_active_cell(i, j, event) {
            let coord = {"i": i, "j": j}

            if(event.ctrlKey) {
                this.selected_cells.push(coord)
            } else {
                this.selected_cells = [coord]
            }
        },
        is_cell_active(i, j) {
            let cell_index = this.selected_cells.findIndex(cell => cell.i == i && cell.j == j)
            if(cell_index >= 0) {
                return true
            }
            return false
        },
        key_down(e) {
            if(e.key >= 0 && e.key <= 9) {
                let active_cells = document.getElementsByClassName('active')
                for(let i=0; i<active_cells.length; i++) {
                    active_cells[i].innerHTML = e.key
                }

                //Insert number
                this.selected_cells.forEach(function(cell) {
                    let row = document.getElementsByClassName('active')
                })
            }
            if(e.key == 'Control') {
                this._ctrl = true;
            }
            if(e.key == 'Shift') {
                this._shift = true;
            }
        },
        key_up(e) {
            if(e.key == 'Control') {
                this._ctrl = false;
            }
            if(e.key == 'Shift') {
                this._shift = false;
            }
        },
        mouse_down(e) {
            console.log(e)
        },
        mouse_enter(i, j, event) {
            if(event.which == 1) {
                let coord = {"i": i, "j": j}
                this.selected_cells.push(coord)
            }
        }
    },
    created: function() {
        this.sudoku = this.empty_sudoku()
        window.addEventListener('keydown', this.key_down)
        window.addEventListener('keyup', this.key_up)
        window.addEventListener('mousedown', this.mouse_down)
    },
    destroyed: function() {
        window.removeEventListener('keydown', this.key_down)
        window.removeEventListener('keyup', this.key_up)
        window.addEventListener('mousedown', this.mouse_down)
    }
}
</script>

<style scoped>
    #SudokuBoard * { color: black; }
    #SudokuBoard { display: inline-block; }
    #SudokuBoard tr { display: flex; }
    #SudokuBoard tr:nth-child(3n) .cell { border-bottom: solid 4px; }
    #SudokuBoard tr:first-child .cell { border-top: solid 4px; }
    #SudokuBoard tr:last-child .cell { border-bottom: solid 4px; }
    #SudokuBoard td:nth-child(3n) { border-right: solid 4px; }
    #SudokuBoard td:first-child { border-left: solid 4px; }
    #SudokuBoard td:last-child { border-right: solid 4px; }
    .cell { display: inline-block; color: darkblue; font-size: 34px; text-align: center; cursor: pointer; border: solid black; border-width: 0px 1px 1px 0px; width: 50px; height: 50px; }
    .locked { color: rgb(255, 0, 0) }

    .active {
        background: yellow;
    }

    .disable-select{
    -webkit-touch-callout: none; /* iOS Safari */
      -webkit-user-select: none; /* Safari */
       -khtml-user-select: none; /* Konqueror HTML */
         -moz-user-select: none; /* Firefox */
          -ms-user-select: none; /* Internet Explorer/Edge */
              user-select: none; /* Non-prefixed version, currently
                                    supported by Chrome and Opera */
  }
</style>