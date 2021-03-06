import requests
from bs4 import BeautifulSoup


def main():
    # Difficulty level of sudoku and how many to scrape; 1 to 5 (very easy to very hard)
    LEVEL = 4
    TO_GET = 50

    file = open('sudoku_9x9_lvl_' + str(LEVEL) + '.txt', 'a')

    for i in range(TO_GET):
        sudoku = scrape_sudoku_9_x_9(LEVEL)
        file.write('\n' + str(sudoku))

        if (i + 1) % 10 == 0 or i == TO_GET - 1:
            print('{0}/{1}'.format(i + 1, TO_GET))

def scrape_sudoku_9_x_9(LEVEL):
    # Scrape sudoku boards from sudoku9x9.com
    # Levels 1 to 5 = very easy to very hard
    url = 'https://sudoku9x9.com/?level=' + str(LEVEL)
    
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    # Sudoku table and list of cells
    playtable = soup.find(id='playtable')
    cells = playtable.find_all(class_='t1')

    sudoku = empty_sudoku()

    for i in range(9):
        for j in range(9):
            # Cell index for cells list
            c = i * 9 + j
            try:
                sudoku[i][j] = int(cells[c].text)
            except ValueError:
                pass

    # for row in sudoku:
    #     print(row)

    return sudoku

def empty_sudoku():
    return [[0 for _ in range(9)] for _ in range(9)]


if __name__ == "__main__":
    main()