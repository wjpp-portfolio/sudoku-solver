class Cell:
    """defines an individual cell in a sudoku puzzle"""
    def __init__(self,box,row,column,value):
        self.box = box
        self.row = row
        self.column = column
        self.value = value
        self.viable_values = []

#class RCBCellCollection:
#    """A collection of 9 Cell to represent every row, column and box.  Used for easier validation solving"""
#    def __init__(self):
#        self.member_cells = []
        
class SudokuPuzzle:
    """defines an entire sudoku puzzle grid"""
    def __init__(self,puzzle_string=None):
        self.data_map = []
        self.game_string = puzzle_string
        #self.row_collection = []
        #self.col_collection = []
        #self.box_collection = []
        
        if puzzle_string is None:
            self.generate()
        else:
            self.parse_data_string(puzzle_string)
            self.validate()
            
    def parse_data_string(self,passed_string):
        """ingests passed puzzle string into Cell objects"""
      
        if len(passed_string) != 81:
            raise ValueError("Passed string not 81 characters long")
            return

        r = 1 #row
        c = 1 #column
        b = 1 #9x9 box
        box_col_1,box_col_2,box_col_3 = 1,2,3 
        
        offset = 0 #offset increments by 3 at the 4th row and 3 again at the 7th row, used to work out which 'box' we are in
        for i in passed_string:
            try:
                cell_data = int(i)
            except:
                raise ValueError("Non interger present in game string")
                return
            
            
            # to calculate which of the 9 boxes (3x3 grids) this cell is in
            if r > 6:
                offset = 6
            elif r > 3:
                offset = 3
                
            if c > 6:
                b = box_col_3+offset
            elif c > 3:
                b = box_col_2+offset
            else:
                b = box_col_1+offset

            if cell_data == 0:
                cell_data = ' '
            new_cell = Cell(b,r,c,cell_data)
            
            self.data_map.append(new_cell)

            #add each Cell object to a corresponding 'row', 'column' or 'box list for easier lookups later
            #if len(self.row_collection) < r:
            #    self.row_collection.append([])
            #if len(self.col_collection) < c:
            #    self.col_collection.append([])
            #if len(self.box_collection) < b:
            #    self.box_collection.append([])
            #self.row_collection[r-1].append(new_cell)
            #self.col_collection[c-1].append(new_cell)
            #self.box_collection[b-1].append(new_cell)
            
            #if we reach end of the column, reset colum to 1 and increment row by 1
            if c == 9: 
                c = 1
                r += 1
            else:
                c += 1
            
    def show(self):
        """prints Sudoku grid to console"""
        for i in self.data_map:
            print(i.value,end=' ')
            if i.column == 3 or i.column == 6:
                print('|',end=' ')
            if i.column == 9:
                print('')
            if (i.row == 3 or i.row == 6) and i.column == 9:
                print('------+-------+------')

        print('')
        counter = 0
        for i in [x for x in self.data_map if x.value != ' ']:
            counter += 1
        print('filled cells = ',counter)
    def solve(self):
        """identifies solution to current puzzle"""

        change_made = True
        while change_made:
            print('new loop --------------------------------------')
            self.show()
            change_made = False
      
            for cell in [x for x in self.data_map if x.value == ' ']:
                print('cell',cell.row,cell.column,cell.box)
                self.__populate_viable_values(cell)

                #check to see if any cells have only 1 viable number
                if len(cell.viable_values) == 1:
                    change_made = True
                    cell.value = cell.viable_values.pop()
                else:
                    print(cell.viable_values)

                



 

        if self.validate():      
            self.show()
        else:
            print('Invalid solution')

    def __populate_viable_values(self,cell):
        """Identify any cell that has only a single real viable value based on its row, colum and box.  E.g. if it has viable values of 1,3 and 6 but 3 does not appear as a viable value for any cell in the same row, column or box, value can only be 3"""
        viable_values_in_row_col_box = []

        for other_cell in [x for x in self.data_map if x.value == ' ' and x != cell and (x.row == cell.row or x.column == cell.column or x.box == cell.box)]: 
            self.__get_possible_cell_values(other_cell)  

            for other_cell_viable in other_cell.viable_values:
                viable_values_in_row_col_box.append(other_cell_viable)
                
        for cell_viable in cell.viable_values:
            if cell_viable not in viable_values_in_row_col_box:
                cell.viable_values = []
                cell.viable_values.append(cell_viable) #main solve routine will discover single item and assign it as cell value

    def __get_possible_cell_values(self,cell):
        """for passed cell, iterate across all data to identiy which values could be valid values based on existing values in relevant row, column and box"""
        neighbour_values = []
        cell.viable_values = []
        for other_cell in [x for x in self.data_map if x != cell and x.value != ' ' and x.value not in neighbour_values and (x.row == cell.row or x.column == cell.column or x.box == cell.box)]:
            neighbour_values.append(other_cell.value)

        for i in range(1,10):
            if i not in neighbour_values and i not in cell.viable_values:
                cell.viable_values.append(i)
                
    def validate(self):
        """checks that puzzle in current configuration is valid"""
        #iterate each cell as a reference to check other cells against
        for cell in [x for x in self.data_map if x.value != ' ']: 
            #iterate all other cells to test whether it has a same value in the row, column or box
            for other_cell in [y for y in self.data_map if cell != y and y.value != ' ' and (y.row == cell.row or y.column == cell.column or y.box == cell.box) and y.value == cell.value]: 
                print('Clashing value: row:', cell.row,'col:', cell.column,'with row:',other_cell.row,'col:', other_cell.column)
                raise ValueError('Validation failed')
                return False                
        return True
        
    def generate(self):
        """generates a sudoku puzzle"""
        pass
    def export(self):
        """writes puzzle data to string"""
        export_string = ''
        for i in self.data_map:
            if i.value == ' ':
                i.value = 0
            export_string += str(i.value)

        return export_string
            


#def main():
puzzle = '506102000000650017810000050000200090900507008051039040008000409765984000009000000'

game = SudokuPuzzle(puzzle)
game.show()
print('#####################')
game.solve()



#if __name__ == '__main__':
#    main()
