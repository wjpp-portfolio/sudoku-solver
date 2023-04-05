class Cell:
    """defines an individual cell in a sudoku puzzle and maintains track of values that are possible in this cell"""
    def __init__(self,box,row,column,value):
        self.box = box
        self.row = row
        self.column = column
        self.value = value
        
        if value == 0:
            self.value = ' '
            self.viable_values = {1,2,3,4,5,6,7,8,9}

    def is_filled(self) -> bool:
        """returns True if this cell has a value rather than an empty space"""
        return self.value != ' '

    def is_neighbour(self,other_cell) -> bool:
        """checks if other_cell is in the same row, column or box as self"""
        return (self.row == other_cell.row or
                self.column == other_cell.column or
                self.box == other_cell.box)
                
class SudokuPuzzle:
    """defines an entire sudoku puzzle grid.  Game data is stored in 81-length list of Cell objects"""
    
    def __init__(self,puzzle_string):
        self.data_map = []

        if not self.parse_data_string(puzzle_string):
            raise ValueError('Puzzle string parse failed')
        if not self.validate():
            raise ValueError('Invalid game configuration passed')
            
    def parse_data_string(self,passed_string):
        """ingests passed puzzle string into Cell objects into a list on SudokuPuzzle object"""      
        if len(passed_string) != 81:
            raise ValueError("Passed string not 81 characters long")
        
        self.data_map = []
        r,c,b = 1,1,1 #row, col, box

        box_col_1,box_col_2,box_col_3 = 1,2,3 
        offset = 0 #offset increments by 3 at the 4th row and 3 again at the 7th row, used to work out which 'box' we are in
        
        for i in passed_string:
            try:
                cell_data = int(i)
            except ValueError:
                raise ValueError("Non interger present in game string")
                    
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

            new_cell = Cell(b,r,c,cell_data)
            self.data_map.append(new_cell)
            #if we reach end of the column, reset colum to 1 and increment row by 1
            if c == 9: 
                c = 1
                r += 1
            else:
                c += 1
                
        return True
                        
    def validate(self):
        """checks that puzzle in current configuration is valid by checking each cell, row, and column for duplicates"""
        self.filled_cells = 0
        for cell in (x for x in self.data_map if x.is_filled()):
            self.filled_cells += 1
            if any(y != cell and
                   y.is_filled() and
                   y.is_neighbour(cell) and
                   y.value == cell.value
                   for y in self.data_map):
                return False
        return True
    
    def show(self):
        """prints Sudoku grid to console"""
        row = "{} {} {} | {} {} {} | {} {} {} \n"
        sep = "------|-------|------ \n"
        grid = ((row*3)+sep)*2+row*3
        
        print(grid.format(*[x.value for x in self.data_map]))

    def solve(self):
        """identifies solution to current puzzle firstly through deductions, then backtracking"""
        change_made = True

        while change_made:
            change_made = False
            self.__deductions()
                
            for cell in (x for x in self.data_map if not x.is_filled()):
                if len(cell.viable_values) == 1:
                    cell.value = cell.viable_values.pop()
                    change_made = True
                    
        if self.validate() and self.filled_cells != 81:
            self.__backtrack()
            
        if self.validate() and self.filled_cells == 81:
            return True
        else:
            return False

    def __backtrack(self):
        """creates a new SudokuPuzzle object to work through backtrack until every viable value for every cell has been evaluted."""
        cell_count = 0
        temp_game = SudokuPuzzle(self.export())
        empty_cells = [] #creates a list of just empty cells for working through
        temp_vv = [] #creates a list of 'set' for each cells viable values.  Maintains same index as empty_cells.  Ensure we can re-set the viable-values if we backtrack
        for cell in (x for x in temp_game.data_map if not x.is_filled()):
            temp_vv.append(cell.viable_values.copy())
            empty_cells.append(cell)

        while True:
            if cell_count < 0:
                print('Exhausted all viable values, unsolved')
                return
            #if there are no further viable values for this cell, reset the viable values, reset the cell value and step back 1
            if len(empty_cells[cell_count].viable_values) == 0:
                empty_cells[cell_count].viable_values = temp_vv[cell_count].copy()
                empty_cells[cell_count].value = ' '
                cell_count -= 1
            #assign cell a value from viable_values list, update neighbouring viable values
            else:
                empty_cells[cell_count].value = empty_cells[cell_count].viable_values.pop()
                temp_game.__eliminate_nonviable_values_based_on_neighbour_values(empty_cells[cell_count])
                            
                if temp_game.validate():
                    if temp_game.filled_cells == 81:
                        self.parse_data_string(temp_game.export())
                        return
                    else:
                        cell_count += 1          
           
    def __deductions(self):
        """for each row, box and column, identify any viable values that cannot exist based on neighbouring row/box/column and remove them"""
        for cell in (x for x in self.data_map if not x.is_filled()):
            self.__eliminate_nonviable_values_based_on_neighbour_values(cell)
            viable_values_in_row = []
            viable_values_in_col = []
            viable_values_in_box = []
            for sub_cell in (x for x in self.data_map
                             if not x.is_filled() and
                             x != cell
                             ):
                for sub_viable in sub_cell.viable_values:
                    if sub_cell.row == cell.row:
                        viable_values_in_row.append(sub_viable)
                    if sub_cell.column == cell.column:
                        viable_values_in_col.append(sub_viable)
                    if sub_cell.box == cell.box:
                        viable_values_in_box.append(sub_viable)
                       
            values_to_remove = []
            for cell_v in (y for y in cell.viable_values if y not in viable_values_in_row):
                for row_v in viable_values_in_row:
                    values_to_remove.append(row_v)           
            for cell_v in (y for y in cell.viable_values if y not in viable_values_in_col):
                for col_v in viable_values_in_col:
                    values_to_remove.append(col_v)   
            for cell_v in (y for y in cell.viable_values if y not in viable_values_in_box):
                for box_v in viable_values_in_box:
                    values_to_remove.append(box_v)
                    
            for value in values_to_remove:
                try:   
                    cell.viable_values.remove(value)
                except KeyError:
                    pass

    def __eliminate_nonviable_values_based_on_neighbour_values(self,cell):
        """for passed cell, iterate across all data to identiy which values could be valid values based on existing values in relevant row, column and box"""
        neighbour_values = set()
        for other_cell in (x for x in self.data_map
                           if x.is_filled() and
                           x != cell and
                           x.is_neighbour(cell)
                           ):
            neighbour_values.add(other_cell.value)

        for i in range(1,10):
            if i in neighbour_values and i in cell.viable_values:
                cell.viable_values.remove(i)

    def export(self):
        """writes puzzle data to string, the same format as the object ingests data"""
        export_string = ''
        for cell in self.data_map:
            if not cell.is_filled():
                export_string += str(0)
            else:
                export_string += str(cell.value)

        return export_string
            
def main():       
    string_input = input('Enter numbers from Sudoku grid starting from top left and enter across and down with the last digit being bottom right box. Use zero (0) for empty spaces: ')
    #string_input = '010000370000006082000400000003510000700908003000023900000004000820300000065000010'
    print('Inputted string:',string_input)
    game = SudokuPuzzle(string_input)
    game.show()
    print('')
    if game.solve():
        print('Solution found!')
        game.show()
        print('Solution string:',game.export())
    else:
        print('Solution NOT found')
        game.show()
    
if __name__ == '__main__':
    main()
