class Cell:
    """defines an individual cell in a sudoku puzzle"""
    def __init__(self,box,row,column,value):
        self.box = box
        self.row = row
        self.column = column
        self.value = value
        
        if value == 0:
            self.value = ' '
            self.viable_values = {1,2,3,4,5,6,7,8,9}
        else:
            self.viable_values = set()
                
class SudokuPuzzle:
    """defines an entire sudoku puzzle grid"""
    def __init__(self,puzzle_string = None):
        self.data_map = []
        self.game_string = puzzle_string
        self.debug = False
        
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
        
        self.data_map = []
        
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

            new_cell = Cell(b,r,c,cell_data)
            
            self.data_map.append(new_cell)

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

        print('Filled cells:',self.filled_cells)

    def solve(self):
        """identifies solution to current puzzle firstly through deductions, then backtracking"""
        change_made = True

        while change_made:
            change_made = False
            self.__deductions()
                
            for cell in [x for x in self.data_map if x.value == ' ']:
                if len(cell.viable_values) == 1:
                    change_made = True
                    cell.value = cell.viable_values.pop()
                    
        if self.validate() and self.filled_cells != 81:
            self.__backtrack()
            
        if self.validate() and self.filled_cells == 81:
            return True
        else:
            return False



    def __backtrack(self):
        """attempt a value in a box (based on viable values) and see if it leads to a solution"""
        pass
        #for cell in [x for x in self.data_map if x.value == ' ']:
        #    for cell_v in cell.viable_values:

       
    def __deductions(self):
        """for each row, box and column, identify any viable values that cannot exist based on neighbouring row/box/column and remove them"""
        for cell in [x for x in self.data_map if x.value == ' ']:

            self.__eliminate_nonviable_values_based_on_neighbour_values(cell)
            viable_values_in_row = []
            viable_values_in_col = []
            viable_values_in_box = []
            for sub_cell in [x for x in self.data_map if x.value == ' ' and x != cell]:
                for sub_viable in sub_cell.viable_values:
                    if sub_cell.row == cell.row:
                        viable_values_in_row.append(sub_viable)
                    if sub_cell.column == cell.column:
                        viable_values_in_col.append(sub_viable)
                    if sub_cell.box == cell.box:
                        viable_values_in_box.append(sub_viable)
                       
            values_to_remove = []
            for cell_v in [y for y in cell.viable_values if y not in viable_values_in_row]:
                for row_v in viable_values_in_row:
                    values_to_remove.append(row_v)           
            for cell_v in [y for y in cell.viable_values if y not in viable_values_in_col]:
                for col_v in viable_values_in_col:
                    values_to_remove.append(col_v)   
            for cell_v in [y for y in cell.viable_values if y not in viable_values_in_box]:
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
        for other_cell in [x for x in self.data_map if x.value != ' ' and x != cell and (x.row == cell.row or x.column == cell.column or x.box == cell.box)]:
            neighbour_values.add(other_cell.value)

        for i in range(1,10):
            if i in neighbour_values and i in cell.viable_values:
                cell.viable_values.remove(i)
                    
    def validate(self):
        """checks that puzzle in current configuration is valid"""

        self.filled_cells = 0
        for i in [x for x in self.data_map if x.value != ' ']:
            self.filled_cells += 1
        
        for cell in [x for x in self.data_map if x.value != ' ']: 
            for other_cell in [y for y in self.data_map if y != cell and y.value != ' ' and y.value == cell.value and (y.row == cell.row or y.column == cell.column or y.box == cell.box)]: 
                raise ValueError('Validation failed - clashing value: row:', cell.row,'col:', cell.column,'with row:',other_cell.row,'col:', other_cell.column)
                return False                
        return True
        
    def generate(self):
        """generates a sudoku puzzle"""
        pass
    def export(self):
        """writes puzzle data to string"""
        export_string = ''
        for cell in self.data_map:
            if cell.value == ' ':
                export_string += str(0)
            else:
                export_string += str(cell.value)

        return export_string
            


#def main():
puzzle = '000040610600000000501002084090007002000080000210306700105063400960015000300000000'
#puzzle = '207010605095600020800004000000000260000726018000090030050000300604530000012079000'
game = SudokuPuzzle(puzzle)
game.show()
print('#####################')
if game.solve():
    print('Solution found!')
    game.show()
    print(game.export())
else:
    print('Solution not found')
    game.show()
    


#if __name__ == '__main__':
#    main()
