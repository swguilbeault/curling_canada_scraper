class Grid:
    def __init__(self,width=0,height=0):
        self.grid = [[None for i in range(height)] for i in range(width)]
        self._width = width
        self._height = height
        
        self.display_settings = {
            "None_rep": "-",
            "column_seperator": "   ",
            "align": "left",
            "seperate_rows": False,
            "row_seperator": " "
            }
        
    def add_column(self,n=1):
        for i in range(n):
            self.grid.append([None for i in range(self._height)])
        self._width += n
            
    def add_row(self,n=1):
        for i in range(self._width):
            self.grid[i] += [None for i in range(n)]
        self._height += n
        
    def append_row(self, row):
        self._expand_to(len(row),0);
        self.add_row()
        for index,i in enumerate(row):
            self.grid[index][-1] = row[index]
        
    def transpose(self):
        self.grid = [[j[i] for j in self.grid] for i in range(self._height)]
        self._height, self._width = self._width, self._height
        
    def put(self,grid,x0=0,y0=0,write_None_cells=True):
        if y0 < 0:
            y0 = self._height + y0
            
        if x0 < 0:
            x0 = self._width + x0
        
        if y0 < 0 or x0 < 0:
            raise IndexError("point out of range: (" + str(x0) + ", " + str(y0) + ")")
        
        if isinstance(grid, Grid):
            grid = grid.grid
            
        self._expand_to(x0+len(grid), y0+max([len(i) for i in grid]))
        
        for x in range(len(grid)):
            for y in range(max([len(i) for i in grid])):
                if len(grid[x]) > y:
                    if write_None_cells or grid[x][y] != None:
                        self[x0 + x][y0 + y] = grid[x][y]
                else:
                    if write_None_cells:
                        self[x0 + x][y0 + y] = None
    
    def toCSV(self, path, c=","):
        with open(path, "w") as f:
            rows = []
            for y in range(self._height):
                row = []
                for x in range(self._width):
                    row.append(str(self.grid[x][y]))
                rows.append(c.join(row))
            out = "\n".join(rows)
            f.write(out)
    
    def __str__(self,pillow=lambda x : x):
        strings = Grid(self._width,self._height)
        for i,x,y in self:
            if i != None:
                strings[x][y] = str(pillow(i))
            else:
                strings[x][y] = self.display_settings["None_rep"]
                
        #print("\n".join(str(i) for i in strings.grid))
        
        column_widths = []
        for i in range(self._width):
            column_widths.append(max([len(j) for j in strings[i]] + [1]))
        
        row_heights = []
        for i in range(self._height):
            row_heights.append(max([j[i].count("\n") + 1 for j in strings.grid] + [1]))
            
        #print(column_widths)
        #print(row_heights)
        
        rows = []
        for y in range(self._height):
            row = []
            for y2 in range(row_heights[y]):
                row_ = []
                for x in range(self._width):
                    if len(strings[x][y].split("\n")) > y2:
                        row_.append(self._widened(strings[x][y].split("\n")[y2], column_widths[x]))
                    else:
                        row_.append(self._widened("", column_widths[x]))          
                    
                row.append(self.display_settings["column_seperator"].join(row_))
            rows.append("\n".join(row))
        
        if self.display_settings["seperate_rows"]:
            return ("\n" + self.display_settings["row_seperator"] * (sum(column_widths) + len(self.display_settings["column_seperator"])*(self._width - 1)) + "\n").join(rows)
        
        return "\n".join(rows)
    
    def _widened(self,string, width):
        if self.display_settings["align"] == "center":
            return " "*int((width - len(string) + 1) / 2) + string + " "*int((width - len(string)) / 2)
        elif self.display_settings["align"] == "right":
            return " "*(width-len(string)) + string
        return string + " "*(width-len(string))
    
    def __getitem__(self,i):
        return self.grid[i]
    
    def __iter__(self):
        out = []
        for x in range(self._width):
            for y in range(self._height):
                out.append((self[x][y], x, y))
        return iter(out)
    
    def _expand_to(self,x,y):
        if x > self._width:
            self.add_column(x - self._width)
            
        if y > self._height:
            self.add_row(y - self._height)