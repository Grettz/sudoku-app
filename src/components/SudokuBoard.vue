<template>
    <div>
        <table id='sudokuBoard'>
            <tr v-for='(row, i) in sudoku' :key='row.id' :id='"r-" + i'>
                <td v-for='(cell, j) in row' :key='cell.id' :id='"c-" + j' class='cell'
                    :class='{ active: is_cell_active(i, j), locked: sudoku[i][j].isLocked }'
                    @mouseenter="mouse_enter(i, j, $event)"
                    @mousedown="set_active_cell(i, j, $event)">
                        {{ sudoku[i][j] }}
                </td>
            </tr>
        </table>
        <div id="numbers">
            <span v-for='(row, i) in sudoku' :key='row.id' class='number' @click='enter_cells_value(i+1)'>{{ i+1 }}</span>
        </div>
        <div id='load_sudoku' @click='load_sudoku()'>Load Sudoku</div>
    </div>
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
            _ctrl: false,
            temp_sudokus: [[[3, 0, 0, 0, 6, 8, 0, 0, 0], [0, 0, 0, 0, 1, 0, 7, 0, 0], [7, 0, 0, 9, 0, 2, 0, 0, 0], [0, 0, 4, 0, 9, 6, 0, 7, 0], [0, 8, 0, 0, 0, 7, 0, 0, 2], [0, 5, 0, 0, 4, 0, 9, 0, 0], [0, 0, 0, 0, 0, 0, 0, 4, 0], [2, 0, 0, 0, 0, 9, 0, 1, 0], [0, 0, 0, 6, 0, 0, 0, 2, 0]],
                          [[0, 7, 0, 6, 0, 0, 9, 0, 0], [0, 0, 0, 9, 0, 3, 0, 2, 0], [3, 5, 0, 0, 0, 4, 0, 0, 0], [8, 0, 1, 0, 0, 0, 0, 0, 0], [5, 0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 7, 0, 1, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0, 4, 0, 8], [0, 0, 0, 8, 0, 0, 0, 5, 3], [9, 0, 0, 0, 3, 0, 6, 0, 1]],
                          [[0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 6, 0, 0, 0, 0, 1, 0, 5], [0, 0, 0, 0, 0, 3, 0, 2, 0], [2, 0, 0, 0, 0, 4, 0, 6, 0], [4, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 9, 0, 0, 0, 0], [1, 0, 5, 0, 0, 6, 0, 0, 4], [0, 0, 8, 3, 0, 0, 7, 0, 0], [0, 9, 4, 7, 0, 1, 0, 0, 0]],
                          [[8, 0, 9, 0, 0, 0, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 9, 1, 0, 0, 5], [0, 1, 5, 0, 0, 0, 0, 0, 0], [0, 7, 0, 0, 0, 3, 0, 0, 2], [0, 0, 3, 0, 0, 0, 9, 4, 0], [2, 4, 0, 3, 0, 0, 0, 0, 7], [0, 0, 0, 4, 0, 0, 0, 1, 0], [0, 0, 0, 5, 8, 0, 0, 6, 0]],
                          [[0, 9, 0, 0, 0, 6, 3, 0, 0], [7, 8, 0, 0, 0, 0, 0, 0, 0], [6, 0, 0, 1, 5, 0, 0, 0, 0], [0, 0, 0, 0, 0, 4, 0, 5, 3], [0, 7, 0, 0, 0, 0, 0, 2, 0], [1, 0, 9, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 1, 7, 6, 0, 0], [0, 0, 0, 4, 0, 0, 0, 8, 0], [0, 3, 0, 5, 0, 0, 0, 0, 0]],
                          [[0, 2, 3, 4, 0, 1, 0, 0, 0], [1, 0, 0, 0, 5, 0, 0, 0, 0], [0, 7, 0, 0, 0, 0, 0, 4, 5], [0, 0, 0, 0, 0, 2, 0, 9, 0], [0, 0, 0, 0, 6, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 4, 2, 7], [7, 0, 4, 1, 0, 0, 8, 0, 0], [0, 0, 0, 2, 0, 9, 3, 0, 0], [0, 0, 8, 0, 0, 0, 0, 0, 0]],
                          [[0, 0, 0, 0, 0, 6, 1, 0, 4], [2, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 7, 6, 5, 0, 9, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0], [1, 3, 5, 0, 0, 0, 7, 0, 0], [4, 2, 0, 0, 0, 0, 9, 0, 0], [0, 0, 8, 4, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 8, 0, 3, 0]],
                          [[0, 2, 0, 0, 0, 9, 0, 1, 0], [8, 0, 0, 0, 0, 4, 0, 5, 0], [3, 9, 7, 0, 6, 0, 0, 2, 0], [0, 0, 3, 0, 1, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 6, 4], [0, 0, 0, 0, 3, 0, 0, 0, 0], [0, 6, 1, 5, 8, 0, 0, 0, 0], [9, 0, 8, 0, 0, 0, 0, 0, 0], [7, 0, 0, 0, 0, 0, 0, 0, 1]],
                          [[0, 3, 0, 0, 0, 0, 0, 0, 4], [0, 0, 0, 0, 0, 0, 0, 1, 0], [9, 2, 0, 0, 6, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 7], [0, 0, 0, 5, 0, 1, 0, 0, 6], [3, 0, 5, 2, 0, 0, 0, 9, 0], [6, 0, 0, 0, 7, 0, 0, 0, 3], [1, 0, 9, 0, 2, 0, 4, 6, 0], [0, 0, 0, 0, 9, 0, 0, 0, 0]],
                          [[0, 9, 0, 0, 3, 0, 7, 2, 5], [0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 6, 0, 2, 0, 0, 0, 3], [3, 0, 0, 8, 0, 0, 0, 0, 6], [9, 0, 0, 0, 0, 0, 1, 0, 0], [0, 5, 0, 7, 0, 0, 0, 0, 2], [0, 0, 0, 6, 1, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0, 2, 0, 9], [8, 0, 0, 0, 0, 0, 0, 0, 0]],
                          [[0, 0, 4, 0, 0, 9, 0, 0, 0], [0, 0, 8, 0, 6, 2, 0, 0, 0], [6, 0, 0, 0, 0, 3, 0, 1, 2], [1, 0, 0, 0, 9, 0, 0, 0, 4], [0, 0, 0, 1, 0, 7, 6, 0, 8], [0, 2, 7, 0, 0, 4, 0, 0, 1], [0, 0, 0, 0, 8, 0, 5, 0, 6], [0, 0, 0, 0, 0, 0, 0, 0, 7], [7, 0, 3, 0, 0, 0, 0, 0, 0]],
                          [[4, 3, 0, 9, 0, 0, 5, 0, 8], [0, 0, 0, 4, 0, 5, 0, 0, 3], [1, 0, 0, 0, 0, 0, 0, 0, 6], [0, 0, 0, 8, 0, 1, 0, 5, 4], [8, 0, 0, 0, 4, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0, 0, 0], [3, 0, 1, 0, 9, 0, 0, 7, 0], [0, 6, 7, 0, 0, 0, 0, 1, 0]],
                          [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 4, 3, 0, 5, 1, 2, 0], [0, 8, 0, 7, 0, 0, 0, 0, 0], [6, 5, 3, 0, 8, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 7, 0, 5], [2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 6, 0, 0, 0, 4, 0], [7, 0, 0, 0, 0, 3, 0, 1, 0], [8, 0, 0, 0, 4, 0, 3, 0, 0]],
                          [[0, 0, 0, 0, 0, 2, 4, 0, 0], [0, 5, 0, 0, 0, 0, 0, 9, 0], [0, 9, 0, 0, 3, 0, 1, 0, 5], [0, 4, 8, 0, 0, 9, 0, 0, 0], [7, 0, 2, 0, 0, 0, 0, 8, 0], [0, 0, 0, 6, 0, 0, 0, 0, 0], [0, 0, 0, 4, 0, 0, 0, 3, 1], [5, 0, 6, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 9, 7, 0]],
                          [[0, 7, 0, 0, 3, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0, 0, 5, 6], [6, 1, 0, 0, 0, 2, 0, 8, 0], [0, 0, 0, 0, 0, 0, 6, 0, 0], [2, 0, 3, 9, 0, 5, 0, 0, 0], [0, 0, 0, 0, 0, 6, 1, 0, 7], [0, 0, 0, 0, 2, 0, 9, 3, 0], [0, 5, 0, 0, 0, 9, 0, 0, 0]],
                          [[0, 0, 0, 0, 0, 8, 2, 9, 0], [6, 0, 4, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 8], [7, 0, 0, 4, 6, 0, 0, 0, 0], [0, 4, 9, 0, 0, 0, 0, 0, 0], [0, 0, 6, 0, 7, 3, 0, 0, 0], [0, 0, 0, 3, 0, 0, 0, 0, 0], [5, 0, 0, 0, 0, 6, 0, 0, 1], [1, 7, 0, 0, 0, 0, 0, 8, 5]],
                          [[2, 0, 0, 0, 0, 0, 0, 0, 0], [7, 0, 0, 0, 0, 6, 0, 5, 0], [5, 0, 0, 1, 4, 0, 0, 0, 9], [0, 1, 0, 8, 0, 5, 0, 3, 0], [8, 0, 2, 0, 0, 0, 4, 0, 0], [0, 0, 0, 0, 0, 0, 9, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 3], [0, 6, 0, 0, 0, 0, 0, 2, 0], [4, 8, 0, 0, 1, 2, 0, 0, 0]],
                          [[9, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 8, 0, 0, 0, 5], [0, 2, 0, 0, 7, 0, 9, 4, 0], [6, 0, 0, 2, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 3, 8, 9, 0], [0, 7, 0, 1, 0, 0, 0, 0, 0], [7, 0, 0, 0, 0, 6, 0, 3, 0], [0, 6, 0, 0, 0, 1, 5, 0, 0], [0, 0, 5, 7, 0, 0, 0, 0, 0]],
                          [[5, 0, 0, 0, 0, 4, 0, 8, 0], [3, 4, 0, 7, 0, 0, 0, 0, 0], [8, 0, 0, 2, 0, 0, 0, 5, 9], [0, 6, 0, 0, 4, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 6, 0, 0], [0, 0, 7, 0, 0, 0, 0, 2, 0], [0, 2, 0, 0, 0, 9, 0, 0, 0], [0, 0, 0, 8, 0, 0, 0, 9, 2], [9, 0, 5, 6, 2, 0, 0, 0, 1]],
                          [[8, 7, 0, 0, 3, 6, 0, 4, 0], [2, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 4, 0, 0, 0, 0, 7], [0, 0, 0, 7, 0, 0, 0, 6, 1], [0, 8, 3, 0, 0, 0, 0, 0, 0], [0, 0, 4, 0, 0, 5, 0, 0, 0], [0, 0, 0, 1, 0, 0, 6, 0, 0], [3, 0, 9, 0, 0, 0, 0, 0, 2], [0, 0, 0, 6, 0, 8, 0, 0, 0]],
                          [[0, 0, 2, 0, 0, 6, 0, 0, 0], [0, 0, 0, 0, 0, 0, 4, 0, 0], [8, 0, 0, 0, 0, 0, 5, 3, 1], [4, 0, 0, 5, 3, 0, 0, 0, 0], [9, 0, 3, 0, 4, 0, 0, 1, 0], [0, 8, 0, 0, 0, 0, 0, 0, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 5, 9, 0, 0, 2], [0, 0, 6, 0, 0, 0, 9, 0, 0]],
                          [[0, 9, 0, 0, 4, 0, 0, 0, 0], [0, 6, 0, 0, 8, 7, 3, 0, 0], [0, 0, 0, 5, 0, 0, 0, 4, 8], [7, 0, 0, 0, 2, 1, 0, 0, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 9, 4, 3, 0, 0, 6, 5], [0, 0, 8, 7, 6, 0, 0, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0, 7], [0, 0, 0, 0, 0, 0, 5, 2, 0]],
                          [[5, 0, 0, 0, 0, 0, 3, 6, 0], [0, 6, 7, 0, 5, 0, 0, 2, 0], [0, 0, 0, 0, 2, 0, 0, 0, 5], [0, 4, 0, 0, 0, 0, 1, 0, 6], [0, 0, 0, 9, 0, 0, 0, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 9], [1, 0, 8, 6, 0, 0, 0, 0, 0], [0, 0, 2, 3, 0, 9, 0, 0, 0], [0, 0, 4, 7, 0, 0, 0, 0, 8]],
                          [[0, 0, 0, 8, 7, 0, 6, 0, 9], [0, 0, 0, 9, 0, 1, 0, 0, 0], [5, 0, 0, 0, 0, 0, 3, 0, 0], [4, 0, 5, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0, 0, 2, 0], [0, 2, 0, 6, 0, 7, 0, 8, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 5, 0, 0, 3, 9, 0, 0, 0], [1, 0, 0, 0, 6, 0, 0, 4, 0]],
                          [[4, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 7, 6, 0, 0], [0, 8, 0, 0, 1, 0, 0, 3, 0], [0, 0, 0, 0, 0, 2, 4, 1, 3], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 7, 0, 2], [0, 0, 0, 3, 8, 0, 0, 0, 0], [0, 0, 7, 2, 0, 0, 0, 6, 0], [0, 5, 0, 6, 0, 9, 3, 0, 0]]]

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
            // Create empty sudoku grid
            let sudoku = []

            for(let i=0; i<rows; i++) {
                sudoku[i] = new Array(columns)
                
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
        enter_cells_value(value) {
            // Fill all active/selected cells with value
            [].forEach.call(this.active_cells, cell => {
                cell.innerHTML = value
            });
        },
        load_sudoku() {
            let sudoku = this.temp_sudokus[Math.floor(Math.random()*this.temp_sudokus.length)]

            sudoku.forEach((row, i) => {
                row.forEach((cell, j) => {
                    if(cell == 0) {
                        sudoku[i][j] = ''
                    }
                })
            })

            this.sudoku = sudoku
        },
        key_down(e) {
            //Enter number
            if(e.key >= 1 && e.key <= 9) {
                if(e.altKey == true) {
                    this.pencil_cells_value(e.key)
                }
                console.log(e)
                this.enter_cells_value(e.key)
                return
            }
            // Clear cells
            if(e.key == 'Backspace' || e.key == 'Delete') {
                this.enter_cells_value('')
                return
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
            // Is the sudoku board clicked
            let isMouseOnBoard = e.composedPath().includes(document.getElementById('sudokuBoard')) ? true : false
            
            if(!isMouseOnBoard) {
                this.selected_cells = []
            }
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
        // window.addEventListener('mousedown', this.mouse_down)
        // window.addEventListener('mouseup', this.mouse_up)
    },
    destroyed: function() {
        window.removeEventListener('keydown', this.key_down)
        window.removeEventListener('keyup', this.key_up)
        // window.addEventListener('mousedown', this.mouse_down)
        // window.addEventListener('mouseup', this.mouse_up)
    }
}
</script>

<style scoped>
    #sudokuBoard * { color: black; }
    #sudokuBoard { display: inline-block; }
    #sudokuBoard tr { display: flex; }
    #sudokuBoard tr:nth-child(3n) .cell { border-bottom: solid 4px; }
    #sudokuBoard tr:first-child .cell { border-top: solid 4px; }
    #sudokuBoard tr:last-child .cell { border-bottom: solid 4px; }
    #sudokuBoard td:nth-child(3n) { border-right: solid 4px; }
    #sudokuBoard td:first-child { border-left: solid 4px; }
    #sudokuBoard td:last-child { border-right: solid 4px; }
    .cell { display: inline-block; color: darkblue; font-size: 34px; text-align: center; cursor: pointer; border: solid black; border-width: 0px 1px 1px 0px; width: 50px; height: 50px; }
    .locked { color: rgb(255, 0, 0) }

    .active {
        background: yellow;
    }
    #numbers {
        padding: 10px;
        padding-top: 20px;
    }
    .number {
        margin: 7px;
        padding: 8px;
        font-size: 25px;
        border: solid 2px;
        border-radius: 8px;
        cursor: pointer;
    }
    #load_sudoku {
        width: fit-content;
        margin: 7px;
        padding: 8px;
        font-size: 20px;
        border: solid 2px;
        border-radius: 8px;
        cursor: pointer;
    }
</style>