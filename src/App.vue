<template>
    <div id='app' class='disable-select' draggable='false'>
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

    .disable-select {
    -webkit-touch-callout: none; /* iOS Safari */
      -webkit-user-select: none; /* Safari */
       -khtml-user-select: none; /* Konqueror HTML */
         -moz-user-select: none; /* Firefox */
          -ms-user-select: none; /* Internet Explorer/Edge */
              user-select: none; /* Non-prefixed version, currently
                                    supported by Chrome and Opera */
  }
</style>