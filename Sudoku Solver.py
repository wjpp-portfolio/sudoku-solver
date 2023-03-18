class Cell:
    """defines an individual cell in a sudoku puzzle"""
    def __init__(self,box,row,column,value):
        self.box = box
        self.row = row
        self.column = column
        self.value = value
        self.viable_values = []

class RCBCellCollection:
    """A collection of 9 Cell to represent every row, column and box.  Used for easier validation solving"""
    def __init__(self):
        self.member_cells = []
        
class SudokuPuzzle:
    """defines an entire sudoku puzzle grid"""
    def __init__(self,puzzle_string=None):
        self.data_map = []
        self.row_collection = []
        self.col_collection = []
        self.box_collection = []
        
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
            if len(self.row_collection) < r:
                self.row_collection.append([])
            if len(self.col_collection) < c:
                self.col_collection.append([])
            if len(self.box_collection) < b:
                self.box_collection.append([])
            self.row_collection[r-1].append(new_cell)
            self.col_collection[c-1].append(new_cell)
            self.box_collection[b-1].append(new_cell)
            
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
                
    def solve(self):
        """identifies solution to current puzzle"""

        change_made = True
        while change_made:
            change_made = False
            #check to see if any cells have only 1 viable number
            for cell in self.data_map:
                
                #print('---------------------------------')
                #print('row:',cell.row,'col:',cell.column)
                if cell.value == ' ':
                    self.__populate_viable_values(cell)
                    #print(cell.viable_values)
                    if len(cell.viable_values) == 1:
                        change_made = True
                        cell.value = cell.viable_values.pop()


                
            #check each row, col and box for whether

        if self.validate():      
            self.show()
        else:
            print('Invalid solution')






    def __populate_viable_values(self,cell):
        """for each cell, identiy which values are viable values based on existing values in row, column and box"""
        row_map = []
        col_map = []
        box_map = []
        cell.viable_values = []
        for other_cell in self.data_map:
            #print('checking against other row:',other_cell.row,'col:',other_cell.column) 
            if (other_cell.row == cell.row and other_cell.column == cell.column) or other_cell.value == ' ':
                #print('cell row and col match, pass')
                continue
            if other_cell.row == cell.row and cell.value not in row_map:
                #print('rows match and cell value not in row_map, adding',other_cell.value,'to row map')
                row_map.append(other_cell.value)
            if other_cell.column == cell.column and cell.value not in col_map:
                #print('columns match and cell value not in col_map, adding',other_cell.value,'to col map')
                col_map.append(other_cell.value)
            if other_cell.box == cell.box and cell.value not in box_map:
                #print('box match and cell value not in box_map, adding',other_cell.value,'to box map')
                box_map.append(other_cell.value)

        #print('row map:',row_map)
        #print('col map:',col_map)
        #print('box map:',box_map)
        for i in range(1,10):
            if i not in row_map and i not in col_map and i not in box_map and i not in cell.viable_values:
                #print(i,'not in any maps, adding to viable_varibles')
                cell.viable_values.append(i)
        
    def validate(self):
        """checks that puzzle in current configuration is valid"""
        #iterate each cell as a reference to check other cells against
        for checked_cell in self.data_map: 
            if checked_cell.value == ' ':
                continue
            #iterate all cells to test against the cell in focus
            for other_cell in self.data_map:
                if checked_cell.row == other_cell.row and checked_cell.column == other_cell.column: 
                    break
                elif checked_cell.value == other_cell.value and (checked_cell.row == other_cell.row or checked_cell.column == other_cell.column or checked_cell.box == other_cell.box):
                    print('Clashing value: row:', checked_cell.row,'col:', checked_cell.column,'with row:',other_cell.row,'col:', other_cell.column)
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
puzzle = '000000000980501607000007094090000048005008300000496100078060450000085000060300902'

game = SudokuPuzzle(puzzle)
game.solve()



            
        #set(this_cell.viable_values).intersection(this_row)
            


#if __name__ == '__main__':
#    main()
